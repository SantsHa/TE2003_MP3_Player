import serial
from PyQt5.QtCore import pyqtSignal,QThread

class serialThreadClass(QThread):
    msj = pyqtSignal(str)
    
    def __init__(self,parent=None):
        super(serialThreadClass, self). __init__(parent)
        
        # innit serial port
        self.serPort = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        self.serPort.flush()
        self.serDat = ""
        #self.serPort.open()
        
    def run(self): #thread run function, receive data
        while True:
            #Decode ASCII value
            data = self.serPort.readline().decode('utf-8').rstrip()
            if data != '':
                
                self.msj.emit(str(data)) #pipe
                #print(data) #print to terminal
                self.serDat=data # set serDat to data received
                
            
        
        