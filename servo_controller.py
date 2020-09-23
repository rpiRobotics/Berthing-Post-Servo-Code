# Servo Controller
# David Carabis

from Adafruit_PWM_Servo_Driver import PWM
import time

class servoController_imp:
    def __init__(self,servo_val):
        self.servo_val = [150,150]
    def setServo(self,channel,pulse,servoMin,servoMax,pwm):
        if pulse<servoMin:
            pulse = servoMin
        elif pulse > servoMax:
            pulse = servoMax
        self.servo_val[channel] = pulse
        pwm.setPWM(channel,0,pulse)


def setServoPulse(channel,pulse):
    pulseLength = 1000000
    pulseLength /= 60
    print "%d us per period" % pulseLength
    pulseLength /= 4096
    print "%d us per bit" % pulseLength
    pulse *=1000
    pulse /= pulseLength
    pwm.setPWM(channel,0,pulse)


def main():
    pwm = PWM(0x40)
    servoMin = 150
    servoMax = 600
    pwm.setPWMFreq(60)
    servoController = servoController_imp([servoMin,servoMin])
    pwm.setPWM(0,0,servoMin)
    pwm.setPWM(1,0,servoMin)
    time.sleep(2)
    print("Welcome to Servo Controller")

   

    print("Servo Settings:")
    print(servoController.servo_val[0])
    print(servoController.servo_val[1])

    time.sleep(3)
    pulse = 400
    channel = 0
    print(pulse)
    print(channel)
    servoController.setServo(channel,pulse,servoMin,servoMax,pwm)
    time.sleep(1)
    channel = 1
    print(channel)
    servoController.setServo(channel,pulse,servoMin,servoMax,pwm)
    time.sleep(1)
    print("Servo Settings:")
    print(servoController.servo_val[0])
    print(servoController.servo_val[1])
    
    

if __name__=='__main__':
    main()
