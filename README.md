# pycectv
  
![](https://raw.githubusercontent.com/janttari/pycectv/main/doc/paaikkuna.png)
  
![](https://raw.githubusercontent.com/janttari/pycectv/main/doc/elokuvalista.png)
  

pycectv on yksinkertainen television kaukosäätimellä (HDMI-CEC) ohjattava IPTV-toistin Raspberry Pi:lle.
  
### Imageksi suositellaan Raspberry Pi OS with desktop

    #Paneelin piilotus:
    ~/.config/lxpanel/LXDE-pi/panels/panel
    autohide=1
    heightwhenhidden=0
    
    
  
### Asenna pycectv ja riippuvuudet:  

    sudo apt update
    sudo apt install -y python3-pip python3-pyqt5 jq vlc cec-utils unclutter omxplayer
    sudo apt purge -y youtube-dl
    sudo pip3 install cec python-vlc youtube-dl
    wget https://github.com/janttari/pycectv/raw/main/pycectv2.deb
    sudo dpkg -i pycectv2.deb
  

  

konfiguroi kanavat tiedostoon **/opt/pycectv/kanavat.conf**  
  
Kuvakkeet ja skriptit tulee olla hakemistossa **/opt/pycectv/data/**  

Ohjelman käynnistys:
  
    sudo systemctl start pycectv

Ohjelman sammutus:  
  
    sudo systemctl stop pycectv


Automaattinen käynnistys päälle:  
  
    sudo systemctl enable pycectv

Automaattinen käynnistys pois päältä:
  
    sudo systemctl disable pycectv


-------
**/opt/pycectv/kanavat.conf**

 nimi|kuva|tyyppi|parametrit  
  
 nimi = kanavalistalla näkyvä nimi  
  
 kuva = kanavalistalla näkyvä kuvake  
 

 tyyppi:  
 play   ;sisäisellä VLC-soittimella soitettava striimi  
 geturl ;sisäisellä VLC-soittimella soitettava striimi. Striimin osoite haetaan ulkoiselta ohjelmalta  
 e2movie;enigma2-boksin elokuvalista
 exec   ;suoritettava skripti (parametreinä url, käyttäjänimi ja salasana ks esimerkki [konffitiedostosta](dist/opt/pycectv/kanavat.conf)  
 quit   ;lopettaa ohjelman suorituksen  
   
 parametrit = soittimelle välitettävä url ja muut parametrit. Tarvittaessa erottele |-merkillä.  
  
 Kanavan voi kommentoida pois käytöstä rivin alkuun lisättävällä #-merkillä    
 
-------
  
TODO:  
- pikakelaus kuntoon
- virhetilanteiden hallinta
  

  

  
  
  


