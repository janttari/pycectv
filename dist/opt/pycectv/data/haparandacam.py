#!/usr/bin/env python3
#etsii youtubevideon videostriimin osoitteen ja palauttaa sen
import subprocess, json, sys, os
url = 'https://www.youtube.com/watch?v=stIqAtXoKug' #youtube-sivun osoite
laatu=360 #laadut saa listattua: youtube-dl -J https://www.youtube.com/watch?v=stIqAtXoKug|jq .formats[].height
p = subprocess.Popen('youtube-dl -J '+ url, stdout=subprocess.PIPE, shell=True)
out, _ = p.communicate()
json_object = json.loads(out.decode())
for kohde in json_object["formats"]:
    if str(kohde["height"]) == str(laatu):
        striimi=kohde["url"]
print(striimi) #tämä on toistettavan videon osoite
