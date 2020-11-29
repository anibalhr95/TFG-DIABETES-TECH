#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h>
#endif
#include "HX711.h"
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>
#define DOUT  A1
#define CLK  A0
#define buzzer 8
#define PIN 7
#define NUMPIXELS 12
#define DEBUG(a)Serial.println(a);

Adafruit_NeoPixel neopix = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
int delayval = 100;

LiquidCrystal_I2C lcd(0x3F,16,2);  
HX711 scale;
Servo servo1;

const int BotonTare = 10; //Boton para hacer tara 

const int BotonServoVigilancia = 12;

const int BotonServoPeso = 11;

float calibracion_factor = 300000; //factor de calibracion

//Vectores para adornar en pantalla LCD
uint8_t note[8]  = {0x02, 0x03, 0x02, 0x0e, 0x1e, 0x0c, 0x00, 0x00};
uint8_t arrow[8] = {0x0, 0x04 ,0x06, 0x1f, 0x06, 0x04, 0x00, 0x00};
byte customChar[] = {
  B00000,
  B11110,
  B01100,
  B01100,
  B11110,
  B11110,
  B11110,
  B11110
};
byte cuadro[] = {
  B11111,
  B11111,
  B11111,
  B11111,
  B11111,
  B11111,
  B11111,
  B11111
};
uint16_t i;
int positionpix= 0;

void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  pinMode(BotonTare, INPUT_PULLUP);
  pinMode(BotonServo, INPUT_PULLUP);
  pinMode(BotonServoNormal, INPUT_PULLUP);
  pinMode(buzzer, OUTPUT);

  ///NEOPIXEL INICIO
  #if defined (__AVR_ATtiny85__)
  if (F_CPU == 16000000) clock_prescale_set(clock_div_1);
  #endif
  neopix.begin(); // Inicializa neopixel
  teatroArcoIris(10);
  delay(1000);
  cambiaColor(neopix.Color(0, 0, 0), 50); //negro
  //NEOPIXEL FIN

  //Creación de los simbolos en pantalla alojandolos en memoria
  lcd.createChar(1622, arrow);   
  lcd.createChar(265, customChar);
  lcd.createChar(264, cuadro);
  digitalWrite(buzzer , HIGH);
  delay(500);
  digitalWrite(buzzer , LOW);
  lcd.home(); //Home
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(" ANIBAL HERRERA ");
  lcd.setCursor(0,1);  
  lcd.print("----->TFG<------");
  delay(3000);
  lcd.clear();
  servo1.attach(3);
  servo1.write(90);
 
  
  scale.begin(DOUT, CLK);
  scale.set_scale();
  scale.tare(20); 
  scale.set_scale(calibracion_factor); 
  long zero_factor = scale.read_average(); 

}

