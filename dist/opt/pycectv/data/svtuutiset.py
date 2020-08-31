#!/usr/bin/env python3
#sudo apt install -y  jq
#etsii uusimman svt:n suomenkielisen uutislähetyksen urlin
import subprocess, json, sys, os
komento='''youtube-dl -g 'https://www.svtplay.se/uutiset'|grep http|head -n 1'''
p = subprocess.Popen(komento, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
url, err = p.communicate()

print(url.decode())
