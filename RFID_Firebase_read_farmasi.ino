
#include <ESP8266WiFi.h>                 
#include <FirebaseESP8266.h> 
  
#define FIREBASE_HOST "rfid-e94ef-default-rtdb.firebaseio.com"  //without https    
#define FIREBASE_AUTH "Cky7x6N4vPXKb8pAYPlS67hAKbqrcUFv5oDwvFTL"            
#define WIFI_SSID "OMAH_AYOE"                          
#define WIFI_PASSWORD "Allahtaala"     

#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN D4  //10 arduino
#define RST_PIN D3 //9 arduino
#define LED D8
MFRC522 mfrc522(SS_PIN, RST_PIN); 
MFRC522::MIFARE_Key key; 

FirebaseData firebaseData;
FirebaseJson json;

void sending(){
   Serial.println("PASSED");
   Serial.println("PATH: " + firebaseData.dataPath());
   Serial.println("TYPE: " + firebaseData.dataType());
   Serial.println("ETag: " + firebaseData.ETag());
   Serial.println("------------------------------------");
   Serial.println();

}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);   
  pinMode(LED,OUTPUT);
  SPI.begin();      // Initiate  SPI bus
  mfrc522.PCD_Init();   // Initiate MFRC522

  Serial.println();
                                                    
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
  Serial.println("Place your card on reader...");
  digitalWrite(LED,HIGH);
}
void loop() {
  // put your main code here, to run repeatedly:

    // Look for new cards
  digitalWrite(LED,HIGH);
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
  String content= "";
  byte letter;
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
//     Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
//     Serial.print(mfrc522.uid.uidByte[i], HEX);
     content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  Serial.println(content.substring(1));
  //********************************************************************
    Firebase.setString(firebaseData, "/Farmasi/read/UID2",content.substring(1));
    sending();
    digitalWrite(LED,LOW);
    delay(500);
    Serial.println("Success fully added");
  

         
   }

