import librosa
import numpy as np
import tensorflow as tf
import pickle

# ✅ 모델 & 라벨 인코더 로드
model = tf.keras.models.load_model("cubo/baby_cry_model.h5")
with open("cubo/label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

# ✅ 테스트할 오디오 경로
test_audio_path = "test_audio/my_test3.wav"

# ✅ 전처리 함수 (학습 때랑 동일)
def preprocess_audio(file_path):
    y, sr = librosa.load(file_path, sr=22050)
    mel = librosa.feature.melspectrogram(y=y, sr=sr)
    mel_db = librosa.power_to_db(mel, ref=np.max)
    mel_db = np.resize(mel_db, (128, 128))
    mel_db = mel_db[np.newaxis, ..., np.newaxis]  # (1, 128, 128, 1)
    return mel_db

# ✅ 예측
x_input = preprocess_audio(test_audio_path)
prediction = model.predict(x_input)
predicted_label = label_encoder.inverse_transform([np.argmax(prediction)])[0]
confidence = np.max(prediction)

print(f"🧠 예측 결과: {predicted_label} ({confidence*100:.2f}%)")
