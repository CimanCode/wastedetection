from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from .models import History, Detection
from .serializers_auth import RegisterSerializer, LoginSerializer
from .serializers import HistorySerializer, DetectionSerializer
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser
from detection.inferences.yolo import predict_yolo_from_bytes
from rest_framework.permissions import AllowAny
from detection.inferences.detection import detect_and_map
from django.shortcuts import get_object_or_404

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProtectedView(APIView):
    def get(self, request):
        return Response({"message": f"Hello, {request.user.username}! You are authenticated."})
    

class YoloRealtimeDetectView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        image = request.FILES.get("frame")
        if not image:
            return Response({"error": "No frame uploaded"}, status=400)

        detections = predict_yolo_from_bytes(image.read())
        return Response({"detections": detections})
    
class ImageDetectionView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [AllowAny]

    def post(self, request):
        image_file = request.FILES.get("image")
        if not image_file:
            return Response({"error": "No image provided"}, status=400)

        result = detect_and_map(image_file, request.user)
        return Response(result)
    
class HistoryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            histories = History.objects.filter(user=user).order_by("-save_at")
            serializer = HistorySerializer(histories, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DetectionDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            detection = get_object_or_404(Detection, pk=pk, user=request.user)
            serializer = DetectionSerializer(detection)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class DetectionDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            detection = get_object_or_404(Detection, pk=pk, user=request.user)
            detection.delete()
            return Response({"message": "Detection deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        