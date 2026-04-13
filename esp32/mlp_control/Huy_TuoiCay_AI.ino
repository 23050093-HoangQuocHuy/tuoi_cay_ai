#include <EloquentTinyML.h>
#include "DHT.h"
#include "model_data.h"

#define NUMBER_OF_INPUTS 3   
#define NUMBER_OF_OUTPUTS 1  
#define TENSOR_ARENA_SIZE 8*1024

Eloquent::TinyML::TfLite<NUMBER_OF_INPUTS, NUMBER_OF_OUTPUTS, TENSOR_ARENA_SIZE> mlp;

#define DHTPIN 4
#define DHTTYPE DHT11
#define SOIL_PIN 36
#define PUMP_PIN 5 

DHT dht(DHTPIN, DHTTYPE);

void setup() {
    Serial.begin(115200);
    dht.begin();
    
    // Khởi tạo ban đầu là INPUT để tránh rò điện làm bơm tự chạy
    pinMode(PUMP_PIN, INPUT); 

    if (!mlp.begin(model_data)) {
        Serial.println("Lỗi: Không nạp được bộ não AI!");
        while (1) delay(100);
    }
    Serial.println("=====================================");
    Serial.println("HỆ THỐNG TƯỚI CÂY AI - ĐÃ SẴN SÀNG!");
    Serial.println("=====================================");
}

void loop() {
    // 1. Đọc dữ liệu từ các cảm biến
    float t = dht.readTemperature(); // Nhiệt độ
    float h = dht.readHumidity();    // Độ ẩm không khí
    int soilRaw = analogRead(SOIL_PIN); // Độ ẩm đất (giá trị thô)
    
    // Quy đổi độ ẩm đất sang % (4095: Khô, 1118: Ướt)
    float soilPercent = map(soilRaw, 4095, 1118, 0, 100);
    soilPercent = constrain(soilPercent, 0, 100);

    // Kiểm tra nếu cảm biến DHT11 bị lỗi dây
    if (isnan(t) || isnan(h)) {
        Serial.println("Đang đợi dữ liệu từ cảm biến DHT11...");
        delay(2000);
        return;
    }

    // 2. AI thực hiện tính toán dự đoán
    float input[3] = { t, h, soilPercent };
    float prediction = mlp.predict(input);

    // 3. Hiển thị thông số tiếng Việt (Để Huy chụp ảnh báo cáo)
    Serial.print("Nhiệt độ: "); Serial.print(t, 1); Serial.print("°C");
    Serial.print(" | Độ ẩm KK: "); Serial.print(h, 0); Serial.print("%");
    Serial.print(" | Độ ẩm Đất: "); Serial.print(soilPercent, 0); Serial.print("%");
    Serial.print(" | AI Dự đoán: "); Serial.println(prediction, 4);

    // 4. Điều khiển máy bơm dựa trên kết quả AI
    if (prediction > 0.5) {
        // Nếu AI đoán > 0.5 là đất đang cần nước
        Serial.println(">>> TRẠNG THÁI: [BẬT] - ĐANG TƯỚI CÂY");
        pinMode(PUMP_PIN, OUTPUT);    
        digitalWrite(PUMP_PIN, LOW);  
    } else {
        // Nếu AI đoán < 0.5 là đất đã đủ ẩm
        Serial.println(">>> TRẠNG THÁI: [TẮT] - NGỪNG TƯỚI");
        pinMode(PUMP_PIN, INPUT);     // Chuyển sang INPUT để ngắt điện tuyệt đối
    }

    Serial.println("-------------------------------------");
    delay(3000); // Đợi 3 giây rồi kiểm tra tiếp
}