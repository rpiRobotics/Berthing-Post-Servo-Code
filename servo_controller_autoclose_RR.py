# Servo Controller
# David Carabis

from Adafruit_PWM_Servo_Driver import PWM
import time
import RobotRaconteur as RR
import thread
import threading
import numpy

def autoClose(servocon,pwm):
    while True:
        if servocon._autoclose:
            xA = servocon._closevals[0]-servocon._servo_val[0]
            xB = servocon._closevals[1]-servocon._servo_val[1]
            if abs(xA)>abs(xB):
                x = abs(xA)
            else:
                x = abs(xB)
            for y in range(x):
                tprev = time.clock()
                if servocon._servo_val[0]!=servocon._closevals[0]:
                    servocon._servo_val[0] += 1*numpy.sign(xA)
                    pwm.setPWM(servocon._channel[0],0,servocon._servo_val[0])
                if servocon._servo_val[1]!=servocon._closevals[1]:
                    servocon._servo_val[1] += 1*numpy.sign(xB)
                    pwm.setPWM(servocon._channel[0],0,servocon._servo_val[0])
                t = time.clock()
                if (t-tprev)<servocon._closespeed:
                    time.sleep(servocon._closespeed - (t-tprev))
            servocon._autoclose = False

class servoController_imp:
    def __init__(self,servo_val,servoMin,servoMax,pwm):
        self._lock = threading.RLock()
        self._servo_val = [150,150]
	self._min = servoMin
	self._max = servoMax
	self._pwm = pwm
	self._autoclose = False
	self._closevals = [0,0]
	self._closespeed = 0.02
	self._channel = [0,0]
    def setServo(self,channel,pulse):
        if not self._autoclose:
            with self._lock:
                if pulse<self._min:
                    pulse = self._min
                elif pulse > self._max:
                    pulse = self._max
                self._servo_val[channel] = pulse
                self._pwm.setPWM(channel,0,pulse)

    def autoCloseSet(self,channelA,channelB,closevalA,closevalB,closespeed):
        self._channel[0] = channelA
        self._channel[1] = channelB
        self._closevals[0] = closevalA
        self._closevals[1] = closevalB
        self._closespeed = closespeed
        self._autoclose = True

    @property
    def servoVal(self):
        with self._lock:
            return self._servo_val



def main():
    pwm = PWM(0x40)
    servoMin = 150
    servoMax = 600
    pwm.setPWMFreq(60)
    
    RR.RobotRaconteurNode.s.NodeName = "ServoController"
    servoController = servoController_imp([servoMin,servoMin],servoMin,servoMax,pwm)

    t = RR.TcpTransport()
    t.StartServer(5252)
    RR.RobotRaconteurNode.s.RegisterTransport(t)

    autoCloseProtocol = threading.Thread(target=autoClose, args = (servoController,pwm,))
    autoCloseProtocol.setDaemon(True)
    autoCloseProtocol.start()
    
    try:
        with open('servo_controller_autoclose.robdef','r') as f:
            service_def = f.read()
    except:
	print("error1")

    try:
        RR.RobotRaconteurNode.s.RegisterServiceType(service_def)
    except:
	print("error2")
    try:
        RR.RobotRaconteurNode.s.RegisterService("servcon","edu.rpi.controller.servcon",servoController)

        print("Connect at tcp://localhost:5252/ServoController/servcon")
        raw_input("press enter to quit...\r\n")


    except:
        print("error")
    RR.RobotRaconteurNode.s.Shutdown()

    
    

if __name__=='__main__':
    main()
