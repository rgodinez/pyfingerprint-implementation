#!/usr/bin/env python
# -*- coding: utf-8 -*-

## imports
import csv
import time
from pyfingerprint.pyfingerprint import PyFingerprint

## Searches for a finger and alias associated with it

## Tries to initialize the sensor
try:
	f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
	
	if( f.verifyPassword() == False):
		raise ValueError('The given fingerprint sensor password is wrong!')
	

except Exception as e:
	print('The fingerprint sensor could not be initialized!')
	print('Exception message: ' + str(e))
	exit(1)

## Get sensor storage information
print('Currently used templates: ' + str(f.getTemplateCount()) + '/' + str(f.getStorageCapacity()))

## Tries to search the finger and finds alias
try:
	print('Waiting for finger...')
	
	## Finger read loop
	while(f.readImage() == False):
		pass
	
	## Converts read image to characteristics and stores in charbuffer 1
	f.convertImage(0x01)
	
	## Searches templates
	result = f.searchTemplate()
	
	positionNumber = result[0]
	accuracyScore = result[1]
	
	if( positionNumber == -1):
		print('No match found!')
		exit(0)
	else:
		print('Found template at position #' + str(positionNumber))
		print('The accuracy score is: ' + str(accuracyScore))
	
	## Loads template into charbuffer 1
	f.loadTemplate(positionNumber, 0x01)
	
	## Check hashes stored on system and find alias
	aliasFound = []
	
	with open('testRoster.csv', 'rb') as rosterFile:
		print('Reading roster...')
		rosterReader = csv.reader(rosterFile, delimiter=',')
		
		for row in rosterReader:
			tempAlias = ''.join(row)
			
			if positionNumber in tempAlias:
				aliasFound.append(tempAlias)
				break
	
	aliasFound = aliasFound[0].split(',')[0]
	
	## Store clock-in time for alias
	with open('timesheet.csv', 'a') as timesheetFile:
		print('Writing to timesheet...')
		timesheetWriter = csv.writer(timesheetFile)
		
		clockInTime = time.strftime('%m-%d-%Y %H:%M:%S')
		rowEntry = [clockInTime + ' - ' + aliasFound]
		
		timesheetWriter.writerow(rowEntry)
	

except Exception as e:
	print('Operation failed!')
	print('Exception message: ' + str(e))
	exit(1)