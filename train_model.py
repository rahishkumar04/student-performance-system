import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# Load cleaned data
df = pd.read_csv("cleaned_student.csv")

# Features & target
X = df[['study_hours', 'attendance', 'previous_marks']]
y = df['final_marks']

# Train model
model = LinearRegression()
model.fit(X, y)

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved!")