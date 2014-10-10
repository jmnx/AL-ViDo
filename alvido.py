#!/usr/bin/env python

import sre
import sys

from os import path, mkdir, chdir

print "\nAL ViDo v0.1\n\nAutomatic Lecture Video Downloader\n\nBitte beachtet, dass ihr die Videos nicht weiter geben duerft!\n\n"

print "Die Benutzung dieses Skripts geschiet auf eigenes Risiko, fuer Schaeden an Hard- oder Software wird keine Haftung uebernommen."

#haftung  = raw_input("Vestanden [j/n] : ")
#haftung  = "j"

#if haftung != "j" :
#	sys.exit()

# Die Datei user_data.py befindet sich nicht mit im Repository
# Sie wird beim ersten ausfuehren des Skripts erstellt und das Skript wird abgebrochen
# Bitte ergaenzen sie die Datei um die von Weitz erhaltenen Nutzerdaten

if path.isfile("user_data.py"):
	print "Nutzerdaten gefunden!\n"
else:
	saveTxtFile("#!/usr/bin/env python\n\n# Zugangs-Daten:\nusr = 'xxx'\npwd = 'xxx'", "user_data.py")
	
	print "ACHTUNG:\n\tNutzerdaten wurden nicht gefunden!\n\tEine entsprechende Datei(user_data.py) wurde erstellt.\n\tBitte ergaenze diese, bevor Du das Skript neu startetest!\n(Abbruch)"
	sys.exit()

from user_data import *

if usr == 'xxx' or pwd == 'xxx':
	print "ACHTUNG:\n\tNutzerdaten wurden nicht gefunden!\n\tEine entsprechende Datei(user_data.py) wurde erstellt.\n\tBitte ergaenze diese, bevor Du das Skript neu startetest!\n(Abbruch)"
	sys.exit()

from functions import *


if path.isfile("setup.py"):

	from setup import *
# 6*9
	print "Setup-Datei gefunden und eingebunden."

else:
	print "Welches Datei Format moechtest du haben?"
	typ  = raw_input("[webm/mp4] : ")
	print "Kommentare Speichern?"
	cmt = "j"

	print "In welchem Jahr hat das Semester angefangen?"
	year = raw_input("z.B. 2014 : ")

	print "Winter- oder Sommersemester?"
	sem  = raw_input("[w/s] : ")

	print "Welches Fach moechtest du runterladen?"
	crs  = raw_input("[m1/m2/ti] : ")

	print "Moechtest du deine Eingabe in einer Setup-Datei speichern?"
	savesetup = raw_input("[j/n] : ")

	if savesetup == "j":
		savesetup = '#!/usr/bin/env python\n\ntyp  = "'+typ+'"\ncmt  = "'+cmt+'"\nyear = "'+year+'"\nsem  = "'+sem+'"\ncrs  = "'+crs+'"'

		saveTxtFile(savesetup, "setup.py")
		print "Setup erstellt, beim naechsten starten des Skripts werden die Fragen nicht wieder gestellt."



newDirCh(beautifulCrs(crs))


website_html = getSitePwd(genURL(year,sem,crs),usr,pwd)


matches = sre.findall('<video xmlns:xsi=.*?<\/video>', website_html)

for match in matches:

	title = returnOne('title=".*?"',match)
	datum = title[10:20]
	name  = title[21:len(title)-1]
	
	newDirCh(datum)

	print "\n---> "+year+" "+beautifulSem(sem)+" "+beautifulCrs(crs)+" Datum: "+datum+" Name: "+name

	#Kommentare
	if cmt == "j":	
		saveComments(match, name)
	
	dwnldVideoIfNExist(match, name, typ)

	chdir("..")

	print "==============================================================="




