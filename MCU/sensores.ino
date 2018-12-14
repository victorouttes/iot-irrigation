#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#define MUX_A D1
#define MUX_B D2
#define MUX_C D3
#define ANALOG_INPUT A0

const char* SSID = ""; // rede wifi
const char* PASSWORD = ""; // senha da rede wifi

const char* BROKER_MQTT = ""; //url do servidor MQTT
int BROKER_PORT = 1883;
const char* BROKER_USER = ""; //usuario
const char* BROKER_PASS = ""; //senha
const char* BROKER_TOPIC = "iot";
int BROKER_QOS = 1;

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
}

void changeMux(int a, int b, int c) {
  digitalWrite(MUX_A, a);
  digitalWrite(MUX_B, b);
  digitalWrite(MUX_C, c);
}

void loop() {
  if (!MQTT.connected()) {
    reconnectMQTT();
  }
  recconectWiFi();
  
  float valueUmidade, valorTemperatura, valorLuminosidade;
  changeMux(LOW, LOW, LOW);
  valueUmidade = analogRead(ANALOG_INPUT); //pino A0 do MUX (umidade)
  
  changeMux(HIGH, LOW, HIGH);
  float valor = analogRead(ANALOG_INPUT); //pino A5 do MUX (temperatura)
  valorTemperatura = (3.3 * valor * 100.0) / 1024.0; //convertendo para graus Celcius
  
  changeMux(LOW, HIGH, LOW);
  valorLuminosidade = analogRead(ANALOG_INPUT); //pino A2 do MUX (luminosidade)
  
  char publicar[50];
  sprintf(publicar, "%f;%f;%f", valueUmidade, valorTemperatura, valorLuminosidade);
  MQTT.publish("iot", publicar);
  delay(60000); //coleta de 1 em 1 min.
}

void initPins() {
  pinMode(MUX_A, OUTPUT);
  pinMode(MUX_B, OUTPUT);
  pinMode(MUX_C, OUTPUT);
  pinMode(ANALOG_INPUT, INPUT);
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
  Serial.println("Tópico => " + String(topic) + " | Valor => " + String(message));
}

void reconnectMQTT() {
  while (!MQTT.connected()) {
    Serial.println("Tentando se conectar ao Broker MQTT: " + String(BROKER_MQTT));
    
    if (MQTT.connect("ESP8266-SENSOR", BROKER_USER, BROKER_PASS)) {
      Serial.println("Conectado");
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