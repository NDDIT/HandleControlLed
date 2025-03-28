#define BLYNK_TEMPLATE_ID "TMPL6ZNW_sr80"
#define BLYNK_TEMPLATE_NAME "ControlLed"
#define BLYNK_AUTH_TOKEN "iVvuG0xatpOYcFI-8YW9QtkwpemEDj4J"
#define BLYNK_PRINT Serial
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>

// Thay thế bằng thông tin WiFi của bạn
char ssid[] = "IotC2";  
char pass[] = "danhgia5sao";

// Nhập Auth Token từ Blynk (Email gửi về)
char auth[] = BLYNK_AUTH_TOKEN;

// Khai báo các chân điều khiển đèn
#define LED1 LED_BUILTIN
#define LED2 D6
#define LED3 D7

void setup() {
  Serial.begin(115200);
  Blynk.begin(auth, ssid, pass);

  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);

  // Đảm bảo đèn tắt khi khởi động
  digitalWrite(LED1, HIGH);
  digitalWrite(LED2, HIGH);
  digitalWrite(LED3, HIGH);
}

// Nhận lệnh từ Blynk (Blynk Button V1, V2, V3)
BLYNK_WRITE(V1) { digitalWrite(LED1, !param.asInt()); } // Đảo tín hiệu
BLYNK_WRITE(V2) { digitalWrite(LED2, !param.asInt()); }
BLYNK_WRITE(V3) { digitalWrite(LED3, !param.asInt()); }

void loop() {
  Blynk.run();
}
