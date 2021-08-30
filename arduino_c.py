import serial
 
arduino = serial.Serial('COM4', 9600)

def person(diff_cnt, max_diff,cp,cc,cm,cb):

    if cp>0 or cc>0 or cm>0 or cb>0: #사람이 있을 때
        if diff_cnt > max_diff:#움직임이 감지 되었을 때
            m ='1'
            m = [m.encode('utf-8')]
            arduino.writelines(m)
        else: #움직임이 감지 되지 않았을 때
            m ='2'
            m = [m.encode('utf-8')]
            arduino.writelines(m)
        
    if cp==0 & cc==0 & cm==0:
            m ='3'
            m = [m.encode('utf-8')]
            arduino.writelines(m)
