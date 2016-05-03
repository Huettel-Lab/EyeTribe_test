# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 16:43:16 2016

@author: eig4
"""

import copy
import os.path

import numpy

from detectors import blink_detection, fixation_detection, saccade_detection


def read_tobii(filename, start, stop=None, missing=0.0, debug=False):
	
	"""Returns a list with dicts for every trial. A trial dict contains the
	following keys:
		x		-	numpy array of x positions
		y		-	numpy array of y positions
		size		-	numpy array of pupil size
		time		-	numpy array of timestamps, t=0 at trialstart
		trackertime-	numpy array of timestamps, according to the tracker
		events	-	dict with the following keys:
						Sfix	-	list of lists, each containing [starttime]
						Ssac	-	EMPTY! list of lists, each containing [starttime]
						Sblk	-	list of lists, each containing [starttime]
						Efix	-	list of lists, each containing [starttime, endtime, duration, endx, endy]
						Esac	-	EMPTY! list of lists, each containing [starttime, endtime, duration, startx, starty, endx, endy]
						Eblk	-	list of lists, each containing [starttime, endtime, duration]
						msg	-	list of lists, each containing [time, message]
						NOTE: timing is in EyeTribe time!
	
	arguments

	filename		-	path to the file that has to be read
	start		-	trial start string
	
	keyword arguments

	stop		-	trial ending string (default = None)
	missing	-	value to be used for missing data (default = 0.0)
	debug	-	Boolean indicating if DEBUG mode should be on or off;
				if DEBUG mode is on, information on what the script
				currently is doing will be printed to the console
				(default = False)
	
	returns

	data		-	a list with a dict for every trial (see above)
	"""

	# # # # #
	# debug mode
	
	if debug:
		def message(msg):
			print(msg)
	else:
		def message(msg):
			pass
		
	
	# # # # #
	# file handling
	
	# check if the file exists
	if os.path.isfile(filename):
		# open file
		message("opening file '%s'" % filename)
		f = open(filename, 'r')
	# raise exception if the file does not exist
	else:
		raise Exception("Error in read_tobii: file '%s' does not exist" % filename)
	
	# read file contents
	message("reading file '%s'" % filename)
	raw = f.readlines()
	
	# close file
	message("closing file '%s'" % filename)
	f.close()

	
	# # # # #
	# parse lines
	
	# variables
	data = []
	x = []
	y = []
	size = []
	time = []
	trackertime = []
	events = {'Sfix':[],'Ssac':[],'Sblk':[],'Efix':[],'Esac':[],'Eblk':[],'msg':[]}
	starttime = 0
	started = False
	trialend = False
	
	# loop through all lines
	for i in range(len(raw)):
		
		# string to list
		line = raw[i].replace('\n','').replace('\r','').split('\t')
		
		#print(line)
		
		# check if trial has already started
		if started:
			# only check for stop if there is one
			if stop != None:
				if (line[0] == 'MSG' and stop in line[3]) or i == len(raw)-1:
					started = False
					trialend = True
			# check for new start otherwise
			else:
				if start in line:
					started = True
					trialend = True

			# # # # #
			# trial ending
			
			if trialend:
				message("trialend %d; %d samples found" % (len(data),len(x)))
				# trial dict
				trial = {}
				trial['x'] = numpy.array(x)
				trial['y'] = numpy.array(y)
				trial['size'] = numpy.array(size)
				trial['time'] = numpy.array(time)
				trial['trackertime'] = numpy.array(trackertime)
				trial['events'] = copy.deepcopy(events)
				# events
				trial['events']['Sblk'], trial['events']['Eblk'] = blink_detection(trial['x'],trial['y'],trial['trackertime'],missing=missing)
				trial['events']['Sfix'], trial['events']['Efix'] = fixation_detection(trial['x'],trial['y'],trial['trackertime'],missing=missing)
				trial['events']['Ssac'], trial['events']['Esac'] = saccade_detection(trial['x'],trial['y'],trial['trackertime'],missing=missing)
				# add trial to data
				data.append(trial)
				# reset stuff
				x = []
				y = []
				size = []
				time = []
				trackertime = []
				events = {'Sfix':[],'Ssac':[],'Sblk':[],'Efix':[],'Esac':[],'Eblk':[],'msg':[]}
				trialend = False
				
		# check if the current line contains start message
		else:
			#if line[0] == "MSG":
			#if start in line[0]:
				message("trialstart %d" % len(data))
				# set started to True
				started = True
				# find starting time
				#starttime = int(line[2])
		
		# # # # #
		# parse line
		
		if started:
			# message lines will start with MSG, followed by a tab, then a
			# timestamp, a tab, the time, a tab and the message, e.g.:
			#	"MSG\t2014-07-01 17:02:33.770\t853589802\tsomething of importance here"
			if line[0] == "MSG":
				t = int(line[2]) # time
				m = line[3] # message
				events['msg'].append([t,m])
			
			# regular lines will contain tab separated values, beginning with
			# a timestamp, follwed by the values that were asked to be stored
			# in the data file. Usually, this comes down to
			# timestamp, time, fix, state, rawx, rawy, avgx, avgy, psize, 
			# Lrawx, Lrawy, Lavgx, Lavgy, Lpsize, Lpupilx, Lpupily,
			# Rrawx, Rrawy, Ravgx, Ravgy, Rpsize, Rpupilx, Rpupily
			# e.g.:
			# '2014-07-01 17:02:33.770, 853589802, False, 7, 512.5897, 510.8104, 614.6975, 614.3327, 16.8657,
			# 523.3592, 475.2756, 511.1529, 492.7412, 16.9398, 0.4037, 0.5209,
			# 501.8202, 546.3453, 609.3405, 623.2287, 16.7916, 0.5539, 0.5209'
			else:
				#print(line)
				# see if current line contains relevant data
				try:
					# extract data
					x.append((float(line[1]) + float(line[5]))/2)
					y.append((float(line[2]) + float(line[6]))/2)
					size.append((float(line[3]) + float(line[7]))/2)
					time.append(int(line[0])-starttime)
					trackertime.append(int(line[0]))
				except:
					message("line '%s' could not be parsed" % line)
					continue # skip this line	
	
	# # # # #
	# return
	
	return data
