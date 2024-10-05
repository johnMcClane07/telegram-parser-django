from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

class CustomUser(AbstractUser):
    """
    Модель пользователя, расширенная полями "department" (отдел) и "position" (должность).

    Переопределенный метод save, который обрабатывает пароль
    перед сохранением модели. Если пароль не шифрован, то
    шифрует его.
    """

    department = models.CharField(max_length=255, verbose_name='Отдел')
    position = models.CharField(max_length=255, verbose_name='Должность')

    USERNAME_FIELD = "username"

    def save(self, *args, **kwargs):

        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)