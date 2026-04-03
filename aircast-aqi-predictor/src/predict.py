import joblib
import pandas as pd

model = joblib.load('../models/model.pkl')

def predict_pm25(temp, humidity, wind, hour, day):
    data = pd.DataFrame([{
        'temperature': temp,
        'humidity': humidity,
        'wind_speed': wind,
        'hour': hour,
        'day': day
    }])

    prediction = model.predict(data)[0]
    return prediction
