from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import tensorflow as tf
import os

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
MODEL_PATH = 'model_sleep_disorder.keras'
stress_model = None
scaler_mean = None
scaler_scale = None

# Custom Layer wajb didefinisikan ulang untuk deserialization Keras
@tf.keras.utils.register_keras_serializable()
class AttentionLayer(tf.keras.layers.Layer):
    def __init__(self, units=16, **kwargs):
        super(AttentionLayer, self).__init__(**kwargs)
        self.units = units
        self.W = tf.keras.layers.Dense(units, activation='tanh')
        self.V = tf.keras.layers.Dense(1)

    def call(self, inputs):
        score = self.V(self.W(inputs))
        attention_weights = tf.nn.softmax(score, axis=-1)
        return inputs * attention_weights
    
    def get_config(self):
        config = super().get_config()
        config.update({'units': self.units})
        return config

# Fungsi untuk meload model TF saat server API di-start
@app.on_event("startup")
def load_keras_model():
    global stress_model, scaler_mean, scaler_scale
    if os.path.exists(MODEL_PATH):
        # Menyertakan AttentionLayer ke custom_objects langsung saat meload
        stress_model = tf.keras.models.load_model(MODEL_PATH, custom_objects={'AttentionLayer': AttentionLayer})
        scaler_mean = np.load('scaler_mean.npy')
        scaler_scale = np.load('scaler_scale.npy')
        print("✅ AI Engine + Scalers Berhasil Terdampar (Loaded)!")
    else:
        print("⚠️ Peringatan: File model.keras belum ada, hanya mode fallback.")

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
    global stress_model, scaler_mean, scaler_scale
    
    # Label dictionary
    labels = {0: "Normal/Aman", 1: "Risiko Insomnia", 2: "Risiko Sleep Apnea"}
    
    if stress_model is not None and scaler_mean is not None:
        # Ekstrak data menjadi numpy array input (Sesuai 7 Features)
        raw_input = np.array([[
            data.gender, data.age, data.sleep_duration, 
            data.physical_activity, data.heart_rate, data.daily_steps, data.stress_level
        ]])
        
        # Normalisasi menggunakan scaler dari training
        normalized_input = (raw_input - scaler_mean) / scaler_scale
        
        predictions = stress_model.predict(normalized_input)[0]
        predicted_class = int(np.argmax(predictions))
        
        # Formatting probabilities
        prob_breakdown = {
            "Normal": round(float(predictions[0]) * 100, 2),
            "Insomnia": round(float(predictions[1]) * 100, 2),
            "Sleep_Apnea": round(float(predictions[2]) * 100, 2)
        }
        
        confidence = prob_breakdown[list(prob_breakdown.keys())[predicted_class]]
        
        risk_level = "LOW"
        if predicted_class > 0:
            if confidence > 75: risk_level = "HIGH"
            elif confidence > 50: risk_level = "MEDIUM"
        
        return {
            "predicted_disorder": labels[predicted_class],
            "confidence_score": f"{confidence}%",
            "risk_level": risk_level,
            "probabilities": prob_breakdown,
            "model_type": "Keras Deep Learning (Custom Attention Layer)"
        }
    else:
        # Dummy Fallback
        return {
            "predicted_disorder": labels[1] if data.sleep_duration < 6.0 else labels[0], 
            "confidence_score": "80%",
            "risk_level": "MEDIUM",
            "probabilities": {"Normal": 20.0, "Insomnia": 80.0, "Sleep_Apnea": 0.0},
            "model_type": "Dummy Fallback Heuristics"
        }
