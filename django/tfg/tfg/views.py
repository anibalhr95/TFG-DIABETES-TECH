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
from django.http import HttpResponse
import datetime
from django.template import Template, Context
from django.template import loader
from django.shortcuts import render



#ser = serial.Serial('/dev/ttyUSB0',9600)
#ser.flushInput()

con = mysql.connector.connect(
    host='localhost',
    user='anibal',
    password='pi',
    database="AlimentosReconocidos"
)


def index(request):
    #lineBytes = ser.readline()
    mycursor = con.cursor()
    mycursor.execute("SELECT Producto FROM ALIMENTOSRECONOCIMIENTO ORDER BY id DESC LIMIT 1")
    productoAlimento  = mycursor.fetchone()
    #productoAlimento1 = float(productoAlimento[0])
    productoAlimento2 = str(productoAlimento[0])
    con.commit()

    mycursor.execute("SELECT Peso FROM ALIMENTOSRECONOCIMIENTO ORDER BY id DESC LIMIT 1")
    productoPeso  = mycursor.fetchone()
    productoPeso1 = float(productoPeso[0])
    productoPeso2 = str(productoPeso1)
    con.commit()


    mycursor.execute("SELECT HC FROM ALIMENTOSRECONOCIMIENTO ORDER BY id DESC LIMIT 1")
    productoHC  = mycursor.fetchone()
    productoHC1 = float(productoHC[0])
    productoHC2 = str(productoHC1)
    con.commit()


    mycursor.execute("SELECT IC FROM ALIMENTOSRECONOCIMIENTO ORDER BY id DESC LIMIT 1")
    productoIC = mycursor.fetchone()
    productoIC1 = float(productoIC[0])
    productoIC2 = str(productoIC1)
    con.commit()

    
    peso = productoPeso2
    nombre= productoAlimento2
    indice_glucemico= productoIC2
    carga_glucemica= productoHC2
    #doc_externo = open("/home/pi/tfg/transmision/djangoTest/TFG/TFG/plantillas/miplantilla.html")
    #plt = Template(doc_externo.read())
    #doc_externo.close()
    doc_externo =  loader.get_template('miplantilla.html')
    #ctx=Context({"nombre_alimento":nombre, "peso_alimento": peso, "indice_glucemico": indice_glucemico, "carga_glucemica": carga_glucemica})
    documento=doc_externo.render({"nombre_alimento":nombre, "peso_alimento": peso, "indice_glucemico": indice_glucemico, "carga_glucemica": carga_glucemica})
    
   
    return HttpResponse(documento)


def reconocimiento(request):
    mycursor = con.cursor()
    mycursor.execute("SELECT Producto FROM ALIMENTOSRECONOCIMIENTO ORDER BY id DESC LIMIT 1")
    productoAlimento  = mycursor.fetchone()
    #productoAlimento1 = float(productoAlimento[0])
    productoAlimento2 = str(productoAlimento[0])
    con.commit()

    mycursor.execute("SELECT Peso FROM ALIMENTOSRECONOCIMIENTO ORDER BY id DESC LIMIT 1")
    productoPeso  = mycursor.fetchone()
    productoPeso1 = float(productoPeso[0])
    productoPeso2 = str(productoPeso1)
    con.commit()


    mycursor.execute("SELECT HC FROM ALIMENTOSRECONOCIMIENTO ORDER BY id DESC LIMIT 1")
    productoHC  = mycursor.fetchone()
    productoHC1 = float(productoHC[0])
    productoHC2 = str(productoHC1)
    con.commit()


    mycursor.execute("SELECT IC FROM ALIMENTOSRECONOCIMIENTO ORDER BY id DESC LIMIT 1")
    productoIC = mycursor.fetchone()
    productoIC1 = float(productoIC[0])
    productoIC2 = str(productoIC1)
    con.commit()

    
    peso = productoPeso2
    nombre= productoAlimento2
    indice_glucemico= productoIC2
    carga_glucemica= productoHC2
    #doc_externo = open("/home/pi/tfg/transmision/djangoTest/TFG/TFG/plantillas/miplantilla.html")
    #plt = Template(doc_externo.read())
    #doc_externo.close()
    doc_externo =  loader.get_template('reconocimiento.html')
    #ctx=Context({"nombre_alimento":nombre, "peso_alimento": peso, "indice_glucemico": indice_glucemico, "carga_glucemica": carga_glucemica})
    documento2=doc_externo.render({"nombre_alimento":nombre, "peso_alimento": peso, "indice_glucemico": indice_glucemico, "carga_glucemica": carga_glucemica})
    return HttpResponse(documento2)
    
