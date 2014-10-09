#!/usr/bin/env python

import sre
import sys

from os import path, mkdir, chdir

print "\nAL ViDo v0.1\n\nAutomatic Lecture Video Downloader\n\nBitte beachtet, dass ihr die Videos nicht weiter geben duerft!\n\n"

print "Die Benutzung dieses Skripts geschiet auf eigenes Risiko, fuer Schaeden an Hard- oder Software wird keine Haftung uebernommen."

#haftung  = raw_input("Vestanden [j/n] : ")
haftung  = "j"

if haftung != "j" :
	sys.exit()

# Die Datei user_data.py befindet sich nicht mit im Repository
# Sie wird beim ersten ausfuehren des Skripts erstellt und das Skript wird abgebrochen
# Bitte ergaenzen sie die Datei um die von Weitz erhaltenen Nutzerdaten

if path.isfile("user_data.py"):
	print "Nutzerdaten gefunden!\n"
else:
	saveTxtFile("#!/usr/bin/env python\n\n# Zugangs-Daten:\nusr = ''\npwd = ''", "user_data.py")
	
	print "ACHTUNG:\nNutzerdaten wurden nicht gefunden!\nEine entsprechende Datei(user_data.py) wurde erstellt.\nBitte ergaenze diese, bevor Du das Skript neu startetest!\n(Abbruch)"
	sys.exit()

# Benutzerdaten werden importiert
from user_data import *

from functions import *


if path.isfile("setup.py"):
	from setup import *
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
		mediathek = returnOne('url=".*?"', match)
		print "Mediathek URL: "+mediathek[5:len(mediathek)-1]

		comment = getComments(mediathek[5:len(mediathek)-1], year+" "+sem+" "+crs+" - "+datum+" - "+name)
		
		if comment != "false" :
			saveTxtFile(comment, name+".html")
		else:
			print "zu diesem Video sind keine Kommentare vorhanden!"


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




