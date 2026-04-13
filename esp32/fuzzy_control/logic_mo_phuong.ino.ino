#include <Fuzzy.h>
#include "DHT.h"

// --- CẤU HÌNH CHÂN CẮM (GIỮ NGUYÊN NHƯ BẢN MLP CỦA HUY) ---
#define DHTPIN 4
#define DHTTYPE DHT11
#define SOIL_PIN 36
#define PUMP_PIN 5

DHT dht(DHTPIN, DHTTYPE);
Fuzzy *fuzzy = new Fuzzy();

void setup() {
  Serial.begin(115200);
  dht.begin();
  
  // Khởi tạo chân bơm là INPUT để chống rò điện lúc mới khởi động
  pinMode(PUMP_PIN, INPUT); 

  // 1. ĐỊNH NGHĨA BIẾN ĐẦU VÀO: ĐỘ ẨM ĐẤT (Input 1)
  FuzzyInput *soilMoisture = new FuzzyInput(1);
  
  // Định nghĩa các vùng mờ (Khô, Vừa, Ướt)
  FuzzySet *dry = new FuzzySet(0, 0, 20, 40);      // Độ ẩm từ 0-40% là vùng Khô
  FuzzySet *mid = new FuzzySet(30, 50, 50, 70);    // Độ ẩm từ 30-70% là vùng Vừa
  FuzzySet *wet = new FuzzySet(60, 80, 100, 100);  // Độ ẩm từ 60-100% là vùng Ướt
  
  soilMoisture->addFuzzySet(dry);
  soilMoisture->addFuzzySet(mid);
  soilMoisture->addFuzzySet(wet);
  fuzzy->addFuzzyInput(soilMoisture);

  // 2. ĐỊNH NGHĨA BIẾN ĐẦU RA: TRẠNG THÁI BƠM (Output 1)
  FuzzyOutput *pump = new FuzzyOutput(1);
  
  // Định nghĩa các mức đầu ra (Tắt, Bật)
  FuzzySet *off = new FuzzySet(0, 0, 0, 0.4);      
  FuzzySet *on = new FuzzySet(0.6, 1, 1, 1);       
  
  pump->addFuzzySet(off);
  pump->addFuzzySet(on);
  fuzzy->addFuzzyOutput(pump);

  // 3. THIẾT LẬP CÁC LUẬT MỜ (RULES)
  
  // Luật 1: NẾU Đất Khô THÌ Bật bơm
  FuzzyRuleAntecedent *ifDry = new FuzzyRuleAntecedent();
  ifDry->joinSingle(dry);
  FuzzyRuleConsequent *thenOn = new FuzzyRuleConsequent();
  thenOn->addOutput(on);
  FuzzyRule *rule1 = new FuzzyRule(1, ifDry, thenOn);
  fuzzy->addFuzzyRule(rule1);

  // Luật 2: NẾU Đất Ướt THÌ Tắt bơm
  FuzzyRuleAntecedent *ifWet = new FuzzyRuleAntecedent();
  ifWet->joinSingle(wet);
  FuzzyRuleConsequent *thenOff = new FuzzyRuleConsequent();
  thenOff->addOutput(off);
  FuzzyRule *rule2 = new FuzzyRule(2, ifWet, thenOff);
  fuzzy->addFuzzyRule(rule2);

  Serial.println("================================");
  Serial.println("LOGIC MO (FUZZY) - PHUONG & HUY");
  Serial.println("HE THONG DA SAN SANG!");
  Serial.println("================================");
}

void loop() {
  // Đọc dữ liệu thực tế
  float t = dht.readTemperature();
  int soilRaw = analogRead(SOIL_PIN);
  
  // Quy đổi giá trị Analog sang % độ ẩm đất
  float soilPercent = map(soilRaw, 4095, 1118, 0, 100);
  soilPercent = constrain(soilPercent, 0, 100);

  // Kiểm tra cảm biến DHT11 (để tránh lỗi đọc)
  if (isnan(t)) {
    delay(1000);
    return;
  }

  // Đưa dữ liệu vào bộ xử lý Logic mờ
  fuzzy->setInput(1, soilPercent);
  fuzzy->fuzzify();

  // Giải mờ để lấy kết quả (Số từ 0.0 đến 1.0)
  float result = fuzzy->defuzzify(1);

  // In thông số ra Serial Monitor để theo dõi
  Serial.print("Nhiet do: "); Serial.print(t, 1); Serial.print("C");
  Serial.print(" | Do am dat: "); Serial.print(soilPercent, 1); Serial.print("%");
  Serial.print(" | Ket qua mo: "); Serial.print(result, 2);

  // Điều khiển Relay dựa trên kết quả giải mờ (Ngưỡng 0.5)
  if (result >= 0.5) {
    Serial.println(" -> TRANG THAI: [BAT]");
    pinMode(PUMP_PIN, OUTPUT);
    digitalWrite(PUMP_PIN, LOW); // Relay kích mức thấp
  } else {
    Serial.println(" -> TRANG THAI: [TAT]");
    pinMode(PUMP_PIN, INPUT);    // Chống rò điện
  }

  Serial.println("--------------------------------");
  delay(3000); // Đợi 3 giây cho lần kiểm tra tiếp theo
}