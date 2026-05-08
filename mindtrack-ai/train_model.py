from pathlib import Path
import datetime
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.utils.class_weight import compute_class_weight


BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR.parent / "mindtrack-ds" / "dataset_raw_lama.csv"
LOG_ROOT = BASE_DIR / "logs" / "tensorboard"
MODEL_PATH = BASE_DIR / "model_sleep_disorder.keras"
EVALUATION_IMAGE_PATH = BASE_DIR / "model_evaluation.png"

SEED = 42
BATCH_SIZE = 16
EPOCHS = 500
TARGET_ACCURACY = 0.85
TARGET_MAE = 0.02
EARLY_STOPPING_PATIENCE = 80

np.random.seed(SEED)
tf.random.set_seed(SEED)

print("=" * 50)
print("   MindTrack AI - Custom GradientTape Training")
print("=" * 50)


def load_and_preprocess_dataset():
    print("\n[Step 1] Membaca Dataset Kaggle...")
    df = pd.read_csv(DATASET_PATH)

    df["Sleep Disorder"] = df["Sleep Disorder"].fillna("None")
    df["Gender"] = df["Gender"].map({"Male": 0, "Female": 1})

    bmi_map = {"Normal": 0, "Normal Weight": 0, "Overweight": 1, "Obese": 2}
    df["BMI Category"] = df["BMI Category"].map(bmi_map).fillna(0)

    df["Systolic_BP"] = df["Blood Pressure"].apply(
        lambda value: int(str(value).split("/")[0]) if "/" in str(value) else 120
    )

    label_encoder = LabelEncoder()
    df["Target"] = label_encoder.fit_transform(df["Sleep Disorder"])
    class_names = label_encoder.classes_

    print(f"  Kelas Target: {list(class_names)}")
    print(f"  Distribusi: {dict(zip(class_names, np.bincount(df['Target'])))}")

    features = [
        "Gender",
        "Age",
        "Sleep Duration",
        "Physical Activity Level",
        "Heart Rate",
        "Daily Steps",
        "Stress Level",
    ]

    x = df[features].fillna(0).values.astype("float32")
    y = df["Target"].values.astype("int32")

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=SEED,
        stratify=y,
    )

    y_train_oh = tf.keras.utils.to_categorical(y_train, num_classes=len(class_names)).astype(
        "float32"
    )
    y_test_oh = tf.keras.utils.to_categorical(y_test, num_classes=len(class_names)).astype(
        "float32"
    )

    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train).astype("float32")
    x_test = scaler.transform(x_test).astype("float32")

    print(f"  Train: {len(x_train)} sampel | Test: {len(x_test)} sampel")
    return features, class_names, scaler, x_train, x_test, y_train, y_test, y_train_oh, y_test_oh


class AttentionLayer(tf.keras.layers.Layer):
    """Custom attention gate untuk memberi bobot pada representasi fitur."""

    def __init__(self, units=16, **kwargs):
        super().__init__(**kwargs)
        self.units = units
        self.projection = tf.keras.layers.Dense(units, activation="tanh")
        self.score = tf.keras.layers.Dense(1)

    def call(self, inputs):
        attention_logits = self.score(self.projection(inputs))
        attention_weights = tf.nn.sigmoid(attention_logits)
        return inputs * attention_weights

    def get_config(self):
        config = super().get_config()
        config.update({"units": self.units})
        return config


class AccuracyThresholdCallback(tf.keras.callbacks.Callback):
    """Custom callback untuk menghentikan training saat target Capstone tercapai."""

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        acc = logs.get("val_accuracy", 0)
        mae = logs.get("val_mae", 1.0)
        if acc >= TARGET_ACCURACY and mae <= TARGET_MAE:
            print(
                "\nTarget Capstone tercapai! "
                f"Val Acc: {acc * 100:.2f}%, Val MAE: {mae:.4f}. "
                f"Menghentikan training di epoch {epoch + 1}."
            )
            self.model.stop_training = True


