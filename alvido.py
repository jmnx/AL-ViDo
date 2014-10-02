#!/usr/bin/env python

import sre
import sys

from os import path, mkdir, chdir

print "\nAL ViDo v0.1\n\nAutomatic Lecture Video Downloader\n"

# Die Datei user_data.py befindet sich nicht mit im Repository
# Sie wird beim ersten ausfuehren des Skripts erstellt und das Skript wird abgebrochen
# Bitte ergaenzen sie die Datei um die von Weitz erhaltenen Nutzerdaten

if path.isfile("user_data.py"):
	print "Nutzerdaten gefunden!\n"
else:
	usdata = open("user_data.py", 'wb')
	usdata.write("#!/usr/bin/env python\n\n# Zugangs-Daten:\nusr = ''\npwd = ''")
	usdata.close()
	
	print "ACHTUNG:\nNutzerdaten wurden nicht gefunden!\nEine entsprechende Datei(user_data.py) wurde erstellt.\nBitte ergaenze diese, bevor Du das Skript neu startetest!\n(Abbruch)"
	sys.exit()

# Benutzerdaten werden importiert
from user_data import *

from functions import *


print "Welches Datei Format moechtest du haben?"
typ  = raw_input("[webm/mp4] : ")

print "In welchem Jahr hat das Semester angefangen?"
year = raw_input("z.B. 2014 : ")
print "Winter- oder Sommersemester?"
sem  = raw_input("[w/s] : ")

print "Welches Fach moechtest du runterladen?"
crs  = raw_input("[m1/m2/ti] : ")


# 6*9

url = genURL(year,sem,crs)

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
		print "FEHLER: Unbekannter Dateityp!\n(Abbruch)"
		sys.exit()
	
	dateiname = name+"."+typ

	if path.isfile(dateiname):
		print "Datei schon runtergeladen: "+dateiname
	else:
		download(dwnld_url, dateiname)

	chdir("..")

	print "============================================================="








