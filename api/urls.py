from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProtectedView, YoloRealtimeDetectView, ImageDetectionView, HistoryListView, DetectionDetailView, DetectionDeleteView
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='token_blacklist'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('detect/yolo-realtime/', YoloRealtimeDetectView.as_view(), name='yolorealtimedetection'),
    path("detect/image/", ImageDetectionView.as_view(), name="detect-image"),
    path('detect/detail/<int:pk>/', DetectionDetailView.as_view(), name='detect-detail'),
    path('detect/delete/<int:pk>/', DetectionDeleteView.as_view(), name='detect-delete'),
    path("history/", HistoryListView.as_view(), name="history"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
