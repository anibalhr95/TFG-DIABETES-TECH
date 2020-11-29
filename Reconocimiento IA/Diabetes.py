import RPi.GPIO as GPIO
import time
import io
import picamera
from clarifai.rest import ClarifaiApp
from time import sleep
import serial
import mysql.connector
import decimal
import struct
import test
import shutil

# BASE DE DATOS MYSQL
con = mysql.connector.connect(
    host='localhost',
    user='anibal',
    password='pi',
    database= "AlimentosReconocidos"
)
mycursor = con.cursor()

# SERIAL
ser = serial.Serial('/dev/ttyUSB0', 9600)
ser.flushInput()

# NEOPIXEL
# DECLARACION BOTON
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
with picamera.PiCamera(resolution='640x480', framerate=30) as camera:
    # CONFIGURACION CAMARA
    camera.led = False
    
    
    # FIN CONFIGURACION CAMARA

    # CLARIFAI
    app = ClarifaiApp(api_key='2ba21ecb25d94a9b88fd5c1b2553cb6a')
    model = app.public_models.general_model
   

    # FIN CLARIFAI
    lineBytes = ser.readline()
    line = lineBytes.decode('utf-8').strip()

    while True:
        try:

            lineBytes = ser.readline()
            line = lineBytes.decode('utf-8').strip()
            Status = GPIO.input(27)
            if Status == False:
                ser.write("B".encode())
                camera.capture("alimento.jpg")
                print("Detectando alimento, por favor espere...")
                time.sleep(0.2)
                shutil.copy('alimento.jpg', '/home/pi/tfg/transmision/djangotestcopia/tfg/static/images/')
                response = model.predict_by_filename("alimento.jpg")
                concepts = response['outputs'][0]['data']['concepts']
                for concept in concepts:
                    if concept['name'] == 'food':
                        food_model = app.public_models.food_model
                        result = food_model.predict_by_filename(
                            "alimento.jpg")
                        first_concept = result['outputs'][0]['data']['concepts'][0]['name']
                        second_concept = result['outputs'][0]['data']['concepts'][1]['name']
                        third_concept = result['outputs'][0]['data']['concepts'][2]['name']
                        print("Producto: " + first_concept + " - Peso: " + line)
                        print("Producto: " + second_concept + " - Peso: " + line)
                        print("Producto: " + third_concept + " - Peso: " + line)
                        espacio = " "
                        ser.write(espacio.encode())
                        ser.write(first_concept.encode())
                        print(" ")
                        print("------------------")
                        print(" ")
                        mycursor.execute("INSERT INTO RECONOCIMIENTO(Producto, Peso) VALUES (%s,%s)", (first_concept, line))
                        con.commit()
                        mycursor.execute("SELECT cargaGlucémica FROM DIABETES WHERE Producto LIKE '%' %(fts)s '%' LIMIT 1;", {
                                         "fts": first_concept})
                        data1 = mycursor.fetchone()
                        command0 = float(data1[0])
                        dat1 = str(command0)
                        time.sleep(2)
                        ser.write(" HC: ".encode())
                        ser.write(dat1.encode())
                        print("Carga Glucémica(HC):")
                        print(dat1)

                        mycursor.execute("SELECT indiceGlucemico FROM DIABETES WHERE Producto LIKE '%' %(fts)s '%' LIMIT 1;", {
                                         "fts": first_concept})
                        data2 = mycursor.fetchone()
                        command = int(data2[0])
                        le = str(command)
                        ser.write(" IC: ".encode())
                        ser.write(le.encode())
                        print("Indice Glucémico(IC):")
                        print(le)
                        mycursor.execute("INSERT INTO ALIMENTOSRECONOCIMIENTO(Producto, Peso, HC, IC) VALUES (%s,%s,%s,%s)", (first_concept, line, dat1, le))
                        con.commit()
                        print("RECONOCIMIENTO ACABADO CON EXITO")
                        
        except KeyboardInterrupt:
            break
