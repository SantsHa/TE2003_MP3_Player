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
playlist.append ("[100] 347aidan - Dancing in My Room.mp3")
playlist.append ("[99]  The Rolling Stones - Paint It, Black.mp3")
playlist.append ("[98]  ACDC - You Shook Me All Night Long.mp3")
playlist.append ("[97]  Adele  - Set fire to the rain.mp3")
playlist.append ("[96]  ALI - LOST IN PARADISE.mp3")
playlist.append ("[95]  Arctic Monkeys - 505.mp3")
playlist.append ("[94]  Arctic Monkeys - Do I Wanna Know.mp3")
playlist.append ("[93]  Avicii - Levels.mp3")
playlist.append ("[92]  Axwell Ingrosso - Sun Is Shining.mp3")
playlist.append ("[91]  BAD BUNNY - A TU MERCED.mp3")
playlist.append ("[90]  Bad Bunny - Si Veo a Tu Mam .mp3")
playlist.append ("[89]  Bee Gees - Stayin' Alive.mp3")
playlist.append ("[88]  Black Coast - TRNDSTTR.mp3")
playlist.append ("[87]  Black Eyed Peas - Pump It.mp3")
playlist.append ("[86]  Black Sabbath - Iron Man.mp3")
playlist.append ("[85]  BLACKPINK - How You Like That.mp3")
playlist.append ("[84]  blink-182 - All The Small Things.mp3")
playlist.append ("[83]  Bobby McFerrin - Don't Worry Be Happy.mp3")
playlist.append ("[82]  Burbank - Sorry, I Like You.mp3")
playlist.append ("[81]  BURNOUT SYNDROMES - FLY HIGH!!.mp3")
playlist.append ("[80]  Carpenters - Close To You.mp3")
playlist.append ("[79]  CeeLo Green - Forget You.mp3")
playlist.append ("[78]  Coldplay - Viva La Vida.mp3")
playlist.append ("[77]  Daft Punk - Around the world.mp3")
playlist.append ("[76]  Daft Punk - Something About Us.mp3")
playlist.append ("[75]  David GuettaVassy - Bad (Radio Edit) .mp3")
playlist.append ("[74]  Dayglow - Can I Call You Tonight.mp3")
playlist.append ("[73]  Dayglow - Hot Rod.mp3")
playlist.append ("[72]  DNCE - Cake By The Ocean.mp3")
playlist.append ("[71]  Doja Cat - Say So.mp3")
playlist.append ("[70]  DragonForce - Through The Fire And Flames.mp3")
playlist.append ("[69]  Dua Lipa - Levitating.mp3")
playlist.append ("[68]  Dua Lipa - Physical.mp3")
playlist.append ("[67]  Ed Maverick - Fuentes de Ortiz.mp3")
playlist.append ("[66]  Ed Sheeran - Thinking Out Loud.mp3")
playlist.append ("[65]  Electric Light Orchestra - Mr. Blue Sky.mp3")
playlist.append ("[64]  Eminem & Rihanna - The Monster.mp3")
playlist.append ("[63]  Europe - The Final Countdown.mp3")
playlist.append ("[62]  Eve - Kaikai Kitan.mp3")
playlist.append ("[61]  Fall Out Boy - Centuries.mp3")
playlist.append ("[60]  Fall Out Boy - Immortals.mp3")
playlist.append ("[59]  Fall Out Boy - My Songs Know What You Did In The Dark.mp3")
playlist.append ("[58]  Flo RidaSia - Wild Ones.mp3")
playlist.append ("[57]  Fun - We Are Young.mp3")
playlist.append ("[56]  George Benson - Give Me the Night.mp3")
playlist.append ("[55]  Gioachino Rossini - Rossini -William-Tel L-Trumpet-Entry.mp3")
playlist.append ("[54]  Gorillaz -On Melancholy Hill .mp3")
playlist.append ("[53]  Grover Washington JR. - Just the two of us.mp3")
playlist.append ("[52]  Imagine Dragons - Demons.mp3")
playlist.append ("[51]  Imagine Dragons - Radioactive.mp3")
playlist.append ("[50]  Intouchables - Una Mattina.mp3")
playlist.append ("[49]  J. Balvin & Bad Bunny - LA CANCIàN.mp3")
playlist.append ("[48]  JAWNY - Honeypie.mp3")
playlist.append ("[47]  Kurt - La Mujer Perfecta.mp3")
playlist.append ("[46]  Le Tigre - Deceptacon.mp3")
playlist.append ("[45]  Led Zeppelin - Stairway To Heaven.mp3")
playlist.append ("[44]  LiSA - Gurenge.mp3")
playlist.append ("[43]  lista.txt")
playlist.append ("[42]  Lost FrequenciesJanieck Devy - Reality.mp3")
playlist.append ("[41]  LP-Lost On You.mp3")
playlist.append ("[40]  Lukas Graham - 7 Years.mp3")
playlist.append ("[39]  Lynyrd Skynyrd - Sweet Home Alabama.mp3")
playlist.append ("[38]  M83 - Midnight City.mp3")
playlist.append ("[37]  Major LazerMDJ Snake - Lean On.mp3")
playlist.append ("[36]  Mariya Takeuchi - Plastic Love.mp3")
playlist.append ("[35]  Maroon 5  - Animals.mp3")
playlist.append ("[34]  Maroon 5 - One More Night.mp3")
playlist.append ("[33]  MGMT - Little Dark Age.mp3")
playlist.append ("[32]  Michael Jackson - Billie Jean.mp3")
playlist.append ("[31]  Michael W Smith - Freedom.mp3")
playlist.append ("[30]  Mother Mother - Hayloft.mp3")
playlist.append ("[29]  Mrs.GREEN APPLE - Inferno.mp3")
playlist.append ("[28]  Olivia Rodrigo - good 4 u.mp3")
playlist.append ("[27]  Post Malone, Swae Lee - Sunflower.mp3")
playlist.append ("[26]  potsu - just friends.mp3")
playlist.append ("[25]  Redbone - Come and Get Your Love.mp3")
playlist.append ("[24]  Rok Nardin - Where Is Your God Now.mp3")
playlist.append ("[23]  Rok Nardin - You Can't Kill Me.mp3")
playlist.append ("[22]  Shakira - Antolog¡a.mp3")
playlist.append ("[21]  Shakira - Suerte.mp3")
playlist.append ("[20]  Shakira - Try Everything.mp3")
playlist.append ("[19]  Sheryl Crow - Real Gone.mp3")
playlist.append ("[18]  Skillet - Monster (Album Version).mp3")
playlist.append ("[17]  Skillet - Rise.mp3")
playlist.append ("[16]  Surf Curse - Freaks.mp3")
playlist.append ("[15]  Tame Impala - Borderline.mp3")
playlist.append ("[14]  Tame Impala - The Less I Know The Better.mp3")
playlist.append ("[13]  The Beatles - Here Comes The Sun.mp3")
playlist.append ("[12]  The Chainsmokers & Coldplay - Something Just Like This.mp3")
playlist.append ("[11]  The Drums - Money.mp3")
playlist.append ("[10]  The Neighbourhood - Scary Love.mp3")
playlist.append ("[9]   CJ - Whoopty.mp3" )
playlist.append ("[8]   ACDC - Highway To Hell.mp3" )
playlist.append ("[7]   Bee Gees - Stayin' Alive.mp3" )
playlist.append ("[6]   OneRepublic - Secrets.mp3" )
playlist.append ("[5]   Panic! at the Disco - High Hopes.mp3" )
playlist.append ("[4]   Simple Plan - Perfect.mp3" )
playlist.append ("[3]   The Goo Goo Dolls - Iris.mp3" )
playlist.append ("[2]   Masked Wolf - Astronaut In The Ocean.mp3" )
playlist.append ("[1]   Coldplay - Yellow.mp3" )
playlist.append ("[0]   Jaden - Rainbow Bap.mp3" )

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
        song = self.listWidget.currentItem().text()[6:]
        # Change path according to your configuration
        mySong = "/home/pi/Desktop/RETO/TE2003_MP3_Player/Files/Songs/"+song
        pygame.mixer.music.load(mySong)
        pygame.mixer.music.play()
	
	# Song info is displayed in the GUI
        audiofile = eyed3.load(mySong)
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
                
        
        
