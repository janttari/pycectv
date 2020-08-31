# pycectv
  
![](https://raw.githubusercontent.com/janttari/pycectv/main/doc/paaikkuna.png)
  

pycectv on yksinkertainen television kaukosäätimellä (HDMI-CEC) ohjattava IPTV-toistin Raspberry Pi:lle.
  
Asennus:

  

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
  

  

  
  
  


