#!/usr/bin/env python3
#
# Yksinkertainen IPTV toistin Raspberrylle. Ohjataan TV:n kaukosäätimellä (HDMI-CEC)
#

from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime
import vlc, time, cec, os, subprocess, requests

#Kaukosäätimen CEC-komennot:
NAPIT = {1: "YLÖS", 0: "OK", 2: "ALAS", 3: "VASEN", 4: "OIKEA", 69: "STOP", 70: "PAUSE", 72: "REV", 73: "FWD", 68: "PLAY"}
FILEPATH="/opt/pycectv" #Hakemisto jossa konffi, piconit ja skriptit

class VideoWindow(QtCore.QThread, QtCore.QObject): #------------------------------------------- VIDEOSOITIN -------------------------------
    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.start()

    def setupUi(self, VideoWindow):
        self.valvoTimer = QtCore.QTimer()
        FormVideo.setStyleSheet("background-color:rgb(0, 0, 0); border: none;")
        self.sizeHint = lambda: QtCore.QSize(800, 600)
        self.videoFrame = QtWidgets.QFrame()
        self.videoFrame.setStyleSheet("background-color:green;")
        t_lay_parent = QtWidgets.QHBoxLayout()
        t_lay_parent.setContentsMargins(0, 0, 0, 0)
        self.videoFrame = QtWidgets.QFrame(VideoWindow)
        self.videoFrame.setFixedSize(QtCore.QSize(800, 600))
        t_lay_parent.addWidget(self.videoFrame)
        FormVideo.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.CustomizeWindowHint|QtCore.Qt.FramelessWindowHint)
        monitor = QtWidgets.QDesktopWidget().screenGeometry(0) #vaihda tää jos dualheadin toinen lähtö
        self.videoFrame.setFixedSize(QtCore.QSize(monitor.width(), monitor.height()))
        self.videoFrame.move(0,-1)
        self.videoFrame.setStyleSheet("border: none;")
        self.vlcInstance = vlc.Instance(['--video-on-top'])
        self.videoPlayer = self.vlcInstance.media_player_new()
        self.videoPlayer = self.vlcInstance.media_player_new()
        self.videoPlayer.video_set_mouse_input(False)
        self.videoPlayer.video_set_key_input(False)
        self.viimNahtyAika=time.time()
        self.viimNahtyKuvamaara=0
        self.videoPlayer.set_xwindow(self.videoFrame.winId())
        self.valvoTimer.setInterval(1000)
        self.valvoTimer.timeout.connect(self.valvo)

    def valvo(self): #Valvoo että VLC on pystyssä ja striimi ei ole katkennut. Tarvittaessa yhdistää uudelleen
        if self.media.get_stats(self.mediaStats):
            naytetytKuvat=(self.mediaStats.displayed_pictures) #https://github.com/oaubert/python-vlc/blob/master/examples/cocoavlc.py
            if naytetytKuvat!=self.viimNahtyKuvamaara: #jos on saatu uusia frameja
                self.viimNahtyKuvamaara=naytetytKuvat
                self.viimNahtyAika=time.time()
        if time.time()-self.viimNahtyAika >30: #On kulunut pitkään ettei ole saatu uutta dataa. Käynnistetään VLC uudelleen
            self.viimNahtyAika=time.time()
            print("***************** restart player ****************")
            self.videoPlayer.stop()
            self.videoPlayer.play()

    def seis(self):
        self.videoPlayer.stop()
        self.valvoTimer.stop()

    def toista(self, url, *param):
        self.videoPlayer.set_mrl(url, *param)
        self.videoPlayer.play()
        self.viimNahtyAika=time.time()
        self.valvoTimer.start()
        self.mediaStats = vlc.MediaStats()
        self.media = self.videoPlayer.get_media()
        self.valvoTimer.start()
        FormVideo.show()
        FormVideo.showMaximized()

