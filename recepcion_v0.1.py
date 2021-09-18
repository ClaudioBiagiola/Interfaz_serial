
import serial
from serial import Serial
import serial

import time
import threading




ser = serial.Serial('COM3', 9600)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    while 1:

        if ser.in_waiting > 0:  # if incoming bytes are waiting to be read from the serial input buffer
            data_str = ser.read(ser.inWaiting()).decode('ascii')  # read the bytes and convert from binary array to ASCII
            # recibo un CR
           # if data_str[:1] == '\r':
            #    comando = b'recibi un CR\n'
             #   ser.write(comando)
            slice_object1 = slice(3)
            slice_object2 = slice(4,5,1)
            if data_str == '\r' :
                comando = b'recibi un CR\n'
                ser.write(comando)
            if data_str == '\r'+'\n':
                comando = b'recibi un CRLf\n'
                ser.write(comando)
            if data_str[slice_object2] == '\r'+','+'\n' :
                 print('entre correcto', end='')
            if data_str ==  "?>\r\n" :
                comando = b'comando erroneo\n'
                ser.write(comando)

            print(data_str[slice_object1], end='')
            print(data_str[slice_object2], end='')
            print('el 2',slice_object2, end='')
            print('el 1',slice_object1, end='')
            #print(data_str, end='')  # print the incoming string without putting a new-line ('\n') automatically after every print()
            #comando = b'puto el que lee \n'
            #ser.write(comando)
        # Put the rest of your code you want here
        time.sleep(0.01)  # Optional: sleep 10 ms (0.01 sec) once per loop to let other threads on your PC run during this time