def ipcamera(request):
    mycursor = con.cursor()
    mycursor.execute('SELECT Producto FROM ALIMENTOSRECONOCIMIENTO')
    productos = [row[0] for row in mycursor.fetchall()]
    productos1= " ".join(productos)
    mycursor.execute('SELECT Peso FROM ALIMENTOSRECONOCIMIENTO')
    pesos = [row[0] for row in mycursor.fetchall()]
    pesos1= " ".join(map(str, pesos))
    mycursor.execute('SELECT IC FROM ALIMENTOSRECONOCIMIENTO')
    IC = [row[0] for row in mycursor.fetchall()]
    IC1 =  " ".join(map(str, IC))
    mycursor.execute('SELECT HC FROM ALIMENTOSRECONOCIMIENTO')
    HC = [row[0] for row in mycursor.fetchall()]
    HC1 =  " ".join(map(str, HC))



    
    doc_externo =  loader.get_template('ipcam.html')
    #ctx=Context({"nombre_alimento":nombre, "peso_alimento": peso, "indice_glucemico": indice_glucemico, "carga_glucemica": carga_glucemica})
    documento8=doc_externo.render({"productos":productos1, "pesos":pesos1, "IC":IC1, "HC":HC1})
    return HttpResponse(documento8)
    
    
    
def historial(request):
    mycursor = con.cursor()
    mycursor.execute('SELECT Producto FROM ALIMENTOSRECONOCIMIENTO')
    productos = [row[0] for row in mycursor.fetchall()]
    productos1= " ".join(productos)
    mycursor.execute('SELECT Peso FROM ALIMENTOSRECONOCIMIENTO')
    pesos = [row[0] for row in mycursor.fetchall()]
    pesos1= " ".join(map(str, pesos))
    mycursor.execute('SELECT IC FROM ALIMENTOSRECONOCIMIENTO')
    IC = [row[0] for row in mycursor.fetchall()]
    IC1 =  " ".join(map(str, IC))
    mycursor.execute('SELECT HC FROM ALIMENTOSRECONOCIMIENTO')
    HC = [row[0] for row in mycursor.fetchall()]
    HC1 =  " ".join(map(str, HC))



    
    doc_externo =  loader.get_template('historial.html')
    #ctx=Context({"nombre_alimento":nombre, "peso_alimento": peso, "indice_glucemico": indice_glucemico, "carga_glucemica": carga_glucemica})
    documento3=doc_externo.render({"productos":productos1, "pesos":pesos1, "IC":IC1, "HC":HC1})
    return HttpResponse(documento3)

def contacto(request):
    mycursor = con.cursor()
    mycursor.execute("SELECT Producto FROM ALIMENTOSRECONOCIMIENTO ORDER BY id DESC LIMIT 1")
    productoAlimento  = mycursor.fetchone()
    #productoAlimento1 = float(productoAlimento[0])
    productoAlimento2 = str(productoAlimento[0])
    con.commit()

    mycursor.execute("SELECT Peso FROM ALIMENTOSRECONOCIMIENTO ORDER BY id DESC LIMIT 1")
    productoPeso  = mycursor.fetchone()
    productoPeso1 = float(productoPeso[0])
    productoPeso2 = str(productoPeso1)
    con.commit()


    mycursor.execute("SELECT HC FROM ALIMENTOSRECONOCIMIENTO ORDER BY id DESC LIMIT 1")
    productoHC  = mycursor.fetchone()
    productoHC1 = float(productoHC[0])
    productoHC2 = str(productoHC1)
    con.commit()


    mycursor.execute("SELECT IC FROM ALIMENTOSRECONOCIMIENTO ORDER BY id DESC LIMIT 1")
    productoIC = mycursor.fetchone()
    productoIC1 = float(productoIC[0])
    productoIC2 = str(productoIC1)
    con.commit()

    
    peso = productoPeso2
    nombre= productoAlimento2
    indice_glucemico= productoIC2
    carga_glucemica= productoHC2
    #doc_externo = open("/home/pi/tfg/transmision/djangoTest/TFG/TFG/plantillas/miplantilla.html")
    #plt = Template(doc_externo.read())
    #doc_externo.close()
    doc_externo =  loader.get_template('miplantilla.html')
    #ctx=Context({"nombre_alimento":nombre, "peso_alimento": peso, "indice_glucemico": indice_glucemico, "carga_glucemica": carga_glucemica})
    documento3=doc_externo.render({"nombre_alimento":nombre, "peso_alimento": peso, "indice_glucemico": indice_glucemico, "carga_glucemica": carga_glucemica})
    return HttpResponse(documento3)

def dameFecha(request):
    fecha_actual=datetime.datetime.now()
    
    documento="""<html>
    <body>
    <h1>
    Fecha y hora actuales %s
    </h1>
    </body>
    </html>""" %fecha_actual
    return HttpResponse(documento)


