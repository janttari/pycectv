#!/usr/bin/env python3
#sudo apt install -y  jq
#
# Etsii GTRK karjalan uusimman videostriimin ja palauttaa sen
import subprocess, json, sys, os
laatu=360
komento='''youtube-dl -j --flat-playlist https://www.youtube.com/playlist?list=PLoW-0xF9FLAyYzWFjMZ5QJ5Yy7tthvv0S |jq -r '"\(.url)|\(.title)"'|uniq|tail -n 1'''
p = subprocess.Popen(komento, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
out, err = p.communicate()
video, otsikko=out.decode().split("|")
url = 'https://www.youtube.com/watch?v='+video

p = subprocess.Popen('youtube-dl -J '+url, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
out, err = p.communicate()
json_object = json.loads(out.decode())
for kohde in json_object["formats"]:
    if str(kohde["height"]) == str(laatu):
        striimi=kohde["url"]
print(striimi)
