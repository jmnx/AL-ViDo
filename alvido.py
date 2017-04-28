#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import json
from os import path, makedirs
from requests import get
from urllib.request import urlopen


sep = "=============================================================== <<o>>"


class Alvido(object):
    __data = {
        "m1": "Mathematik_1",
        "m2": "Mathematik_2",
        "ti": "Theoretische_Informatik",
        "mi": "Ausgewaehlte_Themen_der_Medieninformatik",
        "dd": "",
        "ra": "Relationale_Algebra",

        "w": "WiSe",
        "s": "SoSe",

        "mp4": "video/mp4",
        "webm": "video/webm"
    }

    __os = ""
    __url = "https://indexer.blackpinguin.de/"
    __login = False

    __tables = []

    def __init__(self, setupDir):
        print("\n  ▄▄▄       ██▓  ██▒   █▓ ██▓▓█████▄  ▒█████  ")
        print("  ▒████▄    ▓██▒ ▓██░   █▒▓██▒▒██▀ ██▌▒██▒  ██▒")
        print("  ▒██  ▀█▄  ▒██░  ▓██  █▒░▒██▒░██   █▌▒██░  ██▒")
        print("  ░██▄▄▄▄██ ▒██░   ▒██ █░░░██░░▓█▄   ▌▒██   ██░")
        print("   ▓█   ▓██▒░██████▒▒▀█░  ░██░░▒████▓ ░ ████▓▒░")
        print("   ▒▒   ▓▒█░░ ▒░▓  ░░ ▐░  ░▓   ▒▒▓  ▒ ░ ▒░▒░▒░ ")
        print("    ▒   ▒▒ ░░ ░ ▒  ░░ ░░   ▒ ░ ░ ▒  ▒   ░ ▒ ▒░ ")
        print("    ░   ▒     ░ ░     ░░   ▒ ░ ░ ░  ░ ░ ░ ░ ▒  ")
        print("        ░  ░    ░  ░   ░   ░     ░        ░ ░  ")
        print("                      ░        ░                v0.2")
        print("\n\n  Automatic Lecture Video Downloader")
        print("\n\n  Bitte beachtet, dass ihr die Videos nicht weiter geben duerft!")

        print("\n  Die Benutzung dieses Skripts geschiet auf eigenes Risiko, fuer Schaeden an Hard- oder Software wird keine Haftung uebernommen.\n")

        self.__setupDir = setupDir

        jsonSetup = self.__loadSetup(setupDir + "Setup.json")
        self.__courses = jsonSetup["courses"]
        self.__os = jsonSetup["os"]

        with open(setupDir + "DataSource.json") as jDataSrc:
            dsKey = jsonSetup["dataSource"]
            dataSource = json.load(jDataSrc)[dsKey]
            self.__url = dataSource["baseUrl"]
            self.__login = dataSource["login"]

        self.__conn = sqlite3.connect(setupDir + jsonSetup["database"])

    ##
    # Process Data
    ##

    def getAndProcessData(self):
        self.__jsn = self.getJsonData(self.__url + "data.json")

        for layer in self.__jsn["layers"]:
            self.__aLayer(layer, "  ", ("json", ))
            self.__conn.commit()

    def setup(self):
        for s in self.__courses:
            # print(s)
            kurs = self.__data[s['course']]
            semester = str(s['year']) + "_" + self.__data[s['semester']]
            # TODO : Comments
            comments = s['comments']
            fformat = self.__data[s['mediatype']]

            cur = self.__conn.cursor()
            key = (semester,)
            cur.execute('SELECT * FROM ' + kurs + ' WHERE sem=? ', key)
            result = cur.fetchall()

            for r in result:
                print("\n" + sep + "\n")
                json_data = json.loads(r[5])

