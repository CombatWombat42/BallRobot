import Motor
import ReadIMU
import TransformXYRotZToMotor
import Queue
from time import sleep
import Globals
import TelemetryHandler
import CommandHandler
import socket
import threading

TCP_IP = ""
TCP_PORT = 5005


def TcpHandler():
    while 1:
        print "Entered tcp handler"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)

        conn, addr = s.accept()
        print 'Connection address:', addr
        myTelemetryHandler = TelemetryHandler.TelemetryHandler(Motor1TlmQueue, Motor2TlmQueue, Motor3TlmQueue, IMUTlmQueue , NotificationQueue, conn,debug=False)
        myCommandHandler= CommandHandler.CommandHandler(CommandQueue,conn)
        myTelemetryHandler.daemon = True
        myCommandHandler.daemon = True
        myTelemetryHandler.start()
        myCommandHandler.start()
        while(myTelemetryHandler.isAlive() and myCommandHandler.isAlive()):
            sleep(2)
            print "telem and command threads alive"
        


tcpThread = threading.Thread(target=TcpHandler)
tcpThread.daemon = True
tcpThread.start()

Motor1TlmQueue = Queue.Queue(maxsize=10)
Motor2TlmQueue = Queue.Queue(maxsize=10)
Motor3TlmQueue = Queue.Queue(maxsize=10)
IMUTlmQueue = Queue.Queue(maxsize=10)
NotificationQueue = Queue.Queue(maxsize=20)
CommandQueue = Queue.Queue(maxsize=10)

XQueue = Queue.Queue(maxsize=4)
YQueue = Queue.Queue(maxsize=4)

myMotor0 = Motor.Motor("P9_14","P9_12",True,0,5000,Motor1TlmQueue,NotificationQueue,period = 0.02,filterDepth = 2, debug= False)
myMotor1 = Motor.Motor("P9_22","P9_18",True,1,5000,Motor2TlmQueue,NotificationQueue,period = 0.02,filterDepth = 2, debug= False)
myMotor2 = Motor.Motor("P8_13","P8_11",True,2,5000,Motor3TlmQueue,NotificationQueue,period = 0.02,filterDepth = 2, debug= False)

myIMU = ReadIMU.ReadIMU(0x53,"FAKE",XQueue,YQueue,IMUTlmQueue,NotificationQueue,maxIMUVal = 256.0,period=0.02,debug = False)


myMotor0.daemon = True
myMotor1.daemon = True
myMotor2.daemon = True
myIMU.daemon = True


myMotor0.start()
myMotor1.start()
myMotor2.start()
myIMU.start()

i = 0 
while 1:
    #    speed = input('Enter motor speeds seperated by commas: ')
    #    speedList = str(speed).split(",")
    #    for i in speedList.length():
    #        speedList[i] = float(speedList[i])
    #try:
    speedList = TransformXYRotZToMotor.TransformXYRotZToMotor(XQueue.get(),YQueue.get(),0,debug = False)
    myMotor0.set_speed((speedList[0]))
    myMotor1.set_speed((speedList[1]))
    myMotor2.set_speed((speedList[2]))
        #    print "setting speeds to " + str(speedList[0]) + "," + str(speedList[1]) + "," + str(speedList[2])
    i = i + 1    
    #except KeyboardInterrupt:
    #s.close()
    #    print "done"
    #    exit()
