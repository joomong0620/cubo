import os
import numpy as np
import librosa
from pydub import AudioSegment
import tensorflow as tf
import pickle
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now
from .models import User, Heater, MoodLightStatus, SensorStatus, CryDetection
from .serializers import (
    UserSerializer, HeaterSerializer, MoodLightStatusSerializer,
    SensorStatusSerializer, CryDetectionSerializer
)

# GPU 사용 안 할 경우 명시적으로 비활성화
tf.config.set_visible_devices([], 'GPU')

MODEL_PATH = 'D:/cubo/cubo/baby_cry_model.h5'
ENCODER_PATH = 'D:/cubo/cubo/label_encoder.pkl'

model = tf.keras.models.load_model(MODEL_PATH)
with open(ENCODER_PATH, 'rb') as f:
    label_encoder = pickle.load(f)


def preprocess_audio(file_path):
    # wav 파일을 pydub로 읽기
    audio = AudioSegment.from_file(file_path, format="wav")

    # mono 변환 및 numpy 배열로 변환
    audio = audio.set_channels(1)
    samples = np.array(audio.get_array_of_samples()).astype(np.float32)

    # 샘플링 레이트 추출
    sr = audio.frame_rate  # 일반적으로 44100Hz

    # 멜스펙트로그램 변환
    mel = librosa.feature.melspectrogram(y=samples, sr=sr)
    mel_db = librosa.power_to_db(mel, ref=np.max)
    mel_db = np.resize(mel_db, (128, 128))
    mel_db = mel_db[np.newaxis, ..., np.newaxis]

    return mel_db

def predict_cry(file_path):
    processed_audio = preprocess_audio(file_path)
    predictions = model.predict(processed_audio)
    predicted_index = np.argmax(predictions, axis=1)[0]
    predicted_label = label_encoder.inverse_transform([predicted_index])[0]
    confidence = float(np.max(predictions))
    return predicted_label, confidence


class CryDetectionViewSet(viewsets.ModelViewSet):
    queryset = CryDetection.objects.all()
    serializer_class = CryDetectionSerializer

    @action(detail=False, methods=['post'])
    def upload(self, request):
        user_id = request.data.get('userID')
        audio_file = request.FILES.get('file')

        if not user_id or not audio_file:
            return Response({'error': 'userID와 file은 필수입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        upload_dir = 'uploaded_audio'
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, audio_file.name)

        with open(file_path, 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)

        cry_detection = CryDetection.objects.create(
            userID_id=user_id,
            audio_file_name=audio_file.name,
            status='pending'
        )

        try:
            cry_label, confidence_score = predict_cry(file_path)
            cry_detection.status = 'completed'
            cry_detection.cry_label = cry_label
            cry_detection.confidence_score = str(confidence_score)
            cry_detection.responded_at = now()
            cry_detection.save()
        except Exception as e:
            cry_detection.status = 'failed'
            cry_detection.save()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = self.get_serializer(cry_detection)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class HeaterViewSet(viewsets.ModelViewSet):
    queryset = Heater.objects.all()
    serializer_class = HeaterSerializer


class MoodLightStatusViewSet(viewsets.ModelViewSet):
    queryset = MoodLightStatus.objects.all()
    serializer_class = MoodLightStatusSerializer


class SensorStatusViewSet(viewsets.ModelViewSet):
    queryset = SensorStatus.objects.all()
    serializer_class = SensorStatusSerializer