#                print(str(r).encode("utf-8"))
#                print(type(self.__setupDir))
#                print(type(kurs))
#                print(type(semester))
#                print(type(r[2].encode("utf-8")))

                file_name = self.__setupDir + kurs + "/" + semester + "/" + r[2] + "/"

                # file_name = str(file_name.encode("utf-8"))

                if not path.isdir(file_name):
                    makedirs(file_name)

                file_name += r[4] + "." + s['mediatype']

                beding1 = path.isfile(file_name)
                beding2 = r[6] != "Nope"

                if beding1 and beding2:
                    print("Datei schon runtergeladen: " + file_name)
                else:
                    files = json_data["files"]
                    download_url = ""
                    for f in files:
                        if f['type'] == fformat:
                            download_url = f['url']
                            tmp_fformat = fformat
                            break
                    if download_url == "":
                        download_url = files[0]['url']
                        tmp_fformat = files[0]['type']

                    self.download(download_url, file_name)
                    cur.execute('UPDATE ' + kurs + ' SET downloaded=? WHERE datum=? ',
                                (tmp_fformat, r[2]))
                    self.__conn.commit()
                    print("\n  [Done]")

            print("\n\n" + sep)

    ##
    # Helper Methods
    ##

    def getJsonData(self, url):
        r = get(url)
        text = r.text
        text = text.replace("\"Russische Bauernmultiplikation\"", "Russische Bauernmultiplikation")
        pos = text.find("M1 2016-12-12 04")
        text = text[:pos + 17] + "Grosse" + text[pos + 24:]
        jsn = json.loads(text)

        return jsn

    def __aLayer(self, data, preText, path):

        path += (data['dirName'], )

        if data['videos']:
            for video in data['videos']:
                self.__insertVideo(path, video)

        if data['layers']:
            for a in data['layers']:
                self.__aLayer(a, preText + "  ", path)

    def __insertVideo(self, data, video):

        fach = data[2]
        fach = fach.replace("+C3+A4", "ae").replace("+C3+BC", "ue")

        # and a[2] in ["Dies_und_Das", "Relationale_Algebra"]:
        if data[1] in ["Sonstiges", "Semester+C3+BCbergreifend"] or data[2] == "Unsortiert":
            # sonder behandlung
            # TODO
            pass
        else:
            table = fach
            if table not in self.__tables:
                cur = self.__conn.cursor()
                cur.execute("CREATE TABLE IF NOT EXISTS " + table +
                            " (fach TEXT, sem TEXT, datum TEXT, nummer INTEGER, titel TEXT, video_json TEXT, downloaded TEXT)")
                self.__tables.append(table)

            video_json = json.dumps(video)
            cutAway = video['title'].find(" ")
            cutAway = cutAway + 10 + 2  # kurs + datum + leerzeichen

            sem = data[1]
            datum = data[3]

            # TODO: replace checkIfNotExists() with SQL
            if self.__checkIfNotExists(fach, video['title']):
                # whereCl = " WHERE NOT EXISTS (SELECT * FROM " + data[2] +" )"
                cur = self.__conn.cursor()
                nr = video['title'][cutAway:cutAway + 2]

                cur.execute('INSERT INTO ' + fach + '  VALUES (?,?,?,?,?,?,?)',
                            (fach, sem, datum, nr, video['title'], video_json, "Nope"))

    def __checkIfNotExists(self, kurs, titel):
        key = (titel,)
        cur = self.__conn.cursor()
        cur.execute('SELECT * FROM ' + kurs + ' WHERE titel=? ', key)
        return cur.fetchone() is None

    def __loadSetup(self, setupFile):
        with open(setupFile) as json_data:
            return json.load(json_data)

    def download(self, url, file_name):
        u = urlopen(url)
        f = open(file_name, 'wb')

        meta = u.info()
    #   print (meta)
        file_size = int(dict(meta)["Content-Length"])
        print("Es Wird herunter geladen :")
        print("  %s Bytes: %s" % (file_name, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            finished = file_size_dl * 100. / file_size
            status = r"%10d  [%3.2f%%]" % (file_size_dl, finished)
            status = status + chr(8) * (len(status) + 1)
            print(status, end="\r")

        f.close()
