# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# se necesitan


import filecmp

"""marcadorinit = '$$SOE'
marcadorfin = '$$EOE'"""
#chequear_linea = ' Date_(ZONE)_HR:MN, , , Azi_(a-app), Elev_(a-app),'
txt = open("2015HM10.txt")
file = open("comandos.txt", "w")
##datosfinal = []

# Press the green button in the gutter to run the script.

def generacion_comandos():

    if (validador() == 1):
        print('pase')
        generacion_txt()
        print('ok')



def validador():
    chequear_linea = ' Date_(ZONE)_HR:MN, , , Azi_(a-app), Elev_(a-app),'
    linea1 = txt.readline()
    while len(linea1) > 0:

        if chequear_linea in linea1:
            return 1
            break

        linea1 = txt.readline()

    return 0

def generacion_txt():
    marcadorinit = '$$SOE'
    marcadorfin = '$$EOE'
    flaginit = 0
    datosfinal = []
    print('pase')
    linea = txt.readline()
    while len (linea) > 0:

        # se encuentra el de datos, bajo la flag
        if marcadorfin in linea:
            flaginit = 0

       #Codigo a ejecutar para filtrar el archivo
        if flaginit == 1:

            dato = linea.split(',')
            datosfinal= dato[0] +"," +"P"+str(float("{0:.1f}".format(float(dato[3]))))+" "+str(float("{0:.1f}".format(float(dato[4]))))
            #datosfinal= dato[0] +"," +"P"+dato[3].replace("   ","")+" "+dato[4].replace("  ", "")

            file.write(datosfinal+'\n')

            print(datosfinal)


            #print(linea)
        #Fin de codigo a ejecutar  para analizar los datos




        # Encuentro el inicio de la trama deseada, levanta flag
        if  marcadorinit in linea:
            flaginit= 1


        linea = txt.readline()




# See PyCharm help at https://www.jetbrains.com/help/pycharm/"""

if __name__ == '__main__':
    generacion_comandos()
    """if(validador() == 1):
        
        print('pase')
        #txt.seek(0)
        generacion_txt()
        print('ok')"""
file.close()
txt.close()