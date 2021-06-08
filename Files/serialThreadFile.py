import serial
from PyQt5.QtCore import pyqtSignal,QThread

# variables
data = ""
a=[]
b=[]
c=[]
tmp=0
k=0
count=0

class serialThreadClass(QThread):
    msj = pyqtSignal(str)
    
    def __init__(self,parent=None):
        super(serialThreadClass, self). __init__(parent)
        
        self.serPort = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
#         self.serPort.baudrate = 9600
#         self.serPort.port = '/dev/ttyUSB0'
        self.serPort.flush()
        self.serDat = ""
        #self.serPort.open()
        
    def run(self): #thread run func, receive data
        while True:
            #vrfy = self.serPort.readline()
            data = self.serPort.read().decode('utf-8').rstrip()
            if data != '':
                
                self.msj.emit(str(data)) #pipe
                print(data) #print to terminal
                self.serDat=data
                
            
        
        