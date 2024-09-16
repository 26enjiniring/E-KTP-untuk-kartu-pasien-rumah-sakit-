#include <ESP8266WiFi.h>
#include <FirebaseESP8266.h>
#include <DHT.h>
#include <Wire.h>
#include <Adafruit_MLX90614.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

#include "Wire.h"
#include "Adafruit_GFX.h"
//#include "OakOLED.h"
#include <Adafruit_SSD1306.h>
//OakOLED oled;
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);


const byte RATE_SIZE = 4;
byte rates[RATE_SIZE];
byte rateSpot = 0;
float temp;
//float temp;
String stat;

#define REPORTING_PERIOD_MS 1000
#define FIREBASE_HOST "rfid-e94ef-default-rtdb.firebaseio.com"  //without https    
#define FIREBASE_AUTH "Cky7x6N4vPXKb8pAYPlS67hAKbqrcUFv5oDwvFTL"
#define WIFI_SSID "OMAH_AYOE"
#define WIFI_PASSWORD "Allahtaala"
FirebaseData firebaseData;
FirebaseJson json;

#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN D4 //10 arduino
#define RST_PIN D3 //9 arduino
MFRC522 mfrc522(SS_PIN, RST_PIN);
MFRC522::MIFARE_Key key;

Adafruit_MLX90614 mlx = Adafruit_MLX90614();

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  Serial.println();
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3D for 128x64
    Serial.println(F("SSD1306 allocation failed"));
    for (;;);
  }
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(1);
  display.setCursor(0, 0);
  display.println("Initializing Thermometer..");
  display.display();
  if (!mlx.begin())
  {
    Serial.println("FAILED");
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(1);
    display.setCursor(0, 0);
    display.println("FAILED");
    display.display();
    for (;;);
  }
  else
  {
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("Connecting to ");
    Serial.print(WIFI_SSID);
    while (WiFi.status() != WL_CONNECTED) {
      Serial.print(".");
      delay(500);
    }

    Serial.println();
    Serial.print("Connected");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
    Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH); //connect to Database
    Firebase.reconnectWiFi(true);
    SPI.begin();      // Initiate  SPI bus
    mfrc522.PCD_Init();   // Initiate MFRC522

    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(1);
    display.setCursor(0, 0);
    display.println("SUCCESS");
    display.display();
    Serial.println("SUCCESS");
    delay(1000);

    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(1);
    display.setCursor(0, 0);
    display.println("Place your card on reader...");
    Serial.println("Place your card on reader...");
  }
}


void send_sensor() {
  temp = mlx.readObjectTempC();
//  temp = temp * 0.98;

  //
  //        if (temp < 45 && temp > 20 )
  //          {
  //
  //          rates[rateSpot++] = (byte)temp;
  //          rateSpot %= RATE_SIZE;
  //
  //          temp = 0;
  //          for (byte x = 0; x < RATE_SIZE; x++)
  //            {
  //              temp += rates[x];
  //            }
  //          temp /= RATE_SIZE;
  //          }
  //

}

void check_stat() {
  if (temp < 30.0) {
    stat = "ERROR";
  }
  else if (temp >= 30.0 && temp <= 37.8) {
    stat = "NORMAL";
  }
  else if (temp > 37.8) {
    stat = "DEMAM";
  }

}

void loop() {
  // put your main code here, to run repeatedly:

  display.display();

  if ( ! mfrc522.PICC_IsNewCardPresent())
  {
    return;
  }
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial())
  {
    return;
  }
  //Show UID on serial monitor

  Serial.print("UID tag :");
  String content = "";
  byte letter;
  for (byte i = 0; i < mfrc522.uid.size; i++)
  {
    //     Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
    //     Serial.print(mfrc522.uid.uidByte[i], HEX);
    content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
    content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  Serial.println(content.substring(1));
  Firebase.setString(firebaseData, "/Check/check/UID2", content.substring(1));
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(1);
  display.setCursor(0, 0);
  display.println("Checking to Server");
  display.display();
  Serial.println("Checking to Server");
  delay(2000);
  if (Firebase.getInt(firebaseData, "/Check/logic/logic")) {

    if (firebaseData.dataTypeEnum() == fb_esp_rtdb_data_type_integer) {
      int logic = firebaseData.to<int>();
      if (logic == 1) {
        display.clearDisplay();
        display.setTextSize(1);
        display.setTextColor(1);
        display.setCursor(0, 0);
        display.println("Card registered");
        display.display();
        Serial.println("Card registered");
        delay(1500);
        display.clearDisplay();
        display.setTextSize(1);
        display.setTextColor(1);
        display.setCursor(0, 0);
        display.println("arahkan sensor ke tubuh dengan jarak 10cm");
        display.display();
        Serial.println("Cek suhu anda");
        delay(1500);

        for (int i = 0; i <= 200; i += 1) {
          send_sensor();
          check_stat();
          display.clearDisplay();
          display.setTextSize(1);
          display.setTextColor(1);
          display.setCursor(0, 16);
          display.println(temp);

          display.setTextSize(1);
          display.setTextColor(1);
          display.setCursor(0, 0);
          display.println("SUHU ANDA :");

          display.setTextSize(1);
          display.setTextColor(1);
          display.setCursor(0, 45);
          display.println("Scanning");

          display.setTextSize(1);
          display.setTextColor(1);
          display.setCursor(0, 30);
          display.println("STATUS :");
          display.display();
          //        delay(10);
        }
        delay(1000);

        display.clearDisplay();
        display.setTextSize(1);
        display.setTextColor(1);
        display.setCursor(0, 16);
        display.println(temp);

        display.setTextSize(1);
        display.setTextColor(1);
        display.setCursor(0, 0);
        display.println("SUHU ANDA :");

        display.setTextSize(1);
        display.setTextColor(1);
        display.setCursor(0, 45);
        display.println(stat);

        display.setTextSize(1);
        display.setTextColor(1);
        display.setCursor(0, 30);
        display.println("STATUS :");
        display.display();


        delay(2000);

        display.clearDisplay();
        display.setTextSize(1);
        display.setTextColor(1);
        display.setCursor(0, 0);
        display.println("sending data to server");
        display.display();
        Serial.println("send data sensor");
        int nilai = 1;
        Firebase.setFloat(firebaseData, "/Check/Suhu/suhu", temp);
        Firebase.setString(firebaseData, "/Check/Status/status", stat);
        Firebase.setInt(firebaseData, "/Check/logic2/logic2", nilai);
        delay(1500);
      }

      else if (logic == 0) {
        display.clearDisplay();
        display.setTextSize(1);
        display.setTextColor(1);
        display.setCursor(0, 0);
        display.println("Card unregistered");
        display.display();
        Serial.println("Card unregistered");
        delay(2000);
      }

    }

  }
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(1);
  display.setCursor(0, 0);
  display.println("Place your card on reader...");
}
