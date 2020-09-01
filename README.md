# pycectv
  
![](https://raw.githubusercontent.com/janttari/pycectv/main/doc/paaikkuna.png)
  

pycectv on yksinkertainen television kaukosäätimellä (HDMI-CEC) ohjattava IPTV-toistin Raspberry Pi:lle.
  
Asennus:

    sudo apt update
    # sudo apt install -y lxqt lightdm # (jos Raspberry Pi OS lite pohjana ilman graafista työpöytää)  
    # sudo rm /etc/systemd/system/default.target && sudo ln -s /lib/systemd/system/graphical.target /etc/systemd/system/default.target #työpöytä automaattisesti käyntiin
    sudo apt install -y python3-pip python3-pyqt5 jq vlc
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
 exec   ;suoritettava skripti  
 quit   ;lopettaa ohjelman suorituksen  
  
 parametrit = soittimelle välitettävä url ja muut parametrit. Tarvittaessa erottele |-merkillä.  
  
 Kanavan voi kommentoida pois käytöstä rivin alkuun lisättävällä #-merkillä    
 
-------
  
TODO:  
  

  

  
  
  


