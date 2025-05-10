import os
import librosa
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
import pickle

# 데이터 경로
DATASET_PATH = "donateacry_corpus_cleaned_and_updated_data"

# 오디오 → mel-spectrogram 변환
def load_data(path):
    X, y = [], []
    for label in os.listdir(path):
        folder = os.path.join(path, label)
        for file in os.listdir(folder):
            if not file.endswith('.wav'):
                continue
            file_path = os.path.join(folder, file)
            audio, sr = librosa.load(file_path, sr=22050)
            mel = librosa.feature.melspectrogram(y=audio, sr=sr)
            mel_db = librosa.power_to_db(mel, ref=np.max)
            mel_db = np.resize(mel_db, (128, 128))
            X.append(mel_db)
            y.append(label)
    return np.array(X), np.array(y)

print("📁 데이터 불러오는 중...")
X, y = load_data(DATASET_PATH)
X = X[..., np.newaxis]  # CNN용 채널 추가

# 라벨 인코딩
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# train/test 나누기
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# 모델 구성
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(128,128,1)),
    tf.keras.layers.MaxPooling2D((2,2)),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2,2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(len(le.classes_), activation='softmax')
])

# 모델 컴파일 & 학습
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test))

# 모델 저장
model.save("baby_cry_model.h5")
with open("cubo/label_encoder.pkl", "wb") as f:
    pickle.dump(le, f)

print("✅ 모델 저장 완료! -> baby_cry_model.h5, label_encoder.pkl")
