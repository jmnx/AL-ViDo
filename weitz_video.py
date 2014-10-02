#!/usr/bin/env python

import sre
import urllib2
import base64
import sys
from os import path, mkdir, chdir

# Die Datei user_data.py befindet sich nicht mit im Repository
# Sie wird beim ersten ausfuehren des Skripts erstellt und das Skript wird abgebrochen
# Bitte ergaenzen sie die Datei um die von Weitz erhaltenen Nutzerdaten

if path.isfile("user_data.py"):
	print "Nutzerdaten gefunden!"
else:
	usdata = open("user_data.py", 'wb')
	usdata.write("#!/usr/bin/env python\n\n# Zugangs-Daten:\nusr = ''\npwd = ''")
	usdata.close()
	
	print "ACHTUNG:\nNutzerdaten wurden nicht gefunden!\nEine entsprechende Datei(user_data.py) wurde erstellt.\nBitte ergaenzen Sie diese!\n"
	sys.exit()

# Benutzerdaten werden importiert
from user_data import *

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
	print "Downloading: %s Bytes: %s" % (file_name, file_size)

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


# URL zur XML-Datei:
url = "http://weitz.de/haw-videos/2014_WiSe/Mathematik_2/data.xml"
# "mp4" oder "webm"
typ = "webm"
# Faecher
crs = "m2"
# Semester
sem = "2014_WiSe"


newDirCh(crs)

website_html = getSite(url,usr,pwd)

matches = sre.findall('<video xmlns:xsi=.*?<\/video>', website_html)

for match in matches:

	#ACHTUNG: Diese Felder funktionieren momentan moeglicherweise nur bei M1 & M2! Und muessen eventuell angepasst werden.
	title = returnOne('title=".*?"',match)
	datum = title[10:20]
	name  = title[21:len(title)-1]
	
	newDirCh(datum)

	if typ == "mp4":
		dwnld_url = mp4s(match)
	elif typ == "webm":
		dwnld_url = webms(match)
	else:
		print "FEHLER: Unbekannter Dateityp!"
		break
	
	dateiname = name+"."+typ

	if path.isfile(dateiname):
		print "Datei schon runtergeladen: "+dateiname
	else:
		download(dwnld_url, dateiname)

	chdir("..")

	print "============================================================="