def build_model(input_dim, num_classes):
    print("\n[Step 2] Membangun Model TensorFlow Functional API + Custom Attention Layer...")
    inputs = tf.keras.Input(shape=(input_dim,), name="input_lifestyle")
    x = tf.keras.layers.Dense(128, activation="relu", name="dense_1")(inputs)
    x = tf.keras.layers.BatchNormalization(name="batch_norm_1")(x)
    x = AttentionLayer(units=64, name="attention")(x)
    x = tf.keras.layers.Dense(64, activation="relu", name="dense_2")(x)
    outputs = tf.keras.layers.Dense(num_classes, activation="softmax", name="output")(x)
    model = tf.keras.Model(inputs=inputs, outputs=outputs, name="MindTrack_AI")
    print("\nArsitektur Model:")
    model.summary()
    return model


def reset_metrics(metrics):
    for metric in metrics:
        if hasattr(metric, "reset_state"):
            metric.reset_state()
        else:
            metric.reset_states()


def make_weighted_loss(loss_fn, y_true, y_pred, sample_weight=None):
    per_sample_loss = loss_fn(y_true, y_pred)
    if sample_weight is None:
        return tf.reduce_mean(per_sample_loss)

    sample_weight = tf.cast(sample_weight, per_sample_loss.dtype)
    weighted_loss = per_sample_loss * sample_weight
    return tf.reduce_sum(weighted_loss) / tf.maximum(tf.reduce_sum(sample_weight), 1.0)


def class_index_mae(y_true, y_pred, num_classes):
    # Capstone asks for MAE on a multiclass target, so we measure normalized
    # distance between true and predicted class indexes instead of probability MAE.
    true_class = tf.argmax(y_true, axis=1, output_type=tf.int32)
    pred_class = tf.argmax(y_pred, axis=1, output_type=tf.int32)
    absolute_error = tf.abs(tf.cast(true_class - pred_class, tf.float32))
    return tf.reduce_mean(absolute_error / max(num_classes, 1))


