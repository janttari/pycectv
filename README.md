# pycectv
  
![](https://raw.githubusercontent.com/janttari/pycectv/main/doc/paaikkuna.png)
  

pycectv on yksinkertainen television kaukosäätimellä (HDMI-CEC) ohjattava IPTV-toistin Raspberry Pi:lle.
  
Asennus:

    sudo apt install -y python3-pyqt5 python3-pip git jq
    sudo pip3 install youtube-dl python-vlc cec
    cd ~
    git clone https://github.com/janttari/pycectv.git
    cd pycectv
    ./asenna
  
Päivitys:
  
    cd ~/pycectv
    git pull
    ./asenna
  

konfiguroi kanavat tiedostoon **/home/pi/pycectv/kanavat.conf**  
  
Kuvakkeet ja skriptit tulee olla hakemistossa **/home/pi/pycectv/**  

Ohjelman käynnistys:
  
    sudo systemctl start pycectv.service

Ohjelman sammutus:  
  
    sudo systemctl stop pycectv.service


Automaattinen käynnistys päälle:  
  
    sudo systemctl enable pycectv.service

Automaattinen käynnistys pois päältä:
  
    sudo systemctl disable pycectv.service


-------
**/home/pi/pycectv/kanavat.conf**

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
-varsinainen asennus /opt ja vain konffit on /home/pi/cectv
  

  

  
  
  


