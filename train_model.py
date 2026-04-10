import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import StandardScaler

# ===== 1. ĐỌC DỮ LIỆU =====
data = pd.read_csv("data.csv")

X = data[['moisture', 'temp', 'rain']]
y = data['label']

# ===== 2. CHUẨN HÓA DỮ LIỆU =====
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ===== 3. CHIA TRAIN / TEST =====
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# ===== 4. TẠO MODEL MLP =====
model = MLPClassifier(
    hidden_layer_sizes=(10, 5),
    max_iter=500,
    random_state=42
)

# ===== 5. TRAIN MODEL =====
model.fit(X_train, y_train)

# ===== 6. DỰ ĐOÁN =====
y_pred = model.predict(X_test)

# ===== 7. ĐÁNH GIÁ =====
acc = accuracy_score(y_test, y_pred)

print("===== KẾT QUẢ =====")
print("Accuracy:", acc)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# ===== 8. IN MỘT PHẦN TEST =====
print("\n===== DỮ LIỆU TEST =====")
print(pd.DataFrame(X_test).head())

print("\n===== DỰ ĐOÁN =====")
print(y_pred[:5])

# ===== 9. TEST MẪU =====
sample = pd.DataFrame([[30, 32, 0]], columns=['moisture', 'temp', 'rain'])
sample_scaled = scaler.transform(sample)

print("\n===== TEST MẪU =====")
print("Input:", sample.values.tolist())
print("Prediction:", model.predict(sample_scaled))