# Servo Test File
# Drive serovs on channels 0 and 1 to 0, then alternate servos close/open

from Adafruit_PWM_Servo_Driver import PWM
import time

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

    pwm.setPWM(0,0,servoMin)
    pwm.setPWM(1,0,servoMin)

    time.sleep(1)
    pwm.setPWM(0,0,servoMax)
    time.sleep(1)
    pwm.setPWM(1,0,servoMax)
    time.sleep(1)
    pwm.setPWM(0,0,servoMin)
    time.sleep(1)
    pwm.setPWM(1,0,servoMin)

if __name__=='__main__':
    main()
