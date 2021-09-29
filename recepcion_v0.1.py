
import serial
from serial import Serial
import serial

import time
import threading

def envio_de_datos_manuales( comando):

    #Acimut
    #R // Clockwise Rotation
    if comando=='RC':
        texto = b'R\n'
        ser.write(texto)

    #L// Counter Clockwise Rotation
    if comando == 'CRC':
        texto = b'L\n'
        ser.write(texto)

    # A // CW/CCW Rotation Stop
    if comando == 'Stop_Acim':
        texto = b'A\n'
        ser.write(texto)

    # U // UP Direction Rotation
    if comando == 'UpDR':
        texto = b'A\n'
        ser.write(texto)

    # D // DOWN Direction Rotation
    if comando == 'DownDR':
        texto = b'D\n'
        ser.write(texto)

    # E // UP/DOWN Direction Rotation Stop
    if comando == 'Stop_ele':
        texto = b'D\n'
        ser.write(texto)

def Solicitud_datos(comando):
    # Acimut
    # C // solicitar datos
    if comando == 'acimut':
        texto = b'C\n'
        ser.write(texto)

    # elevacion
    # B // solicitar datos
    if comando == 'elevacion':
        texto = b'B\n'
        ser.write(texto)

    # todo
    # B // solicitar datos
    if comando == 'all':
        texto = b'C\n'
        ser.write(texto)
        texto = b'B\n'
        ser.write(texto)

def all_stop():
    # Parar
    # S // solicitar datos
    command = b'S\n'
    ser.write(command)

def Tracking(acimut,elevacion):
    #parametros="P"+str(float("{0:.1f}".format(float(acimut))))+" "+str(float("{0:0.1f}".format(float(elevacion))))
    parametros="P"+str(acimut)+" "+str(elevacion)
    ser.write(parametros.encode('ascii'))

def Recepcion_datos():
    if ser.in_waiting > 0:  # if incoming bytes are waiting to be read from the serial input buffer
        data_str = ser.read(ser.inWaiting()).decode('ascii')  # read the bytes and convert from binary array to ASCII

        slice_object1 = slice(3)
        slice_object2 = slice(4, 5, 1)
        if data_str == '\r':
            comando = b'recibi un CR\n'
            ser.write(comando)
        if data_str == '\r' + '\n':
            comando = b'recibi un CRLf\n'
            ser.write(comando)
            envio_de_datos_manuales('RC')
            Tracking(19.2, 50.9)
        if data_str[slice_object2] == '\r' + ',' + '\n':
            print('entre correcto', end='')
        if data_str == "?>\r\n":
            comando = b'comando erroneo\n'
            ser.write(comando)

        # print(data_str[slice_object1], end='')
        # print(data_str[slice_object2], end='')
        # print('el 2',slice_object2, end='')
    # print('el 1',slice_object1, end='')
    # print(data_str, end='')  # print the incoming string without putting a new-line ('\n') automatically after every print()
    # comando = b'puto el que lee \n'
    # ser.write(comando)
    # Put the rest of your code you want here
    time.sleep(0.01)  # Optional: sleep 10 ms (0.01 sec) once per loop to let other threads on your PC run during this time


ser = serial.Serial('COM3', 9600)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    while 1:

        time.sleep(1)
        Recepcion_datos()







