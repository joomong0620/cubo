from rest_framework import serializers
from .models import User, Heater, MoodLightStatus, SensorStatus, CryDetection

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class HeaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heater
        fields = '__all__'

class MoodLightStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodLightStatus
        fields = '__all__'

class SensorStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorStatus
        fields = '__all__'

class CryDetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryDetection
        fields = '__all__'
