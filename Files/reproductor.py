#pyuic5.exe -x plotter.ui -o plotter.py

#se importan las librerias
import os
import sys
import time
import eyed3

from PyQt5 import QtGui, QtCore
from mp3 import *
from pygame import *
import pygame

#import for Class for serial com
from serialThreadFile import serialThreadClass

from oled import OLED
from oled import Font
from oled import Graphics

# connect to the display on /dev/i2c-0
dis = OLED(1)

# start communication with OLED
dis.begin()

#start initialization
dis.initialize()

# additional configuration
dis.set_memory_addressing_mode(0)
dis.set_column_address(0,127)
dis.set_page_address(0,7)

# clear display
dis.clear()

# set font scae x2
f = Font(2)

pygame.mixer.init()
pygame.display.init()

#se crea la lista y se agregan las canciones
playlist = []
playlist.append ( "[9] CJ - Whoopty.mp3" )
playlist.append ( "[8] ACDC - Highway To Hell.mp3" )
playlist.append ( "[7] Bee Gees - Stayin' Alive.mp3" )
playlist.append ( "[6] OneRepublic - Secrets.mp3" )
playlist.append ( "[5] Panic! at the Disco - High Hopes.mp3" )
playlist.append ( "[4] Simple Plan - Perfect.mp3" )
playlist.append ( "[3] The Goo Goo Dolls - Iris.mp3" )
playlist.append ( "[2] Masked Wolf - Astronaut In The Ocean.mp3" )
playlist.append ( "[1] Coldplay - Yellow.mp3" )
playlist.append ( "[0] Jaden - Rainbow Bap.mp3" )

# Lista de numeros 0 - 100
a_list = []
for i in range(100):
    a_list.append(str(i))

class Ui_MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)    
        
    # para la comunicacion serial
        self.mySerial = serialThreadClass()
        self.mySerial.msj.connect(self.serAct) # Recibe dato -> realiza accion deseada
        self.mySerial.start() # run thread for receive
	
	#se agregan las canciones al widget de lista
        for i in playlist:
            pos = 0
            self.listWidget.insertItem(pos,i)
            pos += 1
	
	#se establece por default al primer item
        self.listWidget.setCurrentRow(0)
        self.lineEdit.setReadOnly(True)
        #------------------------------------
        
	#botones y acciones a realizar
        self.listWidget.itemClicked.connect(self.playSong)
        self.playpButton.clicked.connect(self.playPause)
        self.stopButton.clicked.connect(self.stopSong)
        self.nextButton.clicked.connect(self.nextSong)
        self.prevButton.clicked.connect(self.prevSong)
	
    # Cada vez que se de un click cualquier item de la lista, se reproduce esa cancion 	
    def playSong(self):
	# Se carga la cancion seleccionada y se reproduce
        song = self.listWidget.currentItem().text()[4:]
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
	
	# Se muestran los datos de la cancion en reproduccion
        audiofile = eyed3.load(song)
        album_n = ''.join(map(str,audiofile.tag.track_num))
        self.lineEdit.setText("")
        self.lineEdit.setText(audiofile.tag.artist + " - " + audiofile.tag.title + " | " + audiofile.tag.album + " - " + album_n[0])
        # se imprimen en el OLED
        dis.clear()
        f.scale = 1
        f.print_string(0, 0, audiofile.tag.artist) # print artist
        f.print_string(0, 14, audiofile.tag.title) # print title
        f.print_string(0, 24, audiofile.tag.album) # print albun & albun No.
        dis.update()                               # send video buffer to display
        dis.deactivate_scroll()

    # Verifica el estatus de la cancion y se reproduce o pausa segun el status
    def playPause(self):
        self.status = pygame.mixer.music.get_busy()
        if self.status:
            pygame.mixer.music.pause()
        if not self.status:
            pygame.mixer.music.unpause()
        self.status = not self.status

    # Se para la reproduccion de la cancion actual
    def stopSong(self):
        pygame.mixer.music.stop()

    # Se reproduce la siguiente cancion dentro de la lista
    def nextSong(self):
        self.listWidget.setCurrentRow(self.listWidget.currentRow()+1)
        self.playSong()

   # Se reproduce la cancion anterior en la lista
    def prevSong(self):
        self.listWidget.setCurrentRow(self.listWidget.currentRow()-1)
        self.playSong()
    
    # Accion de acuerdo al serial
    def serAct(self):
        myDat = self.mySerial.serDat
        #self.textEdit.append(myDat)
        
        if myDat in a_list:
            self.textEdit.append("Track: " + myDat)
            self.listWidget.setCurrentRow(int(myDat))
            self.playSong()
            
        if myDat == 'A':
            self.textEdit.append("Play/Pause")
            self.playPause()
            
        if myDat == 'B':
            self.textEdit.append("Stop Song")
            self.stopSong()
        
        if myDat == 'C':
            self.textEdit.append("Next Song")
            self.nextSong()
        
        if myDat == 'D':
            self.textEdit.append("Previous Song")
            self.prevSong()


if __name__ == "__main__":
    
    #while arduino.is_open:
    
    app = QtWidgets.QApplication([])
    window = Ui_MainWindow()
    window.show()
    app.exec_()
                
        
        
