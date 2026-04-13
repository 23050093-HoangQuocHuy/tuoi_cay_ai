import tensorflow as tf
import numpy as np
import os

# 1. Đường dẫn file model đã luyện
model_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'model_mlp_huy.h5')
header_path = os.path.join(os.path.dirname(__file__), '..', 'esp32', 'model_data.h')

# 2. Chuyển đổi sang TensorFlow Lite (để nén model)
model = tf.keras.models.load_model(model_path)
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# 3. Chuyển mảng Byte sang định dạng C Header
def hex_to_c_array(hex_data, var_name):
    c_str = f"const unsigned char {var_name}[] DATA_ALIGN_ATTRIBUTE = {{\n  "
    c_str += ", ".join([f"0x{byte:02x}" for byte in hex_data])
    c_str += "\n};\n"
    c_str += f"const unsigned int {var_name}_len = {len(hex_data)};"
    return c_str

# 4. Lưu thành file .h vào thư mục esp32/
with open(header_path, "w") as f:
    f.write('#include <pgmspace.h>\n\n')
    # Thêm macro để tương thích với một số thư viện TinyML
    f.write('#define DATA_ALIGN_ATTRIBUTE __attribute__((aligned(4)))\n\n')
    f.write(hex_to_c_array(tflite_model, "model_data"))

print(f"Đã chuyển đổi thành công! File lưu tại: {header_path}")