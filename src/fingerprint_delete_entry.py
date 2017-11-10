#!/usr/bin/env python
# -*- coding: utf-8 -*-

## imports
import csv
from pyfingerprint.pyfingerprint import PyFingerprint

## Deletes roster entry from scanner memory and roster index file

## Searches for entry and extract characteristics
def search_entry(entryName):
	
	rows = []	
	positionNumber = []
	
	with open('testRoster.csv', 'rb') as rosterFile:
		alias = entryName
		
		print('Reading roster for entry...')
		rosterReader = csv.reader(rosterFile, delimiter=',')
		
		for row in rosterReader:
			if entryName not in row[0]:
				rows.append(row)
			else:
				positionNumber.append(row[1])
	
	with open('testRoster.csv','w') as rosterFile:
		print('Updating roster...')
		rosterWriter = csv.writer(rosterFile, delimiter=',')
		
		rosterWriter.writerows(rows)
	
	return positionNumber[0]

## Tries to initialize the sensor
try:
	f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
	
	if( f.verifyPassword() == False):
		raise ValueError('The given fingerprint sensor password is wrong!')
	
except Exception as e:
	print('The given fingerprint sensor password is wrong!')
	print('Exception message: ' + str(e))
	exit(1)

## Deletes template from index
try:
	alias = raw_input('Enter name to delete: ')
	alias = str(alias)
	
	positionNumber = search_entry(alias)
	
	if(f.deleteTemplate(positionNumber) == True):
		print('Template deleted! There are ' + str(f.getStorageCapacity()) + ' templates stored.')
	
except Exception as e:
	print('Operation failed!')
	print('Exception message: ' + str(e))
	exit(1)