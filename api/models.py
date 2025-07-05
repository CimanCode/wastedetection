from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class TrashInfo(models.Model):
    label = models.CharField(max_length=20, primary_key=True)
    danger_level = models.CharField(max_length=20, choices=[
        ('RENDAH', 'Rendah'),
        ('SEDANG', 'Sedang'),
        ('TINGGI', 'Tinggi'),
    ])
    mitigation = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.label

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('Username is required')
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class Detection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.ForeignKey(TrashInfo, on_delete=models.CASCADE)
    image_path = models.CharField(max_length=255, null=True, blank=True)
    result_image_path = models.CharField(max_length=255, null=True, blank=True)
    detection_time = models.DateTimeField(null=True, blank=True)
    detection_speed = models.FloatField(null=True, blank=True)
    total_confidence = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.label} by {self.user.username}"
    
class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    detection = models.ForeignKey(Detection, on_delete=models.CASCADE)
    save_at = models.DateTimeField()

    def __str__(self):
        return f"History of {self.user.username} at {self.save_at}"