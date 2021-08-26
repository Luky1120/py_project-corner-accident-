import serial
import time  

arduino = serial.Serial('COM4', 9600)

def person(diff_cnt, max_diff,np,nc):

    if np>0:
        if diff_cnt > max_diff:
            m ='2'
            m = [m.encode('utf-8')]
            arduino.writelines(m)
        else:
            m ='3'
            m = [m.encode('utf-8')]
            arduino.writelines(m)

    if nc>0:
        if diff_cnt > max_diff:
            m ='1'
            m = [m.encode('utf-8')]
            arduino.writelines(m)
        else:
            m ='3'
            m = [m.encode('utf-8')]
            arduino.writelines(m)
        
    if np==0 & nc==0:
            m ='6'
            m = [m.encode('utf-8')]
            arduino.writelines(m)