void loop() {
  
  scale.set_scale(calibracion_factor); //ajusta la escala con el factor de calibracion
  lcd.setCursor(0,0);
  lcd.print("Peso (Kg): "); 
  lcd.setCursor(5,1);
  lcd.write(265);
  lcd.setCursor(7,1);
  lcd.print(scale.get_units(), 3);
  Serial.println(scale.get_units(), 3);
  float PESO= scale.get_units(3);
  if(PESO > 0.005){
    cambiaColor(neopix.Color(255, 255, 255), 50); //blanco
  }else{
    cambiaColor(neopix.Color(0, 0, 0), 50); //negro
    
  }
  delay(100);
  if(Serial.available()){
    String data1 = Serial.readStringUntil("\n");
    if(data1 == "B"){
      digitalWrite(buzzer , HIGH);
      delay(500);
      digitalWrite(buzzer , LOW);
       
    }else{
      arcoIris(20);
      lcd.clear();
      lcd.print("  Reconociendo");
      lcd.setCursor(0,1);
      lcd.print("    alimento...");
      delay(2000);
      lcd.clear();
      lcd.setCursor(0,0);
      

      
      lcd.print(data1);
      String data2 = Serial.readStringUntil("\n");


      lcd.setCursor(0,1);
      lcd.print(data2);
     // lcd.print(scale.get_units(), 3);
      //lcd.print(" kg");
      cambiaColor(neopix.Color(0, 143, 57), 50); //verde
      delay(1000);
      if(PESO > 0.005){
      cambiaColor(neopix.Color(255, 255, 255), 50); //BLANCO
      }else{
      cambiaColor(neopix.Color(0, 0, 0), 50); //negro
      }
      delay(10000);
      lcd.clear();
    }
    delay(100);
  }
  
  if(!digitalRead(BotonTare)){
    digitalWrite(buzzer , HIGH);
    delay(500);
    digitalWrite(buzzer , LOW);
    lcd.clear();
    scale.tare(20);
    lcd.write(264);
    lcd.write(264);
    lcd.print("    Tara    ");
    lcd.write(264);
    lcd.write(264);
    lcd.setCursor(0,1);
    lcd.write(264);
    lcd.print("   Realizada  ");
    lcd.write(264);
    cambiaColor(neopix.Color(0, 143, 57), 50); //verde
    delay(1000);
    lcd.clear();
    if(PESO > 0.005){
      cambiaColor(neopix.Color(255, 255, 255), 50); //BLANCO
    }else{
      cambiaColor(neopix.Color(0, 0, 0), 50); //negro
    }
    while(!digitalRead(BotonTare));
  }
  if(!digitalRead(BotonServoVigilancia)){
    Serial.println("ENTRA");
    digitalWrite(buzzer , HIGH);
    delay(500);
    digitalWrite(buzzer , LOW);
    lcd.clear();
    servo1.write(180);
    lcd.write(264);
    lcd.write(264);
    lcd.print("   Modo     ");
    lcd.write(264);
    lcd.write(264);
    lcd.setCursor(0,1);
    lcd.write(264);
    lcd.print("  Vigilancia  ");
    lcd.write(264);
    cambiaColor(neopix.Color(0, 143, 57), 50); //verde
    delay(1000);
    lcd.clear();
    if(PESO > 0.005){
      cambiaColor(neopix.Color(255, 255, 255), 50); //BLANCO
    }else{
    cambiaColor(neopix.Color(0, 0, 0), 50); //negro
    }
    while(!digitalRead(BotonServoVigilancia));
  }
  if(!digitalRead(BotonServoPeso)){
    digitalWrite(buzzer , HIGH);
    delay(500);
    digitalWrite(buzzer , LOW);
    lcd.clear();
    servo1.write(90);
    lcd.write(264);
    lcd.write(264);
    lcd.print("    Modo    ");
    lcd.write(264);
    lcd.write(264);
    lcd.setCursor(0,1);
    lcd.write(264);
    lcd.print("   ");
    lcd.write(265);
    lcd.print(" Peso ");
    lcd.write(265);
    lcd.print("   ");
    lcd.write(264);
    cambiaColor(neopix.Color(0, 143, 57), 50); //verde
    delay(1000);
    lcd.clear();
    if(PESO > 0.005){
      cambiaColor(neopix.Color(255, 255, 255), 50); //BLANCO

    }else{
    cambiaColor(neopix.Color(0, 0, 0), 50); //negro
    }
    while(!digitalRead(BotonServoPeso));
  }
  if(Serial.available())
  {
    char temp = Serial.read();
    if(temp == '+' || temp == 'a')
      calibracion_factor += 10;
    else if(temp == '-' || temp == 'z')
      calibracion_factor -= 10;
  }
}


// Cogido de las librerias de NeoPixel
void cambiaColor(uint32_t c, uint8_t wait) {
  for(uint16_t i=0; i<neopix.numPixels(); i++) {
    neopix.setPixelColor(i, c);
    neopix.show();
    delay(wait);
  }
}

void arcoIris(uint8_t wait) {
  uint16_t i, j;

  for(j=0; j<256; j++) {
    for(i=0; i<neopix.numPixels(); i++) {
      neopix.setPixelColor(i, Rueda((i+j) & 255));
    }
    neopix.show();
    delay(wait);
  }
}

void arcoIrisCiclo(uint8_t wait) {
  uint16_t i, j;
  for(j=0; j<256*5; j++) { 
    for(i=0; i< neopix.numPixels(); i++) {
      neopix.setPixelColor(i, Rueda(((i * 256 / neopix.numPixels()) + j) & 255));
    }
    neopix.show();
    delay(wait);
  }
}

void teatroCarrera(uint32_t c, uint8_t wait) {
  for (int j=0; j<10; j++) {  
    for (int q=0; q < 3; q++) {
      for (uint16_t i=0; i < neopix.numPixels(); i=i+3) {
        neopix.setPixelColor(i+q, c);    
      }
      neopix.show();
      delay(wait);

      for (uint16_t i=0; i < neopix.numPixels(); i=i+3) {
        neopix.setPixelColor(i+q, 0);        
      }
    }
  }
}

void teatroArcoIris(uint8_t wait) {
  for (int j=0; j < 256; j++) {    
    for (int q=0; q < 3; q++) {
      for (uint16_t i=0; i < neopix.numPixels(); i=i+3) {
        neopix.setPixelColor(i+q, Rueda( (i+j) % 255));   
      }
      neopix.show();

      delay(wait);

      for (uint16_t i=0; i < neopix.numPixels(); i=i+3) {
        neopix.setPixelColor(i+q, 0);       
      }
    }
  }
}


uint32_t Rueda(byte RuedaPos) {
  RuedaPos = 255 - RuedaPos;
  if(RuedaPos < 85) {
    return neopix.Color(255 - RuedaPos * 3, 0, RuedaPos * 3);
  }
  if(RuedaPos < 170) {
    RuedaPos -= 85;
    return neopix.Color(0, RuedaPos * 3, 255 - RuedaPos * 3);
  }
  RuedaPos -= 170;
  return neopix.Color(RuedaPos * 3, 255 - RuedaPos * 3, 0);
}