class Ui_Form(QtCore.QThread, QtCore.QObject): #--------------------------------------------- PÄÄIKKUNA --------------------------------------------
    signal = QtCore.pyqtSignal([str])

    def __init__(self, parent=None):
        super(Ui_Form, self).__init__(parent)
        self.signal.connect(self.eventp)
        self.start()

    def setupUi(self, Form):
        self.kanavalista=[]
        self.nytsoi=[]
        self.laskuri=0
        self.leffaToistuu=False #kun leffa pyörii
        Form.setObjectName("Form")
        Form.resize(400, 300)
        Form.setStyleSheet("background-color:rgb(41, 85, 74); border: none;")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 10, 261, 31))
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n" "font: 26pt \"Ubuntu Mono\";")
        self.label.setObjectName("label")
        self.listWidgetKanavalista = QtWidgets.QListWidget(Form)
        self.listWidgetMovielista = QtWidgets.QListWidget(Form)
        self.listWidgetMovielista.setStyleSheet("QListView{background-color: green; font: 22pt \"Ubuntu Mono\"; color: white;}QListView::item:selected{background-color: rgb(255,0,0); color: yellow;};");
        self.listWidgetMovielista.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidgetMovielista.hide()
        #self.listWidgetKanavalista.setGeometry(QtCore.QRect(70, 70, 256, 192))
        #self.listWidgetMovielista.setGeometry(QtCore.QRect(70, 70, 256, 192))
        self.listWidgetKanavalista.setObjectName("listWidget")
        self.listWidgetKanavalista.setViewMode(QtWidgets.QListWidget.IconMode);
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.listWidgetKanavalista.setStyleSheet("QListView{font: 16pt \"Ubuntu Mono\"; color: white;}QListView::item:selected{background-color: rgb(75,153,134); color: yellow;}");
        self.listWidgetKanavalista.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.label.move(20,0)
        monitor = QtWidgets.QDesktopWidget().screenGeometry(0) # Jos useampi monitori käytössä
        self.listWidgetKanavalista.setGeometry(QtCore.QRect(100, 30, monitor.width()-100, monitor.height()-10))
        self.listWidgetMovielista.setGeometry(QtCore.QRect(100, 30, monitor.width()-100, monitor.height()-10))
        Form.move(monitor.left(), monitor.top())
        Form.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.CustomizeWindowHint|QtCore.Qt.FramelessWindowHint)
        Form.showMaximized()
        self.listWidgetKanavalista.setIconSize(QtCore.QSize(200,120))
        self.listWidgetKanavalista.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.listWidgetKanavalista.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.listWidgetKanavalista.clicked['QModelIndex'].connect(self.klikattuKanava)
        self.listWidgetKanavalista.activated['QModelIndex'].connect(self.klikattuKanava)
        self.listWidgetMovielista.clicked['QModelIndex'].connect(self.klikattuMovie)
        self.listWidgetMovielista.activated['QModelIndex'].connect(self.klikattuMovie)
        self.lueKanavat()
        self.listWidgetKanavalista.setFocus()
        self.listWidgetKanavalista.setCurrentRow(0)
        cec.add_callback(self.nappainPainettu, cec.EVENT_KEYPRESS)
        cec.init()
        self.valvoTimer = QtCore.QTimer()
        self.valvoTimer.setInterval(500)
        self.valvoTimer.timeout.connect(self.recurring_timer)
        self.valvoTimer.start()

    def nappainPainettu(self, event, *args): #cec:n callback (**1**)
        if args[1] == 0 or args[0] == 69: #painike alas #69 stop lähettää vain yhden eventin
            self.signal.emit(NAPIT[args[0]]) #lähetetään signaali --> **2*

    @QtCore.pyqtSlot(str)
    def eventp(self, arvo): #(**2**)
        self.sendKey(arvo)

    def sendKey(self, key): #(**3**)
        if key == "OIKEA":
            nappain=QtCore.Qt.Key_Right
        elif key == "VASEN":
            nappain=QtCore.Qt.Key_Left
        elif key == "ALAS":
            nappain=QtCore.Qt.Key_Down
        elif key == "YLÖS":
            nappain=QtCore.Qt.Key_Up
        elif key == "OK":
            nappain=QtCore.Qt.Key_Enter
        elif key == "STOP":
            print("stop",self.nytsoi)
            if self.nytsoi:
                if self.nytsoi[2]=="e2movie":
                    print("hide")
                    if self.leffaToistuu:
                        ui_video.seis()
                        self.leffaToistuu=False
                        FormVideo.hide()
                        Form.show()
                    else:
                        self.listWidgetKanavalista.show()
                        self.listWidgetMovielista.hide()
                        self.nytsoi=[]
                elif self.nytsoi[2]=="play" or "geturl" : # jos nykyinen soi VLC:llä:
                    ui_video.seis()
                    FormVideo.hide()
                    Form.show()
                    self.nytsoi=[]
                elif self.nytsoi[2]=="exec": # jos nykyinen on skripti
                    os.system(FILEPATH+"/data/"+self.nytsoi[3][0]+" --stop &")
                    Form.show()
                    self.nytsoi=[]
                return
            return

        event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, nappain, QtCore.Qt.NoModifier)
        if not self.nytsoi or (self.nytsoi and self.nytsoi[2] != "e2movie"):
            QtCore.QCoreApplication.sendEvent(self.listWidgetKanavalista, event)
        else:
            QtCore.QCoreApplication.sendEvent(self.listWidgetMovielista, event)
            
    def recurring_timer(self): #qt ajastin joka suoritetaan joka nnn millisekunti
        self.laskuri+=1
        self.label.setText(datetime.now().strftime('%H:%M:%S'))

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "TextLabel"))

    def klikattuKanava(self):
        kohde=self.listWidgetKanavalista.currentRow()
        self.nytsoi=self.kanavalista[kohde]
        if self.kanavalista[kohde][2] == "play": #sisäisellä VLC:llä avattava
            ui_video.toista(self.kanavalista[kohde][3][0],*self.kanavalista[kohde][3][1:])
            FormVideo.show()
        elif self.kanavalista[kohde][2] == "e2movie": #enigma2-boksin elokuvalista
            self.listWidgetKanavalista.hide()
            self.listWidgetMovielista.show()
            self.leffaIkkuna=True
            self.lataaMovielista()
        elif self.kanavalista[kohde][2] == "exec": #suoritettava skripti
            os.system(FILEPATH+"/data/"+self.kanavalista[kohde][3][0]+" --start &")
        elif self.kanavalista[kohde][2] == "quit": #poistutaan ohjelmasta
            quit()
        elif self.kanavalista[kohde][2] == "geturl": #pyytää ulkoiselta ohjelmalta striimin osoitetta
            self.label.setText("Odota...")
            app.processEvents()
            proc = subprocess.Popen(FILEPATH+"/data/"+self.kanavalista[kohde][3][0], stdout=subprocess.PIPE)
            osoite=proc.communicate()[0].decode().rstrip()
            ui_video.toista(osoite)
            Form.hide()
            FormVideo.show()

    def klikattuMovie(self):
        self.leffaToistuu=True
        kohde=self.listWidgetMovielista.currentRow()
        print(kohde, self.leffat[kohde], self.urlit[kohde])
        ui_video.toista(self.urlit[kohde])
        Form.hide()
        FormVideo.show()

        
    def lueKanavat(self):
        with open(FILEPATH+"/kanavat.conf") as fp:
            for line in fp:
                if len(line)>5:
                    if not line.startswith("#"):
                        palat = line.rstrip().split("|")
                        nimi=palat[0]
                        kuva=palat[1]
                        tyyppi=palat[2]
                        url=palat[3:]
                        self.kanavalista.append([nimi, kuva, tyyppi, url])
                        self.listWidgetKanavalista.addItem(QtWidgets.QListWidgetItem(QtGui.QIcon(FILEPATH+"/data/"+kuva),nimi))

    def lataaMovielista(self):
        self.leffat=[]
        self.urlit=[]
        urlsis="http://root:2001jape@192.168.1.12/web/movielist.m3u"
        r = requests.get(urlsis)
        sisalto=r.text.split("\n")
        for i in range(0,len(sisalto)):
            srivi=sisalto[i].rstrip()
            if srivi.startswith("#EXTINF"):
                try:
                    kanava=srivi.split(" - ")[1]
                    ohjelma=" - ".join(srivi.split(" - ")[2:])
                    url=sisalto[i+1].rstrip() #HUOM LISÄÄ KÄYTTÄJÄTUNNUS JA SALASANA!
                    a,l=url.split("://")
                    print(a,l)
                    url=a+"://root:2001jape@"+l
                    self.leffat.append(ohjelma)
                    self.urlit.append(url)
                    self.listWidgetMovielista.addItem(ohjelma)
                except:
                    pass
                    
   
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()

    FormVideo = QtWidgets.QWidget()
    ui_video = VideoWindow()
    ui_video.setupUi(FormVideo)
    
    sys.exit(app.exec_())
