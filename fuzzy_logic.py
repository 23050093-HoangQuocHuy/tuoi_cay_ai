import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# ===== 1. KHAI BÁO BIẾN =====
moisture = ctrl.Antecedent(np.arange(0, 101, 1), 'moisture')
temp = ctrl.Antecedent(np.arange(0, 51, 1), 'temp')
water = ctrl.Consequent(np.arange(0, 101, 1), 'water')

# ===== 2. MEMBERSHIP =====
# Độ ẩm
moisture['low'] = fuzz.trimf(moisture.universe, [0, 0, 35])
moisture['medium'] = fuzz.trimf(moisture.universe, [30, 50, 70])
moisture['high'] = fuzz.trimf(moisture.universe, [65, 100, 100])

# Nhiệt độ
temp['low'] = fuzz.trimf(temp.universe, [0, 0, 20])
temp['medium'] = fuzz.trimf(temp.universe, [15, 25, 35])
temp['high'] = fuzz.trimf(temp.universe, [30, 50, 50])

# Nước tưới
water['off'] = fuzz.trimf(water.universe, [0, 0, 50])
water['on'] = fuzz.trimf(water.universe, [50, 100, 100])

# ===== 3. RULE =====
rule1 = ctrl.Rule(moisture['low'] & temp['high'], water['on'])
rule2 = ctrl.Rule(moisture['low'] & temp['medium'], water['on'])
rule3 = ctrl.Rule(moisture['medium'], water['off'])
rule4 = ctrl.Rule(moisture['high'], water['off'])

# ===== 4. SYSTEM =====
watering_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
watering = ctrl.ControlSystemSimulation(watering_ctrl)

# ===== 5. TEST NHIỀU TRƯỜNG HỢP =====
test_cases = [
    [20, 35],  # rất khô, nóng
    [30, 25],  # hơi khô
    [50, 30],  # trung bình
    [80, 20],  # ẩm cao
]

print("=== TEST HỆ THỐNG TƯỚI ===")

for m, t in test_cases:
    watering.input['moisture'] = m
    watering.input['temp'] = t
    watering.compute()

    result = watering.output['water']
    
    print(f"Moisture={m}, Temp={t} -> Output={result:.2f}", end=" ")
    
    if result > 50:
        print("=> TƯỚI")
    else:
        print("=> KHÔNG TƯỚI")