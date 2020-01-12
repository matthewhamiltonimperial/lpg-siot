# FEATURES: dT, d^2T

import pandas as pd
import matplotlib.pyplot as plt
from sklearn import tree
import numpy as np
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score

data = pd.read_csv("siot-main1.csv", engine='python', usecols=[0,1,2])  # Reading from csv
data["Weight (Kg)"] = data["Weight (Kg)"].values[::-1]                  # Changing order so first entry is earliest entry
data["Temperature (°C)"] = data["Temperature (°C)"].values[::-1]        # Changing order so first entry is earliest entry
data["On/off"] = data["On/off"].values[::-1]                            # Changing order so first entry is earliest entry
data['dT'] = data["Temperature (°C)"].diff(periods=-11)
data['d^2T'] = data["dT"].diff(periods=11)

data = data.dropna()

features = data.iloc[1:32122, [3, 4]]
labels = data.iloc[1:32122, 2]

clf = tree.DecisionTreeClassifier(criterion="entropy", max_depth=3)
clf = clf.fit(features, labels)

c_true = data.iloc[32000:45880, 2]
data['Predicted Cooking'] = np.nan

for i in range(32000, 45880):
    data.iloc[i, 5] = clf.predict([[data.iloc[i, 3], data.iloc[i, 4]]])

c_pred = data.iloc[32000:45880, 5]

print(data.head())
print("Accuracy:", accuracy_score(c_true,c_pred))
print("Confusion Matrix:")
print(confusion_matrix(c_true,c_pred))
print("Classification Report:")
print(classification_report(c_true,c_pred))
print("F1 Score:")
print(f1_score(c_true,c_pred))
print(clf.feature_importances_)

weight = data.iloc[1:, 1]
temperature = data.iloc[1:, 0]
on_off = data.iloc[1:, 2]
diffT = data.iloc[1:, 3]
difftwoT = data.iloc[1:, 4]
on_off_pred = data.iloc[1:, 5]
fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.plot(weight, 'k-', label="Weight (Kg)")
ax1.plot(temperature, 'r-', label="Temperature (°C)")
ax2.plot(on_off, 'g-', label="On/Off")
ax2.plot(diffT, 'b-', label="dT")
ax2.plot(difftwoT, 'y-', label="d^2T")
ax2.plot(on_off_pred, 'm-', label="On/Off Predicted")
ax1.legend(loc="upper left")
ax2.legend(loc="upper right")
ax1.set_xlabel('Time')
ax1.set_ylabel('Temperature (°C), Weight (Kg)', color='k')
ax2.set_ylabel('dT, d^2T, On/Off', color='k')
plt.show()
