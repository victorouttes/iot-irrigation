#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#define RELE D1

const char* SSID = ""; // rede wifi
const char* PASSWORD = ""; // senha da rede wifi

const char* BROKER_MQTT = ""; //url do servidor MQTT
int BROKER_PORT = 1883;
const char* BROKER_USER = ""; //usuario
const char* BROKER_PASS = ""; //senha
const char* BROKER_TOPIC = "iot";
const char* BROKER_TOPIC_IRRIGATION = "iot-irrigation";
int BROKER_QOS = 1;
const char* IRRIGATION_ON = "ON";
const char* IRRIGATION_OFF = "OFF";

// prototypes
void initPins();
void initSerial();
void initWiFi();
void initMQTT();

WiFiClient espClient;
PubSubClient MQTT(espClient); // instancia o mqtt

// setup
void setup() {
  initPins();
  initSerial();
  initWiFi();
  initMQTT();
  irrigationOff();
}

void loop() {
  if (!MQTT.connected()) {
    reconnectMQTT();
  }
  recconectWiFi();
  MQTT.loop();
}

void initPins() {
  pinMode(RELE, OUTPUT);
}

void initSerial() {
  Serial.begin(9600);
}

void initWiFi() {
  delay(10);
  Serial.println("Conectando-se em: " + String(SSID));

  WiFi.begin(SSID, PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Conectado na Rede " + String(SSID) + " | IP => ");
  Serial.println(WiFi.localIP());
}

void irrigationOn() {
  digitalWrite(RELE, LOW);
}

void irrigationOff() {
  digitalWrite(RELE, HIGH);
}

void initMQTT() {
  MQTT.setServer(BROKER_MQTT, BROKER_PORT);
  MQTT.setCallback(mqtt_callback);
}

void mqtt_callback(char* topic, byte* payload, unsigned int length) {
  String message;
  for (int i = 0; i < length; i++) {
    char c = (char)payload[i];
    message += c;
  }
  if (strcmp(topic, BROKER_TOPIC_IRRIGATION) == 0) {
    if (message == IRRIGATION_ON) {
      irrigationOn();
    } else {
      irrigationOff();
    }
  }
  if (strcmp(topic, BROKER_TOPIC) == 0) {
    char mes[50];
    message.toCharArray(mes, 50);
    float umidade = atof(strtok(mes, ";"));
    float temperatura = atof(strtok(NULL, ";"));
    float luz = atof(strtok(NULL, ";"));
    if (luz >= 15.0 && luz <= 30.0) {
      if (umidade >= 500) {
        irrigationOn();
        delay(5000);
        irrigationOff();
      }
    }
  }
  Serial.println("Tópico => " + String(topic) + " | Valor => " + String(message));
}

void reconnectMQTT() {
  while (!MQTT.connected()) {
    Serial.println("Tentando se conectar ao Broker MQTT: " + String(BROKER_MQTT));
    
    if (MQTT.connect("ESP8266-IRRIGADOR", BROKER_USER, BROKER_PASS)) {
      Serial.println("Conectado");
      MQTT.subscribe(BROKER_TOPIC_IRRIGATION, BROKER_QOS);
      MQTT.subscribe(BROKER_TOPIC, BROKER_QOS);

    } else {
      Serial.println("Falha ao Reconectar");
      Serial.println("Tentando se reconectar em 2 segundos");
      delay(2000);
    }
  }
}

void recconectWiFi() {
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }
}
