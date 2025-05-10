from django.db import models

class User(models.Model):
    userID = models.CharField(primary_key=True, max_length=100)
    password = models.CharField(max_length=25, null=True, blank=True)
    name = models.CharField(max_length=25, null=True, blank=True)
    contact = models.CharField(max_length=25, null=True, blank=True)
    birth = models.CharField(max_length=25, null=True, blank=True)
    created_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.userID


class Heater(models.Model):
    id = models.BigAutoField(primary_key=True)  # 자동 순번
    heaterID = models.CharField(max_length=100)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)  # 수정 시간 자동 기록


class MoodLightStatus(models.Model):
    id = models.BigAutoField(primary_key=True)  # 자동 순번
    moodlighID = models.CharField(max_length=100)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    ON_OFF = models.BooleanField(null=True, blank=True)
    colorcode = models.CharField(max_length=25, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)  # 수정 시간 자동 기록


class SensorStatus(models.Model):
    id = models.BigAutoField(primary_key=True)  # 자동 순번
    sensorID = models.CharField(max_length=100)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    temperature = models.CharField(max_length=100, null=True, blank=True)
    humidity = models.CharField(max_length=100, null=True, blank=True)
    dust = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간 자동 기록


class CryDetection(models.Model):
    id = models.BigAutoField(primary_key=True)  # 자동 순번
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)  # 요청 시각 자동 기록
    audio_file_name = models.CharField(max_length=255)  # 업로드된 파일명
    status = models.CharField(max_length=20, default='pending')  # 처리 상태 (pending, completed, failed)
    cry_label = models.CharField(max_length=100, null=True, blank=True)  # 분석 결과 라벨
    confidence_score = models.CharField(max_length=100, null=True, blank=True)  # 신뢰도 (선택 사항)
    responded_at = models.DateTimeField(null=True, blank=True)  # 분석 완료 시각


class Pan(models.Model):
    id = models.BigAutoField(primary_key=True)
    panID = models.CharField(max_length=25)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)