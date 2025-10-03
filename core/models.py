from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import string, random




def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

class ShortURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True, default=generate_short_code)
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.IntegerField(default=0)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.short_code} → {self.original_url}"

    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
