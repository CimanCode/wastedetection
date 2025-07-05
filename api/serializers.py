from rest_framework import serializers
from .models import User, TrashInfo, Detection, History

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class TrashInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrashInfo
        fields = '__all__'

class DetectionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    label = TrashInfoSerializer(read_only=True)

    class Meta:
        model = Detection
        fields = '__all__'

class HistorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    detection = DetectionSerializer(read_only=True)

    class Meta:
        model = History
        fields = '__all__'
