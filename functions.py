#!/usr/bin/env python

import sre
import urllib2
import base64
import sys
from os import path, mkdir, chdir

def newDirCh(name):
	if path.exists(name):
		chdir(name)
	else:
		mkdir(name)
		chdir(name)

def returnOne(regex, string):
	data  = sre.findall(regex, string)
	for value in data:
		return value

def mp4s(string):
	return returnOne('type="mp4.*?.mp4', string)[16:]

def webms(string):
	return returnOne('type="webm.*?.webm', string)[17:]

def getSite(url,usr,pwd):
	request = urllib2.Request(url)
	base64string = base64.encodestring('%s:%s' % (usr, pwd)).replace('\n', '')
	request.add_header("Authorization", "Basic %s" % base64string)   
	website = urllib2.urlopen(request)
	return website.read()

def download(url, file_name):
	u = urllib2.urlopen(url)
	f = open(file_name, 'wb')
	meta = u.info()
	file_size = int(meta.getheaders("Content-Length")[0])
	print "Es Wird herunter geladen : %s Bytes: %s" % (file_name, file_size)

	file_size_dl = 0
	block_sz = 8192
	while True:
		buffer = u.read(block_sz)
		if not buffer:
			break
	
		file_size_dl += len(buffer)
		f.write(buffer)
		status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
		# 6*9
		status = status + chr(8)*(len(status)+1)
		print status,
	
	f.close()

def genURL(jahr,sem,crs):
	if 2013 > int(jahr) or int(jahr) > 2015:
		print "\n\nACHTUNG:\nKein gueltiges Jahr angegeben!\n(Abbruch)"
		sys.exit()

	if sem == "w":
		sem = "WiSe"
	elif sem == "s":
		sem = "SoSe"
	else:
		print "\n\nACHTUNG:\nKein gueltiges Semester angegeben!\n(Abbruch)"
		sys.exit()

	if crs == "m1":
		crs = "Mathematik_1"
	elif crs == "m2":
		crs = "Mathematik_2"
	elif crs == "ti":
		crs = "Theoretische_Informatik"
	else:
		print "\n\nACHTUNG:\nKeinen gueltigen Kurs angegeben!\n(Abbruch)"
		sys.exit()
	
	# Beispiel: http://weitz.de/haw-videos/2014_WiSe/Mathematik_2/data.xml
	return "http://weitz.de/haw-videos/"+jahr+"_"+sem+"/"+crs+"/data.xml"











