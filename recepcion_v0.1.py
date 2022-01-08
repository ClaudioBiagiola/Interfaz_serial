from builtins import print

import serial
from serial import Serial
import serial

import time
import datetime
from datetime import datetime
import threading

""""   ======================= [Lista de comandos validos] =======================

  Trama (PC -> Interface):  Envio: XXX'CR'             (XXX comando valido)
  Trama (intercafe -> PC):  Respuesta:      'CR'            (Sin pedidos de datos)
                                            'CR''LF'XXX     (XXX datos)
                                            ?>'CR'           (Comando no valido)

 Nota: Los comandos basicos del Yaesu solo soportan 3 digitos por ángulo, en el caso de los
 comando extendidos se enviaran/recibiran más caracteres.

    =======================   Comandos manuales   =======================
  Acimut:
   R               // Clockwise Rotation
   L               // Counter Clockwise Rotation
   A               // CW/CCW Rotation Stop
  Elevacion:
   U               // UP Direction Rotation
   D               // DOWN Direction Rotation
   E               // UP/DOWN Direction Rotation Stop
  
 =======================   Comandos lectura   =========================
   C               // Retornar el valor actual del ángulo de acimut
   B               // Retornar el valor de actual del ángulo de elevación
  
  =======================   Comandos tracking   ========================
   S               // Parar todo moviento asociado a cualquier ángulo
   Paaa.a eee.e    // Establecer objetivo de tracking
 
   ======================================================================
"""
#---------archivo de entrada el mismo generado por el generador de txt----------
file = open("comandos3.txt", "r")
#----------habilito el serial--------------
ser = serial.Serial('COM14', 9600, )
Flag_recep=False
flag1=True
acimut=0
elevacion=0
data_acimut = -99 #valor no valido
data_elevacion = -99 #valor no valido
"""----------------Comando Manuales-------------------"""
"""
mov                                         in                  out
Acimut  Clockwise Rotation                  RC ---------------> R
Acimut  Counter Clockwise Rotation          CRC --------------> L
Acimut  CW/CCW Rotation Stop                Stop_Acim --------> A
Elevacion UP Direction Rotation             UpDR -------------> U
Elevacion DOWN Direction Rotation           DownDR -----------> D
Elevacion UP/DOWN Direction Rotation Stop   Stop_ele ---------> E
"""



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
        texto = b'U\n'
        ser.write(texto)

    # D // DOWN Direction Rotation
    if comando == 'DownDR':
        texto = b'D\n'
        ser.write(texto)

    # E // UP/DOWN Direction Rotation Stop
    if comando == 'Stop_ele':
        texto = b'E\n'
        ser.write(texto)

"""
Acimut                  C // solicitar datos ------------> C
Elevacion               B // solicitar datos-------------> B
Acimut elevacion        B // solicitar datos-------------> C-B
"""
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

    ser.write(parametros.encode('ascii')+ b'\r')
    print(parametros.encode('ascii')+ b'\r')
    print("envie comando")

def Recepcion_datos():
    if ser.in_waiting > 0:  # if incoming bytes are waiting to be read from the serial input buffer
        data_str = ser.read(ser.inWaiting()).decode('ascii')  # read the bytes and convert from binary array to ASCII
        Flag_recep=True
        slice_object1 = slice(3)
        slice_object2 = slice(4, 5, 1)
        informacion='a'

        if data_str == '\r\n':
            return 'mensaje_correcto'
            data = 'mensaje correcto'

        if data_str == "?>\r\n":
            return 'mensaje_erroneo'
            data='mensaje erroneo'
            comando = b'comando erroneo\n'
            ser.write(comando)

        if Flag_recep:
            dato1 = data_str.split(',')
            if dato1[len(dato1)-1] == " \r\n":
                if dato1[0] != 0 and dato1[1] == 0:
                    data =dato1[1]
                if dato1[1] !=0:
                    data = dato1[0]+','+dato1[1]
                    Tracking(dato1[0],dato1[1])

        return data
    time.sleep(0.01)  # Optional: sleep 10 ms (0.01 sec) once per loop to let other threads on your PC run during this time

def Control_autonomo():
    global data_acimut
    global data_elevacion
    global flag1
    lineasleidas=0
    hora_actual = time.strftime('%H:%M')
    """--------solicito fecha y la genero al formato para comparar con el archivo----------"""
    fecha_sin_analizar= time.strftime('%m/%d/%y')
    objDate = datetime.strptime(fecha_sin_analizar,'%m/%d/%y')
    fecha=datetime.strftime(objDate, '%Y-%b-%d')

    total_lines = sum(1 for line in file)
    file.seek(0)
    #print(total_lines)
    linea = file.readline()
    while len(linea) > 0:
        dato1 = linea.split(',')

        if dato1[1] == hora_actual and fecha == dato1[0]:
           # print("envie comando")
            if flag1:
                data_acimut=dato1[2]
                data_elevacion=dato1[3]
                Tracking(float(dato1[2]),float(dato1[3]))
                flag1=False
                lineasleidas=lineasleidas+1

            if (float(data_acimut)!=float(dato1[2])) | (float(data_elevacion)!=float(dato1[3])):
                Tracking(float(dato1[2]), float(dato1[3]))
                data_acimut = dato1[2]
                data_elevacion = dato1[3]
                lineasleidas += 1


        linea = file.readline()
        #data = file.readlines()[total_lines]

    return 0
    if total_lines==lineasleidas:
        return 1

# Press the green button in the gutter to run the script.

if __name__ == '__main__':
   ## flags_tracking1 = 1
    ##flags_tracking2 = 1
    command = b'....\r'
    ser.write(command)
    while 1:
       # data = Recepcion_datos()
       # print(data)

        time.sleep(1)
        #data = Recepcion_datos()
        #print(data)
        Control_autonomo()
        #print(data)
       # pass