def train_with_gradient_tape(model, train_ds, val_ds, num_classes):
    print("\n[Step 3] Memulai custom training loop dengan tf.GradientTape...")
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
    loss_fn = tf.keras.losses.CategoricalCrossentropy(
        reduction=tf.keras.losses.Reduction.NONE
    )

    train_loss = tf.keras.metrics.Mean(name="train_loss")
    train_accuracy = tf.keras.metrics.CategoricalAccuracy(name="train_accuracy")
    train_mae = tf.keras.metrics.Mean(name="train_class_index_mae")
    val_loss = tf.keras.metrics.Mean(name="val_loss")
    val_accuracy = tf.keras.metrics.CategoricalAccuracy(name="val_accuracy")
    val_mae = tf.keras.metrics.Mean(name="val_class_index_mae")

    log_dir = LOG_ROOT / datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    train_writer = tf.summary.create_file_writer(str(log_dir / "train"))
    val_writer = tf.summary.create_file_writer(str(log_dir / "validation"))
    print(f"  TensorBoard log dir: {log_dir}")

    callback = AccuracyThresholdCallback()
    callback.set_model(model)
    callback.on_train_begin({})
    model.stop_training = False
    best_weights = model.get_weights()
    best_logs = None
    best_epoch = 0
    epochs_without_improvement = 0

    history = {
        "loss": [],
        "accuracy": [],
        "mae": [],
        "val_loss": [],
        "val_accuracy": [],
        "val_mae": [],
    }

    for epoch in range(1, EPOCHS + 1):
        reset_metrics([train_loss, train_accuracy, train_mae, val_loss, val_accuracy, val_mae])

        for x_batch, y_batch, weight_batch in train_ds:
            with tf.GradientTape() as tape:
                predictions = model(x_batch, training=True)
                loss = make_weighted_loss(loss_fn, y_batch, predictions, weight_batch)
                if model.losses:
                    loss += tf.add_n(model.losses)

            gradients = tape.gradient(loss, model.trainable_variables)
            optimizer.apply_gradients(zip(gradients, model.trainable_variables))

            train_loss.update_state(loss)
            train_accuracy.update_state(y_batch, predictions, sample_weight=weight_batch)
            train_mae.update_state(class_index_mae(y_batch, predictions, num_classes))

        for x_batch, y_batch in val_ds:
            predictions = model(x_batch, training=False)
            loss = make_weighted_loss(loss_fn, y_batch, predictions)
            val_loss.update_state(loss)
            val_accuracy.update_state(y_batch, predictions)
            val_mae.update_state(class_index_mae(y_batch, predictions, num_classes))

        epoch_logs = {
            "loss": float(train_loss.result().numpy()),
            "accuracy": float(train_accuracy.result().numpy()),
            "mae": float(train_mae.result().numpy()),
            "val_loss": float(val_loss.result().numpy()),
            "val_accuracy": float(val_accuracy.result().numpy()),
            "val_mae": float(val_mae.result().numpy()),
        }

        for key, value in epoch_logs.items():
            history[key].append(value)

        with train_writer.as_default():
            tf.summary.scalar("loss", epoch_logs["loss"], step=epoch)
            tf.summary.scalar("accuracy", epoch_logs["accuracy"], step=epoch)
            tf.summary.scalar("mae", epoch_logs["mae"], step=epoch)

        with val_writer.as_default():
            tf.summary.scalar("loss", epoch_logs["val_loss"], step=epoch)
            tf.summary.scalar("accuracy", epoch_logs["val_accuracy"], step=epoch)
            tf.summary.scalar("mae", epoch_logs["val_mae"], step=epoch)

        print(
            f"Epoch {epoch:03d}/{EPOCHS} | "
            f"loss={epoch_logs['loss']:.4f} | "
            f"acc={epoch_logs['accuracy']:.4f} | "
            f"mae={epoch_logs['mae']:.4f} | "
            f"val_loss={epoch_logs['val_loss']:.4f} | "
            f"val_acc={epoch_logs['val_accuracy']:.4f} | "
            f"val_mae={epoch_logs['val_mae']:.4f}"
        )

        is_better = (
            best_logs is None
            or epoch_logs["val_accuracy"] > best_logs["val_accuracy"]
            or (
                epoch_logs["val_accuracy"] == best_logs["val_accuracy"]
                and epoch_logs["val_mae"] < best_logs["val_mae"]
            )
        )
        if is_better:
            best_weights = model.get_weights()
            best_logs = epoch_logs.copy()
            best_epoch = epoch
            epochs_without_improvement = 0
        else:
            epochs_without_improvement += 1

        callback.on_epoch_end(epoch - 1, epoch_logs)
        if model.stop_training:
            break
        if epochs_without_improvement >= EARLY_STOPPING_PATIENCE:
            print(
                f"\nTidak ada peningkatan validasi selama {EARLY_STOPPING_PATIENCE} epoch. "
                f"Restore bobot terbaik dari epoch {best_epoch}."
            )
            break

    callback.on_train_end({})
    train_writer.close()
    val_writer.close()
    if best_logs:
        model.set_weights(best_weights)
        print(
            f"\nBobot terbaik direstore dari epoch {best_epoch}: "
            f"val_acc={best_logs['val_accuracy']:.4f}, val_mae={best_logs['val_mae']:.4f}"
        )
    return history, log_dir


def evaluate_with_custom_loop(model, val_ds, num_classes):
    loss_fn = tf.keras.losses.CategoricalCrossentropy(
        reduction=tf.keras.losses.Reduction.NONE
    )
    loss_metric = tf.keras.metrics.Mean(name="eval_loss")
    accuracy_metric = tf.keras.metrics.CategoricalAccuracy(name="eval_accuracy")
    mae_metric = tf.keras.metrics.Mean(name="eval_class_index_mae")
    predictions_all = []

    for x_batch, y_batch in val_ds:
        predictions = model(x_batch, training=False)
        loss = make_weighted_loss(loss_fn, y_batch, predictions)
        loss_metric.update_state(loss)
        accuracy_metric.update_state(y_batch, predictions)
        mae_metric.update_state(class_index_mae(y_batch, predictions, num_classes))
        predictions_all.append(predictions.numpy())

    return {
        "loss": float(loss_metric.result().numpy()),
        "accuracy": float(accuracy_metric.result().numpy()),
        "mae": float(mae_metric.result().numpy()),
        "predictions": np.vstack(predictions_all),
    }


