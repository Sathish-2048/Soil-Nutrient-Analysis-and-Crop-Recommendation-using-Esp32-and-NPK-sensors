#include <SoftwareSerial.h>
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid     = "******";
const char* password = "******";


#define RX  18
#define TX  19
#define EN  4

SoftwareSerial NPK(RX, TX);
uint8_t RxBuffer[11];

// Sensor values
uint16_t moisture = 0, temperature = 0;
uint16_t conductivity = 0, ph = 0;
uint16_t nitrogen = 0, phosphorus = 0, potassium = 0;

void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid, password);

    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        Serial.print(".");
        delay(500);
    }
    Serial.println("\nConnected to WiFi!");

  pinMode(EN, OUTPUT);
  digitalWrite(EN, LOW);
  NPK.begin(9600, SWSERIAL_8N1, RX, TX, false);
  Serial.println("Soil Sensor Ready");
}

void sendToThingSpeak(float temp, float humi, float c, float ph, float n, float phos, float pots) {
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println(" WiFi Disconnected! Retrying...");
        WiFi.begin(ssid, password);
        return;
    }

    String readings = "{\"Moisture\":\"" + String(temp) + "\", \"Temperature\":\"" + String(humi) + "\", \"pH\":\"" + String(ph) + "\", \"Nitrogen\":\"" + String(n) + "\", \"Phosphorus\":\"" + String(phos) + "\", \"Pottasium\":\"" + String(pots) + "\"}";
   
    HTTPClient http;
    http.begin("http://xxx.xxx.xxx.xxx:8000/data");
    http.addHeader("Content-Type", "application/json");
   
    int httpResponseCode = http.POST(readings);
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    Serial.println(readings);
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Response: " + response);
    } else {
      Serial.print("Error on HTTP request: ");
      Serial.println(httpResponseCode);
    }
    http.end();
}

void sendRequest(uint8_t *request, size_t len) {
  NPK.flush();
  digitalWrite(EN, HIGH);
  delay(2);
  for (int i = 0; i < len; i++) {
    NPK.write(request[i]);
    delayMicroseconds(100);
  }
  digitalWrite(EN, LOW);
}

bool receiveResponse(uint8_t expectedLength) {
  memset(RxBuffer, 0, sizeof(RxBuffer));
  int i = 0;
  unsigned long startTime = millis();
  while (i < expectedLength && (millis() - startTime < 1000)) {
    if (NPK.available()) {
      RxBuffer[i] = NPK.read();
      i++;
    }
  }
  return (i == expectedLength && RxBuffer[0] == 0x01 && RxBuffer[1] == 0x03);
}

void readTemp() {
  uint8_t request[] = {0x01, 0x03, 0x00, 0x13, 0x00, 0x01, 0x75, 0xcf};
  sendRequest(request, sizeof(request));
  if (receiveResponse(7)) {
    temperature    = RxBuffer[3] << 8 | RxBuffer[4];
    Serial.print("Temperature: "); Serial.println(temperature / 10.0,1);
  } else {
    Serial.println("Temp: No response.");
  }
}

void readMoisture() {
  uint8_t request[] = {0x01, 0x03, 0x00, 0x12, 0x00, 0x01, 0x24, 0x0F};
  sendRequest(request, sizeof(request));
  if (receiveResponse(7)) {
    moisture    = RxBuffer[3] << 8 | RxBuffer[4];
    Serial.print("Moisture: "); Serial.println(moisture / 10.0,1);
  } else {
    Serial.println("Moisture: No response.");
  }
}

void readConductivity() {
  uint8_t request[] = {0x01, 0x03, 0x00, 0x15, 0x00, 0x01, 0x95, 0xce};
  sendRequest(request, sizeof(request));
  if (receiveResponse(7)) {
    conductivity = RxBuffer[3] << 8 | RxBuffer[4];
    Serial.print("Conductivity: "); Serial.println(conductivity);
  } else {
    Serial.println("Conductivity: No response.");
  }
}

void readPH() {
  uint8_t request[] = {0x01, 0x03, 0x00, 0x06, 0x00, 0x01, 0x64, 0x0b};
  sendRequest(request, sizeof(request));
  if (receiveResponse(7)) {
    ph = RxBuffer[3] << 8 | RxBuffer[4];
    Serial.print("pH: "); Serial.println(ph / 100.0, 1);
  } else {
    Serial.println("pH: No response.");
  }
}

void readNitrogen() {
  uint8_t request[] = {0x01, 0x03, 0x00, 0x1E, 0x00, 0x01, 0xE4, 0x0c};
  sendRequest(request, sizeof(request));
  if (receiveResponse(7)) {
    nitrogen = RxBuffer[3] << 8 | RxBuffer[4];
    Serial.print("Nitrogen: "); Serial.println(nitrogen / 10.0, 1);
  } else {
    Serial.println("Nitrogen: No response.");
  }
}

void readPhosphorus() {
  uint8_t request[] = {0x01, 0x03, 0x00, 0x1f, 0x00, 0x01, 0xb5, 0xcc};
  sendRequest(request, sizeof(request));
  if (receiveResponse(7)) {
    phosphorus = RxBuffer[3] << 8 | RxBuffer[4];
    Serial.print("Phosphorus: "); Serial.println(phosphorus / 10.0, 1);
  } else {
    Serial.println("Phosphorus: No response.");
  }
}

void readPotassium() {
  uint8_t request[] = {0x01, 0x03, 0x00, 0x20, 0x00, 0x01, 0x85, 0xc0};
  sendRequest(request, sizeof(request));
  if (receiveResponse(7)) {
    potassium = RxBuffer[3] << 8 | RxBuffer[4];
    Serial.print("Potassium: "); Serial.println(potassium / 10.0, 1);
    Serial.println("--------------------------------------------------------");
  } else {
    Serial.println("Potassium: No response.");
  }
}

void loop() {
  readTemp();
  delay(200);
  readMoisture();
  delay(200);
  readConductivity();
  delay(200);
  readPH();
  delay(200);
  readNitrogen();
  delay(200);
  readPhosphorus();
  delay(200);
  readPotassium();
  sendToThingSpeak(temperature, moisture, conductivity, ph, nitrogen, phosphorus, potassium);
  delay(5000);
}