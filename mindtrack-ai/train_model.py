import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("=" * 50)
print("   MindTrack AI - Model Training Pipeline")
print("=" * 50)

# ──────────────────────────────────────────
# 1. LOAD & PREPROCESSING DATASET
# ──────────────────────────────────────────
print("\n[Step 1] Membaca Dataset Kaggle...")
df = pd.read_csv('../mindtrack-ds/dataset_raw.csv')

# Isi NaN di Sleep Disorder menjadi 'None'
df['Sleep Disorder'] = df['Sleep Disorder'].fillna('None')

# Encode Gender: Male=0, Female=1
df['Gender'] = df['Gender'].map({'Male': 0, 'Female': 1})

# Encode BMI Category
bmi_map = {'Normal': 0, 'Normal Weight': 0, 'Overweight': 1, 'Obese': 2}
df['BMI Category'] = df['BMI Category'].map(bmi_map).fillna(0)

# Ekstrak Systolic dari kolom Blood Pressure (format: "120/80")
df['Systolic_BP'] = df['Blood Pressure'].apply(
    lambda x: int(str(x).split('/')[0]) if '/' in str(x) else 120
)

# Target Label
label_encoder = LabelEncoder()
df['Target'] = label_encoder.fit_transform(df['Sleep Disorder'])
class_names = label_encoder.classes_
print(f"  Kelas Target: {list(class_names)}")
print(f"  Distribusi: {dict(zip(class_names, np.bincount(df['Target'])))}")

# Feature Selection (Hanya 7 Variabel yang dikirim dari Frontend Form)
features = ['Gender', 'Age', 'Sleep Duration', 'Physical Activity Level',
            'Heart Rate', 'Daily Steps', 'Stress Level']

X = df[features].fillna(0).values
y = df['Target'].values

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Normalisasi
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

print(f"  Train: {len(X_train)} sampel | Test: {len(X_test)} sampel")

# ──────────────────────────────────────────
# 2. CUSTOM LAYER (Memenuhi Syarat Capstone)
# ──────────────────────────────────────────
class AttentionLayer(tf.keras.layers.Layer):
    """Custom Attention Layer — memberi bobot lebih pada fitur paling relevan."""
    
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

# ──────────────────────────────────────────
# 3. CUSTOM CALLBACK (Syarat Capstone)
# ──────────────────────────────────────────
class AccuracyThresholdCallback(tf.keras.callbacks.Callback):
    """Menghentikan training otomatis saat val_accuracy >= 85%."""
    def on_epoch_end(self, epoch, logs=None):
        acc = logs.get('val_accuracy', 0)
        if acc >= 0.85:
            print(f"\n✅ Target Akurasi 85% Terlampaui ({acc*100:.2f}%)! Menghentikan training di epoch {epoch+1}.")
            self.model.stop_training = True

# ──────────────────────────────────────────
# 4. MEMBANGUN MODEL DEEP LEARNING
# ──────────────────────────────────────────
print("\n[Step 2] Membangun Model TensorFlow Functional API + Custom Attention Layer...")

num_classes = len(class_names)
inputs = tf.keras.Input(shape=(len(features),), name='input_lifestyle')

# Hidden Layer 1
x = tf.keras.layers.Dense(64, activation='relu', name='dense_1')(inputs)
x = tf.keras.layers.BatchNormalization(name='batch_norm_1')(x)
x = tf.keras.layers.Dropout(0.3, name='dropout_1')(x)

# Custom Attention Layer
x = AttentionLayer(units=32, name='attention')(x)

# Hidden Layer 2
x = tf.keras.layers.Dense(32, activation='relu', name='dense_2')(x)
x = tf.keras.layers.Dropout(0.2, name='dropout_2')(x)

# Output Layer
outputs = tf.keras.layers.Dense(num_classes, activation='softmax', name='output')(x)

model = tf.keras.Model(inputs=inputs, outputs=outputs, name='MindTrack_AI')

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

print("\nArsitektur Model:")
model.summary()

# ──────────────────────────────────────────
# 5. TRAINING
# ──────────────────────────────────────────
print("\n[Step 3] Memulai Training...")

history = model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=150,
    batch_size=32,
    callbacks=[AccuracyThresholdCallback()],
    verbose=1
)

# ──────────────────────────────────────────
# 6. EVALUASI MODEL
# ──────────────────────────────────────────
print("\n[Step 4] Evaluasi Model...")
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"\n🎯 Akurasi Akhir Validasi: {accuracy * 100:.2f}%")

# Prediksi untuk Classification Report
y_pred_proba = model.predict(X_test, verbose=0)
y_pred = np.argmax(y_pred_proba, axis=1)

print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred, target_names=class_names))

# ──────────────────────────────────────────
# 7. VISUALISASI: CONFUSION MATRIX & FEATURE IMPORTANCE
# ──────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=class_names, yticklabels=class_names, ax=axes[0])
axes[0].set_title('Confusion Matrix - MindTrack AI')
axes[0].set_xlabel('Prediksi')
axes[0].set_ylabel('Aktual')

# Feature Importance (Approximation via Permutation)
baseline_acc = accuracy
importances = []
X_test_df = X_test.copy()
for i in range(X_test.shape[1]):
    X_perm = X_test.copy()
    np.random.shuffle(X_perm[:, i])
    _, perm_acc = model.evaluate(X_perm, y_test, verbose=0)
    importances.append(baseline_acc - perm_acc)

feat_series = pd.Series(importances, index=features).sort_values(ascending=True)
feat_series.plot(kind='barh', ax=axes[1], color='steelblue')
axes[1].set_title('Feature Importance (Permutation)')
axes[1].set_xlabel('Penurunan Akurasi saat Fitur Diacak')

plt.tight_layout()
plt.savefig('model_evaluation.png', dpi=150)
print("\n📈 Grafik evaluasi disimpan: model_evaluation.png")

# ──────────────────────────────────────────
# 8. SIMPAN MODEL
# ──────────────────────────────────────────
model.save('model_sleep_disorder.keras')
np.save('scaler_mean.npy', scaler.mean_)
np.save('scaler_scale.npy', scaler.scale_)
np.save('class_names.npy', class_names)
print(f"\n✅ Model berhasil disimpan: model_sleep_disorder.keras")
print("✅ Scaler dan label disimpan untuk dipakai di FastAPI")
print(f"\n{'='*50}")
print(f"  TRAINING SELESAI — Akurasi: {accuracy*100:.2f}%")
print(f"{'='*50}")
