import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from preprocess import load_and_preprocess

# Load data
df = load_and_preprocess('../data/sample_air_quality.csv')

X = df.drop('pm25', axis=1)
y = df['pm25']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Model
model = RandomForestRegressor(n_estimators=100)
model.fit(X_train, y_train)

# Save model
joblib.dump(model, '../models/model.pkl')

print("Model trained and saved!")
