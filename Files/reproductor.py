#pyuic5.exe -x plotter.ui -o plotter.py

# Required libraries
import os
import sys
import time
import eyed3

from PyQt5 import QtGui, QtCore
from mp3 import *
from pygame import *
import pygame

# Import Class for serial communication with Arduino
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

# Playlist is created so as song files added
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

# Number list 0-100
a_list = []
for i in range(100):
    a_list.append(str(i))

class Ui_MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)    
        
    # Receive and send serial data in order to do something
        self.mySerial = serialThreadClass()
        self.mySerial.msj.connect(self.serAct) # Rec data -> do something
        self.mySerial.start() # run thread for receive
	
	# Songs are added to playlist widget
        for i in playlist:
            pos = 0
            self.listWidget.insertItem(pos,i)
            pos += 1
	
	# First item as default
        self.listWidget.setCurrentRow(0)
        self.lineEdit.setReadOnly(True)
        #------------------------------------
        
	# Buttons events
        self.listWidget.itemClicked.connect(self.playSong)
        self.playpButton.clicked.connect(self.playPause)
        self.stopButton.clicked.connect(self.stopSong)
        self.nextButton.clicked.connect(self.nextSong)
        self.prevButton.clicked.connect(self.prevSong)
	
    # Whenever an iten in the list is clicked, that song will play 	
    def playSong(self):
	# Load selected file and reproduce it
        song = self.listWidget.currentItem().text()[4:]
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
	
	# Song info is displayed in the GUI
        audiofile = eyed3.load(song)
        album_n = ''.join(map(str,audiofile.tag.track_num))
        self.lineEdit.setText("")
        self.lineEdit.setText(audiofile.tag.artist + " - " + audiofile.tag.title + " | " + audiofile.tag.album + " - " + album_n[0])
        
        # Song info is displayed in the OLED
        dis.clear()                                # clear dispplay
        f.scale = 1                                # set text scale to 1
        f.print_string(0, 0, audiofile.tag.artist) # print artist
        f.print_string(0, 14, audiofile.tag.title) # print title
        f.print_string(0, 24, audiofile.tag.album) # print albun & albun No.
        dis.update()                               # send video buffer to display
        dis.deactivate_scroll()                    # diable scroll functino

    # Check song status and play/pause it
    def playPause(self):
        self.status = pygame.mixer.music.get_busy() # check song is playing or paused
        if self.status:                             # if playing -> pause
            pygame.mixer.music.pause()
        if not self.status:                         # if paused -> play
            pygame.mixer.music.unpause()
        self.status = not self.status               # update status

    # Stop current song
    def stopSong(self):
        pygame.mixer.music.stop()

    # Plays next song in the playlist
    def nextSong(self):
        self.listWidget.setCurrentRow(self.listWidget.currentRow()+1) # move 1 pos forward in list
        self.playSong()

   # Plays previous song in the playlist
    def prevSong(self):
        self.listWidget.setCurrentRow(self.listWidget.currentRow()-1) # move 1 pos backward in list
        self.playSong()
    
    # Do somehting according to data received
    def serAct(self):
        myDat = self.mySerial.serDat # myDat -> serial received data
        
        # Number input (0 - 100) 
        if myDat in a_list:
            self.textEdit.append("Track: " + myDat)   # show input in the GUI
            self.listWidget.setCurrentRow(int(myDat)) # set playlist pos to number input 
            self.playSong()                           # call play function
        
        # Play/Pause song
        if myDat == 'Play' or myDat == "Pause":
            self.textEdit.append("Play/Pause") # show input in the GUI
            self.playPause()                   # call play/pause function
        
        # Stop current song
        if myDat == "Stop":
            self.textEdit.append("Stop Song") # show input in the GUI
            self.stopSong()                   # call stop function
        
        # Play next song in playlist
        if myDat == "Next Song":
            self.textEdit.append("Next Song") # show input in the GUI
            self.nextSong()                   # call nextSong function
        
        # Play previous song in playlist
        if myDat == "Prev Song":
            self.textEdit.append("Previous Song") # show input in the GUI
            self.prevSong()                       # call prevSong function
            
        # else do nothing
        else:
            pass


if __name__ == "__main__":
    
    # Initialize everything and reproduce it    
    app = QtWidgets.QApplication([])
    window = Ui_MainWindow()
    window.show()
    app.exec_()
                
        
        
