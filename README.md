# Hệ thống tưới cây tự động cho ban công/nhà - AI & Fuzzy Logic

Dự án nghiên cứu và triển khai hệ thống điều khiển tưới cây thông minh trên nền tảng ESP32, ứng dụng hai phương pháp tính toán hiện đại để tối ưu hóa lượng nước tưới.

##  Thành viên thực hiện
- **Hoàng Quốc Huy:** Phát triển mô hình mạng nơ-ron nhân tạo **MLP (Multi-Layer Perceptron)**.
- **Lưu Hồng Phương:** Phát triển mô hình điều khiển **Logic mờ (Fuzzy Logic)**.

##  Tính năng nổi bật
- **Mô hình MLP (Huy):** Sử dụng Deep Learning để dự đoán trạng thái tưới dựa trên dữ liệu lịch sử (Data-driven).
- **Mô hình Logic mờ (Phương):** Xây dựng các tập mờ và luật hợp thành (If-Then) dựa trên kinh nghiệm chuyên gia để ra quyết định điều khiển linh hoạt.
- **Edge AI:** Cả hai mô hình đều được tối ưu hóa để chạy trực tiếp trên chip ESP32 mà không cần kết nối Server.
- **Tối ưu phần cứng:** Kỹ thuật điều khiển chân GPIO thông minh để triệt tiêu dòng rò cho Relay.

##  Cấu trúc thư mục
* `data/`: Chứa tập dữ liệu huấn luyện `smart_agriculture.csv`.
* `model/`: Lưu trữ các file mô hình `.h5` và các hàm thành viên (Membership Functions).
* `src/`: Code Python huấn luyện MLP và cấu trúc luật mờ.
* `esp32/`: Code triển khai thực tế trên vi điều khiển.

## SƠ ĐỒ KẾT NỐI CHI TIẾT (HARDWARE PINOUT)
Hệ thống sử dụng Kit ESP32 38-Pin Type-C. Việc kết nối chính xác các chân tín hiệu và nguồn là yếu tố then chốt để AI vận hành ổn định.

1. Cảm biến Nhiệt độ & Độ ẩm (DHT11)

Chân VCC: Nối vào chân 3V3 hoặc 5V trên ESP32.

Chân GND: Nối vào chân GND trên ESP32.

Chân DATA: Nối vào chân GPIO 4 trên ESP32.

2. Cảm biến Độ ẩm đất (Soil Moisture Sensor)

Chân VCC: Nối vào chân 3V3 hoặc 5V trên ESP32.

Chân GND: Nối vào chân GND trên ESP32.

Chân AO (Analog Output): Nối vào chân GPIO 36 (VP) trên ESP32.

3. Module Relay điều khiển máy bơm

Chân VCC: Nối vào chân 5V (Vin) trên ESP32 (Cấp nguồn 5V giúp Relay đóng ngắt dứt điểm).

Chân GND: Nối vào chân GND trên ESP32.

Chân IN (Tín hiệu): Nối vào chân GPIO 5 trên ESP32.

4. Sơ đồ đấu nối động cơ (Máy bơm)

Cực Dương (+) của nguồn ngoài: Nối vào cổng COM (chân giữa) của Relay.

Cực Dương (+) của Máy bơm: Nối vào cổng NO (chân bên trái) của Relay.

Cực Âm (-) của nguồn ngoài và cực Âm (-) của Máy bơm: Nối trực tiếp với nhau.

##  Logic vận hành
### 1. Model MLP (Hoàng Quốc Huy)
Mô hình được huấn luyện qua 3 lớp (Input, Hidden, Output) giúp máy học được các mối liên hệ phi tuyến tính phức tạp giữa môi trường và nhu cầu của cây. Kết quả trả về giá trị xác suất từ `0.0` đến `1.0`.

### 2. Logic mờ (Lưu Hồng Phương)
Hệ thống sử dụng các biến ngôn ngữ như "Khô", "Vừa", "Ẩm" kết hợp với các luật điều khiển mờ để đưa ra quyết định tưới mượt mà, giúp hệ thống hoạt động ổn định kể cả khi cảm biến có sai số nhỏ.

##  Kết quả thực nghiệm
Hệ thống hoạt động ổn định, máy bơm ngắt/mở chính xác theo dự đoán của AI:
- Đất khô: AI dự đoán ON (1.0).
- Đất đủ ẩm: AI dự đoán OFF (0.0).

---
*Đồ án hoàn thành năm 2026*