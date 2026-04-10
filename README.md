#  Hệ thống tưới cây tự động sử dụng AI

##  Giới thiệu
Dự án xây dựng hệ thống tưới cây tự động cho ban công/nhà, sử dụng:
- Cảm biến độ ẩm đất
- Nhiệt độ môi trường
- Kết hợp AI (MLP) và Logic mờ (Fuzzy Logic)

Hệ thống sẽ tự động quyết định có tưới hay không dựa trên điều kiện thực tế.

---

##  Mục tiêu
- Tự động hóa việc tưới cây
- Giảm lãng phí nước
- Ứng dụng AI vào hệ thống nhúng (ESP32)

---

##  Phương pháp sử dụng

### 1. MLP (Machine Learning)
- Dùng để học từ dữ liệu (độ ẩm, nhiệt độ, mưa)
- Dự đoán: có nên tưới hay không

### 2. Logic mờ (Fuzzy Logic)
- Sử dụng luật IF-THEN
- Quyết định dựa trên mức độ (không phải đúng/sai)

---

##  Công nghệ sử dụng
- Python (scikit-learn, scikit-fuzzy)
- Arduino IDE (ESP32)
- VS Code
- GitHub

---

##  Dataset
- Soil moisture dataset (độ ẩm đất)
- Weather dataset (nhiệt độ, mưa)
- Hoặc dữ liệu mô phỏng

---

##  Quy trình thực hiện

1. Thu thập / tạo dữ liệu
2. Train model MLP
3. Xây dựng hệ thống logic mờ:
   - Xác định biến (moisture, temp)
   - Xây dựng membership function
   - Tạo luật IF-THEN
4. Test với nhiều trường hợp
5. Đánh giá kết quả

---