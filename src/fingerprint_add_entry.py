#!/usr/bin/env python
# -*- coding: utf-8 -*-

## imports
import csv
import time
import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint

## Enrolls new finger and returns hashed characteristics
def enroll_entry(f):
	print('Waiting for finger...')
	
	## Waits for finger to be read
	while( f.readImage() == False):
		pass
	
	## Converts read image to characteristics and stores to charbuffer 1
	f.convertImage(0x01)
	
	## Checks if finger is already enrolled
	result = f.searchTemplate()
	positionNumber = result[0]
	
	if( positionNumber >= 0):
		print('Template already exists at position #' + str(positionNumber))
		exit(0)
	
	print('Remove finger...')
	time.sleep(2)
	
	print('Confirming finger characteristics.')
	print('Waiting for same finger again...')
	
	## Waiting for confirmation finger read
	while(f.readImage() == False):
		pass
	
	## Converts read image to characteristics and stores to charbuffer 2
	f.convertImage(0x02)
	
	## Compares buffer for confirmation
	if( f.compareCharacteristics() == 0):
		raise Exception('Fingers do not match.')
	
	## Creates characteristics template
	f.createTemplate()
	
	## Saves template at empty position number
	f.storeTemplate()
	
	## Downloads characteristics of template in charbuffer 1
	characteristics = str(f.downloadCharacteristics(0x01)).encode('utf-8')
	
	## Hashes characteristics
	hashedCharacteristics = hashlib.sha256(characteristics).hexdigest()
	
	return hashedCharacteristics

## Tries to initialize the sensor
try:
	f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
	
	if( f.verifyPassword() == False):
		raise ValueError('The given fingerprint sensor password is wrong!')
	

except Exception as e:
	print('The fingerprint sensor could not be initialized!')
	print('Exception message: ' + str(e))
	exit(1)

## Gets sensor storage information
print('Currently used templates: ' + str(f.getTemplateCount()) + '/' + str(f.getStorageCapacity()))

if( f.getTemplateCount() + 3 > f.getStorageCapacity()):
	print('Scanner memory full! Cannot add entries.')
	exit(1)

entryName = raw_input('Enter new entry name: ')
entryName = str(entryName)

print('Starting scans for ' + entryName)

## Tries to enroll new finger
try:
	characteristics = enroll_entry(f)
	
	with open('testRoster.csv', 'a') as rosterFile:
		print('Adding to roster...')
		rosterWriter = csv.writer(rosterFile)
		
		rosterEntry = [entryName, characteristics]
		rosterWriter.writerow(rosterEntry)
	
	print('Finger enrolled successfully!')
	
except Exception as e:
	print('Operation failed!')
	print('Exception message: ' + str(e))
	exit(1)