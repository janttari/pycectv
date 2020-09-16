#!/usr/bin/env python3
with open("movielist.m3u", "r") as ml: # http://192.168.1.12/web/movielist.m3u #HUOM LISÄÄ KÄYTTÄJÄTUNNUS JA SALASANA!
    lista=ml.readlines()

for i in range(0,len(lista)):
    rivi=lista[i].rstrip()
    if rivi.startswith("#EXTINF"):
        try:
            kanava=rivi.split(" - ")[1]
            ohjelma=rivi.split(" - ")[2]
            url=lista[i+1].rstrip() #HUOM LISÄÄ KÄYTTÄJÄTUNNUS JA SALASANA!
        except:
            pass
        print(kanava, ohjelma, url)