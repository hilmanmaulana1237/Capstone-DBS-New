import pandas as pd
import numpy as np
import random

def generate_kaggle_like_dataset(filename='dataset_raw.csv'):
    np.random.seed(42)
    random.seed(42)
    n_samples = 400

    # Simulate realistic demographic & lifestyle data
    age = np.random.randint(18, 35, n_samples)
    genders = ['Male', 'Female', 'Other']
    gender = np.random.choice(genders, n_samples, p=[0.48, 0.48, 0.04])
    
    # Lifestyle factors
    sleep_hours = np.random.normal(6.8, 1.2, n_samples)
    sleep_hours = np.clip(sleep_hours, 4.0, 10.0)
    
    work_hours = np.random.normal(8.5, 2.0, n_samples)
    work_hours = np.clip(work_hours, 2.0, 14.0)
    
    # 1 to 5 scale
    physical_activity = np.random.randint(1, 6, n_samples)
    
    # High screen time common in modern Gen Z
    screen_time = np.random.normal(5.5, 2.5, n_samples)
    screen_time = np.clip(screen_time, 1.0, 12.0)
    
    # Missing values injection (Simulation of raw data)
    for _ in range(15):
        sleep_hours[random.randint(0, n_samples-1)] = np.nan
    for _ in range(10):
        work_hours[random.randint(0, n_samples-1)] = np.nan
        
    # Stress/Burnout Risk calculation (Hidden formula to simulate reality)
    base_stress = work_hours * 1.5 + screen_time * 1.2 - sleep_hours * 2.0 - physical_activity * 1.0
    # Add random noise
    base_stress += np.random.normal(0, 3.0, n_samples)
    
    # Normalize risk to 3 categories: Low, Medium, High
    # Let's say: < 5 is Low, 5 to 12 is Medium, > 12 is High
    risk_labels = []
    for s in base_stress:
        if pd.isna(s):
            risk_labels.append(np.nan)
        elif s < 3.0:
            risk_labels.append('Low')
        elif s < 10.0:
            risk_labels.append('Medium')
        else:
            risk_labels.append('High')
            
    # Assemble DataFrame
    df = pd.DataFrame({
        'Person_ID': range(1, n_samples + 1),
        'Age': age,
        'Gender': gender,
        'Sleep_Duration_Hours': sleep_hours,
        'Work_Study_Hours': work_hours,
        'Physical_Activity_Level': physical_activity,
        'Screen_Time_Hours': screen_time,
        'Mental_Fatigue_Score': base_stress,
        'Burnout_Risk': risk_labels
    })

    df.to_csv(filename, index=False)
    print(f"File {filename} berhasil didapat (disimulasikan dari Kaggle). Jumlah baris: {len(df)}")

if __name__ == "__main__":
    generate_kaggle_like_dataset()
