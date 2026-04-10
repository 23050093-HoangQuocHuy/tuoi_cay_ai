import pandas as pd
import random

data = []

for _ in range(300):
    moisture = random.randint(20, 70)
    temp = random.randint(25, 35)
    rain = random.randint(0, 1)

    if moisture < 40 and rain == 0:
        label = 1
    else:
        label = 0

    data.append([moisture, temp, rain, label])

df = pd.DataFrame(data, columns=["moisture", "temp", "rain", "label"])
df.to_csv("data.csv", index=False)

print("Đã tạo data.csv")