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

##  Sơ đồ kết nối (Pinout)
| Linh kiện | Chân ESP32 | Ghi chú |
| :--- | :--- | :--- |
| **Cảm biến DHT11** | GPIO 4 | Đo nhiệt độ & độ ẩm không khí |
| **Cảm biến Độ ẩm đất** | GPIO 36 (VP) | Đo độ ẩm đất (Analog) |
| **Module Relay (IN)** | GPIO 5 | Điều khiển máy bơm |

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