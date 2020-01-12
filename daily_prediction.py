import pandas as pd
from sklearn import tree
import numpy as np
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from twilio.rest import Client
import os 

### TRAINING

data = pd.read_csv("siot-main1.csv", engine='python', usecols=[0,1,2])  # Reading from csv
data["Weight (Kg)"] = data["Weight (Kg)"].values[::-1]                  # Changing order so first entry is earliest entry
data["Temperature (°C)"] = data["Temperature (°C)"].values[::-1]        # Changing order so first entry is earliest entry
data["On/off"] = data["On/off"].values[::-1]                            # Changing order so first entry is earliest entry
data['dT'] = data["Temperature (°C)"].diff(periods=-20)
data['d^2T'] = data["dT"].diff(periods=20)

data = data.dropna()

features = data.iloc[1:32122, [3, 4]]
labels = data.iloc[1:32122, 2]

clf = tree.DecisionTreeClassifier(criterion="entropy", max_depth=3)
clf = clf.fit(features, labels)

c_true = data.iloc[32000:45880, 2]
data['Predicted Cooking'] = np.nan

### TESTING

for i in range(32000, 45880):
    data.iloc[i, 5] = clf.predict([[data.iloc[i, 3], data.iloc[i, 4]]])

c_pred = data.iloc[32000:45880, 5]

#print(data.head())
#print("Accuracy:", accuracy_score(c_true,c_pred))
#print("Confusion Matrix:")
#print(confusion_matrix(c_true,c_pred))
print("Classification Report:")
print(classification_report(c_true,c_pred))

## PREDICTING CURRENT DATA

day_data = pd.read_csv("day_data.csv", engine='python', usecols=[0])
day_data["Temperature (°C)"] = day_data["Temperature (°C)"].values[::-1]        # Changing order so first entry is earliest entry
day_data['dT'] = day_data["Temperature (°C)"].diff(periods=-20)
day_data['d^2T'] = day_data["dT"].diff(periods=20)
day_data = day_data.dropna()
day_data['Predicted Cooking'] = np.nan

for j in range(21, 3750):
    day_data.iloc[j, 3] = clf.predict([[day_data.iloc[j, 1], day_data.iloc[j, 2]]])

dc_pred = day_data.iloc[21:3750, 3]

message = "Today you cooked for " + str(round(sum(dc_pred)*(1/3))) + " minutes and used "
message = message + str(round(sum(dc_pred)*(1/3)*0.00595, 2)) + " kg of LPG. You have "
message = message + str(round(5 - ((sum(dc_pred) + sum(c_pred))*1/3*0.00595), 2)) + " kg of LPG remaining - approximately "
message = message + str(round((5 - ((sum(dc_pred) + sum(c_pred))*1/3*0.00595))*2.8, 2)) + " hours of cooking."

client = Client("ACea8b6d2fbbe28cfd28548023fc94f2b8", "07d544a8f0f6a237c50d248a6a00970f")

client.messages.create(to="+447989028158",
                       from_="+19548748373",
                       body=message)

os.remove("day_data.csv")
exec('temperature.py')
