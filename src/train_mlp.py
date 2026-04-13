import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
import os

# 1. Đọc dữ liệu
# Đảm bảo file smart_agriculture.csv nằm trong thư mục data
path = os.path.join(os.path.dirname(__file__), '..', 'data', 'smart_agriculture.csv')

if not os.path.exists(path):
    print(f"Lỗi: Không tìm thấy file dữ liệu tại {path}")
else:
    df = pd.read_csv(path)

    # 2. Chọn cột đầu vào và đầu ra
    # Thứ tự: temp (nhiệt độ), humidity (độ ẩm không khí), MOI (độ ẩm đất)
    X = df[['temp', 'humidity', 'MOI']]
    y = df['result'].replace(2, 0) # Chuyển nhãn 2 (không tưới) thành 0 để AI dễ hiểu

    # 3. Chia dữ liệu (KHÔNG DÙNG SCALER để ESP32 đọc trực tiếp được số thực)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Xây dựng Model MLP
    model = Sequential([
        Dense(12, input_dim=3, activation='relu'), # Lớp vào 3 nút
        Dense(8, activation='relu'),               # Lớp ẩn
        Dense(1, activation='sigmoid')             # Lớp ra (0 đến 1)
    ])

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # 5. Huấn luyện Model
    print("--------------------------------------------------")
    print("Bắt đầu huấn luyện AI (Phiên bản không Scaler)...")
    print("--------------------------------------------------")
    # Huấn luyện trực tiếp trên X_train
    model.fit(X_train, y_train, epochs=100, batch_size=5, verbose=1)

    # 6. Kiểm tra độ chính xác sau khi train
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"\nĐộ chính xác mô hình: {accuracy*100:.2f}%")

    # 7. Lưu vào thư mục model
    model_dir = os.path.join(os.path.dirname(__file__), '..', 'model')
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        
    model_path = os.path.join(model_dir, 'model_mlp_huy.h5')
    model.save(model_path)

    print("--------------------------------------------------")
    print(f"Đã lưu bộ não AI thành công tại: {model_path}")
    print("BƯỚC TIẾP THEO: Huy hãy chạy file convert_to_header.py nhé!")
    print("--------------------------------------------------")