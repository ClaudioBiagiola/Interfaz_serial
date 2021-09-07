
# includes
import serial
import time

# variables
ser = serial.Serial('COM3', 9600)
count=0
timeout=100

if __name__ == '__main__':
    ##comando = b'envio python\n'
    ##ser.write(comando)
    while 1:
        count += 1

        if ser.in_waiting > 0:  # if incoming bytes are waiting to be read from the serial input buffer
            data_str = ser.read(ser.inWaiting()).decode('ascii')  # read the bytes and convert from binary array to ASCII
            print(data_str, end='')  # print the incoming string without putting a new-line ('\n') automatically after every print()
            comando = b'puto el que lee \n'
            ser.write(comando)
            count=0
        # Put the rest of your code you want here
        print(count)
        if count == timeout:
            print('salio')
            break;

        time.sleep(0.1)  # Optional: sleep 10 ms (0.01 sec) once per loop to let other threads on your PC run during this time

