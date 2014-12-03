#!/usr/bin/env python

import sre
import urllib2
import base64
import sys
from time import *
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

def getSitePwd(url,usr,pwd):
	request = urllib2.Request(url)
	base64string = base64.encodestring('%s:%s' % (usr, pwd)).replace('\n', '')
	request.add_header("Authorization", "Basic %s" % base64string)   
	website = urllib2.urlopen(request)
	return website.read()

def getSite(url):
	request = urllib2.Request(url)
	website = urllib2.urlopen(request)
	return website.read()

def dwnldVideo(string, name, typ, force):

	if typ == "mp4":
		download_url = returnOne('type="mp4.*?.mp4', string)[16:]
	elif typ == "webm":
		download_url = returnOne('type="webm.*?.webm', string)[17:]
	else:
		print "FEHLER: Unbekannter Dateityp!\n(Abbruch)"
# 6*9
		sys.exit()
	file_name = name+"."+typ

	if path.isfile(file_name) and not force:
		print "Datei schon runtergeladen: "+file_name
	else:
		download(download_url, file_name)

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
		status = status + chr(8)*(len(status)+1)
		print status,
	
	f.close()

def beautifulCrs(crs):
	if crs == "m1":
		crs = "Mathematik_1"
	elif crs == "m2":
		crs = "Mathematik_2"
	elif crs == "ti":
		crs = "Theoretische_Informatik"
	else:
		print "\n\nACHTUNG:\nKeinen gueltigen Kurs angegeben!\n(Abbruch)"
		sys.exit()

	return crs

def beautifulSem(sem):
	if sem == "w":
		sem = "WiSe"
	elif sem == "s":
		sem = "SoSe"
	else:
		print "\n\nACHTUNG:\nKein gueltiges Semester angegeben!\n(Abbruch)"
		sys.exit()

	return sem


def genURL(jahr,sem,crs):
	if 2013 > int(jahr) or int(jahr) > 2015:
		print "\n\nACHTUNG:\nKein gueltiges Jahr angegeben!\n(Abbruch)"
		sys.exit()

	sem = beautifulSem(sem)
	crs = beautifulCrs(crs)
	
	# Beispiel: http://weitz.de/haw-videos/2014_WiSe/Mathematik_2/data.xml
	return "http://weitz.de/haw-videos/"+jahr+"_"+sem+"/"+crs+"/data.xml"


def saveComments(match, title):

	mediathek = returnOne('url=".*?"', match)
	mediathek = mediathek[5:len(mediathek)-1]

#	print "Holen der Kommentare aus der Mediathek .."
#	print "Mediathek URL: "+mediathek

	site = getSite(mediathek)
	
	anf = site.find('<div class="box-w comments clearfix">')
	end = site.find('</div> <!-- #contentWrapper -->', anf)

	if site.find("Es wurden bisher keine Kommentare abgegeben.") == -1:
		saveTxtFile("<html><head><title>"+title+"</title></head><body>"+site[anf:end+32]+"</body></html>", title+".html")
		print ".. Kommentare gespeichert..\n\n"

	else:
		print ".. keine Kommentare vorhanden ..\n"


def saveTxtFile(contend, fname):
	f = open(fname, 'wb')
	f.write(contend)
	f.close()

def meineZeit():
	lt = localtime()
	jahr, monat, tag, stunde, minute, sekunde = lt[0:6]
	return str(jahr)+"."+str(monat)+"."+str(tag)+" - "+str(stunde)+":"+str(minute)+":"+str(sekunde)











