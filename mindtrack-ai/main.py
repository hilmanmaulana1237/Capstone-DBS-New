from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import tensorflow as tf
import os
from pathlib import Path

app = FastAPI(title="MindTrack AI Endpoint")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PatientData(BaseModel):
    gender: int  # 0: Male, 1: Female
    age: int
    sleep_duration: float
    physical_activity: int
    heart_rate: int
    daily_steps: int
    stress_level: int = 5

# Variabel Global untuk menyimpan model & scaler
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / 'model_sleep_disorder.keras'
stress_model = None
scaler_mean = None
scaler_scale = None
class_names = None

# Custom Layer wajb didefinisikan ulang untuk deserialization Keras
@tf.keras.utils.register_keras_serializable()
class AttentionLayer(tf.keras.layers.Layer):
    def __init__(self, units=16, **kwargs):
        super().__init__(**kwargs)
        self.units = units
        self.projection = tf.keras.layers.Dense(units, activation='tanh')
        self.score = tf.keras.layers.Dense(1)

    def call(self, inputs):
        attention_logits = self.score(self.projection(inputs))
        attention_weights = tf.nn.sigmoid(attention_logits)
        return inputs * attention_weights
    
    def get_config(self):
        config = super().get_config()
        config.update({'units': self.units})
        return config

# Fungsi untuk meload model TF saat server API di-start
@app.on_event("startup")
def load_keras_model():
    global stress_model, scaler_mean, scaler_scale, class_names
    if os.path.exists(MODEL_PATH):
        # Menyertakan AttentionLayer ke custom_objects langsung saat meload
        stress_model = tf.keras.models.load_model(str(MODEL_PATH), custom_objects={'AttentionLayer': AttentionLayer})
        scaler_mean = np.load(BASE_DIR / 'scaler_mean.npy')
        scaler_scale = np.load(BASE_DIR / 'scaler_scale.npy')
        class_names = np.load(BASE_DIR / 'class_names.npy', allow_pickle=True)
        print("[OK] AI Engine + Scalers Berhasil Loaded.")
    else:
        print("[WARN] File model.keras belum ada, hanya mode fallback.")

@app.get("/")
def home():
    return {"status": "MindTrack AI Microservice Active", "engine": "TensorFlow FastAPI"}

@app.get("/model-info")
def get_model_info():
    global stress_model
    if stress_model:
        return {
            "status": "Ready",
            "layers": len(stress_model.layers),
            "input_shape": list(stress_model.input_shape),
            "name": stress_model.name,
            "architecture": "Functional API with Custom Attention Layer L1"
        }
    return {"status": "Fallback / Model Not Found"}

@app.post("/predict")
def predict_risk(data: PatientData):
    global stress_model, scaler_mean, scaler_scale, class_names
    
    def display_label(label):
        label_text = str(label)
        if label_text in ["None", "Aman", "Normal"]:
            return "Normal/Aman"
        if label_text == "Insomnia":
            return "Risiko Insomnia"
        if label_text == "Sleep Apnea":
            return "Risiko Sleep Apnea"
        return label_text

    def probability_key(label):
        label_text = str(label)
        if label_text in ["None", "Aman", "Normal"]:
            return "Normal"
        return label_text.replace(" ", "_")
    
    if stress_model is not None and scaler_mean is not None and class_names is not None:
        # Ekstrak data menjadi numpy array input (Sesuai 7 Features)
        raw_input = np.array([[
            data.gender, data.age, data.sleep_duration, 
            data.physical_activity, data.heart_rate, data.daily_steps, data.stress_level
        ]])
        
        # Normalisasi menggunakan scaler dari training
        normalized_input = (raw_input - scaler_mean) / scaler_scale
        
        predictions = stress_model.predict(normalized_input)[0]
        predicted_class = int(np.argmax(predictions))
        predicted_label = class_names[predicted_class]
        
        # Formatting probabilities
        prob_breakdown = {
            probability_key(label): round(float(predictions[index]) * 100, 2)
            for index, label in enumerate(class_names)
        }
        
        confidence = round(float(predictions[predicted_class]) * 100, 2)
        
        risk_level = "LOW"
        if display_label(predicted_label) != "Normal/Aman":
            if confidence > 75: risk_level = "HIGH"
            elif confidence > 50: risk_level = "MEDIUM"
        
        return {
            "predicted_disorder": display_label(predicted_label),
            "confidence_score": f"{confidence}%",
            "risk_level": risk_level,
            "probabilities": prob_breakdown,
            "model_type": "Keras Deep Learning (Custom Attention Layer)"
        }
    else:
        # Dummy Fallback
        return {
            "predicted_disorder": "Risiko Insomnia" if data.sleep_duration < 6.0 else "Normal/Aman", 
            "confidence_score": "80%",
            "risk_level": "MEDIUM",
            "probabilities": {"Normal": 20.0, "Insomnia": 80.0, "Sleep_Apnea": 0.0},
            "model_type": "Dummy Fallback Heuristics"
        }
