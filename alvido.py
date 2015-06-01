#!/usr/bin/env python

import sre
import sys

from os import path, mkdir, chdir, getcwd

from functions import *

# Das Skript-Verzeichnes als Arbeits-Verzeichnis setzten, falls Skript als Cron-Job ausgefuert wird ;o)
scrLocation = path.abspath(__file__)
scrLocation = scrLocation[0:scrLocation.find("alvido.py")]
chdir(scrLocation)

print "\nAL ViDo v0.1\n\nAutomatic Lecture Video Downloader\n\nBitte beachtet, dass ihr die Videos nicht weiter geben duerft!\n\n"

print "Die Benutzung dieses Skripts geschiet auf eigenes Risiko, fuer Schaeden an Hard- oder Software wird keine Haftung uebernommen.\n\n"

# ------------------------------------------------------------------------------------ Parameter
debugmode = False
nosetup = False
forceDownload = False
nocrs = False
savesetup = "n"
cronJob = False


for argument in sys.argv :
#	print "Argumnt: " +argument

	if argument == "mp4" or argument == "webm" :
		typ = argument
		nosetup = True
#		print "Fileformat: "+argument
	
	elif argument == "w" or argument == "s" :
		sem = argument
		nosetup = True
#		print "Semester: "+argument

	elif argument == "ti" or argument == "m1" or argument == "m2" :
		mcrs = argument
# 6*9
		nocrs = True
		print "\nKurs: "+argument+" -> Kursangabe wird ueberschrieben\n"

	elif argument == "2012" or argument == "2013" or argument == "2014" or argument == "2015" :
		year = argument
		nosetup = True
#		print "Jahr: "+argument

	elif argument == "save" :
		savesetup = "j"
		nosetup = True
		print "Save Setup!"

	elif argument == "force" :
		forceDownload = True
		print "Force Download! \n"

	elif argument == "cron" :
		if path.isfile("cron_setup.py"):
			from cron_setup import *
			cronJob = True
		else :
			print "ACHTUNG:\n\tCrone-Setup nicht gefunden, bitte 'crone_setup.py' erstellen!\n(Abbruch)"
			sys.exit()


# ------------------------------------------------------------------------------------ Benutzerdaten

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
#print "Nutzerdaten: "+usr+":"+pwd

if usr == 'xxx' or pwd == 'xxx':
	print "ACHTUNG:\n\tNutzerdaten wurden nicht gefunden!\n\tEine entsprechende Datei(user_data.py) wurde erstellt.\n\tBitte ergaenze diese, bevor Du das Skript neu startetest!\n(Abbruch)"
	sys.exit()

# ------------------------------------------------------------------------------------ Setup
from setup import *

if nocrs :
	crs = mcrs

# ------------------------------------------------------------------------------------ Los gehts!
if cronJob :
	chdir(workDir)
print "\nArbeitsverzeichnis: "+getcwd()+"\n"

saveTxtFile("letzer zugriff: "+meineZeit(),"zg.txt")

#print "OS ist "+os+"\n"


newDirCh(beautifulCrs(crs))

website_html = getSitePwd(genURL(year,sem,crs),usr,pwd)

matches = sre.findall('<video xmlns:xsi=.*?<\/video>', website_html)

for match in matches:

	print "\n\n =============================================================== <<o>>"

	#changed filename to be the whole title because MINF starts with 2 Letters more

	title = returnOne('title=".*?"',match)

	name = title[21:len(title)-1]

	title = title[7:len(title)-1].replace("?","")
	datum = returnOne('date=".*?"',match)
	datum = datum[6:len(datum)-1]

	if os == "win" or os == "mac":
		name  = name.replace("?","")
		
	
	newDirCh(datum)

	print "\n---> "+year+" "+beautifulSem(sem)+" "+beautifulCrs(crs)+" Datum: "+datum+" Name: "+name+"\n"

	#Kommentare
	if cmt == "j":	
		saveComments(match, name)
	
	dwnldVideo(match, name, typ, forceDownload)

	chdir("..")


print "\n\n =============================================================== <<o>>"

