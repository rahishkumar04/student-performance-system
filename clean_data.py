import pandas as pd

# AUTO DETECT SEPARATOR
df = pd.read_csv(r"C:\Users\rahish\OneDrive\student-por.csv", sep=None, engine='python')

print("Columns:", df.columns)

df = df[['studytime', 'absences', 'G1', 'G2', 'G3']]

df.rename(columns={
    'studytime': 'study_hours',
    'absences': 'attendance',
    'G1': 'previous_marks',
    'G3': 'final_marks'
}, inplace=True)

df['attendance'] = 100 - df['attendance']

df['study_hours'] = df['study_hours'] * 2

df.to_csv("cleaned_student.csv", index=False)

print("✅ Done")