def plot_evaluation(features, class_names, model, x_test, y_test, y_test_oh, accuracy):
    y_pred_proba = model(tf.convert_to_tensor(x_test, dtype=tf.float32), training=False).numpy()
    y_pred = np.argmax(y_pred_proba, axis=1)

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=class_names))

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=class_names,
        yticklabels=class_names,
        ax=axes[0],
    )
    axes[0].set_title("Confusion Matrix - MindTrack AI")
    axes[0].set_xlabel("Prediksi")
    axes[0].set_ylabel("Aktual")

    importances = []
    rng = np.random.default_rng(SEED)
    for feature_index in range(x_test.shape[1]):
        x_perm = x_test.copy()
        rng.shuffle(x_perm[:, feature_index])
        perm_proba = model(tf.convert_to_tensor(x_perm, dtype=tf.float32), training=False).numpy()
        perm_pred = np.argmax(perm_proba, axis=1)
        perm_acc = np.mean(perm_pred == y_test)
        importances.append(accuracy - perm_acc)

    feat_series = pd.Series(importances, index=features).sort_values(ascending=True)
    feat_series.plot(kind="barh", ax=axes[1], color="steelblue")
    axes[1].set_title("Feature Importance (Permutation)")
    axes[1].set_xlabel("Penurunan Akurasi saat Fitur Diacak")

    plt.tight_layout()
    plt.savefig(EVALUATION_IMAGE_PATH, dpi=150)
    print(f"\nGrafik evaluasi disimpan: {EVALUATION_IMAGE_PATH}")


def save_artifacts(model, scaler, class_names):
    model.save(str(MODEL_PATH))
    np.save(BASE_DIR / "scaler_mean.npy", scaler.mean_)
    np.save(BASE_DIR / "scaler_scale.npy", scaler.scale_)
    np.save(BASE_DIR / "class_names.npy", class_names)
    print(f"\nModel berhasil disimpan: {MODEL_PATH}")
    print("Scaler dan label disimpan untuk dipakai di FastAPI")


def main():
    (
        features,
        class_names,
        scaler,
        x_train,
        x_test,
        y_train,
        y_test,
        y_train_oh,
        y_test_oh,
    ) = load_and_preprocess_dataset()

    class_weights = compute_class_weight("balanced", classes=np.unique(y_train), y=y_train)
    class_weight_dict = dict(enumerate(class_weights))
    sample_weights = np.array([class_weight_dict[label] for label in y_train], dtype="float32")

    train_ds = (
        tf.data.Dataset.from_tensor_slices((x_train, y_train_oh, sample_weights))
        .shuffle(buffer_size=len(x_train), seed=SEED)
        .batch(BATCH_SIZE)
    )
    val_ds = tf.data.Dataset.from_tensor_slices((x_test, y_test_oh)).batch(BATCH_SIZE)

    model = build_model(input_dim=len(features), num_classes=len(class_names))
    _, log_dir = train_with_gradient_tape(model, train_ds, val_ds, num_classes=len(class_names))

    print("\n[Step 4] Evaluasi Model dengan custom evaluation loop...")
    eval_result = evaluate_with_custom_loop(model, val_ds, num_classes=len(class_names))
    accuracy = eval_result["accuracy"]
    mae = eval_result["mae"]
    print(f"\nAkurasi Akhir Validasi: {accuracy * 100:.2f}% | MAE Akhir: {mae:.4f}")

    print("\n[Step 5] Visualisasi evaluasi dan feature importance...")
    plot_evaluation(features, class_names, model, x_test, y_test, y_test_oh, accuracy)

    print("\n[Step 6] Simpan model dan artefak inference...")
    save_artifacts(model, scaler, class_names)

    print(f"\nTensorBoard siap dibuka dengan: tensorboard --logdir {LOG_ROOT}")
    print(f"Log run terbaru: {log_dir}")
    print(f"\n{'=' * 50}")
    print(f"  TRAINING SELESAI - Akurasi: {accuracy * 100:.2f}% | MAE: {mae:.4f}")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
    main()
