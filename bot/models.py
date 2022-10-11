from django.db import models

from core.models import User


# Create your models here.
class TgUser(models.Model):
    """Модель пользователя бота"""
    class Meta:
        verbose_name = "Пользователь бота"
        verbose_name_plural = "Пользователи бота"

    telegram_chat_id = models.IntegerField(verbose_name="ID телеграмм чата")
    telegram_user_id = models.IntegerField(verbose_name="ID телеграмма пользователя")
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.PROTECT, null=True, blank=True)
    verification_code = models.CharField(verbose_name="Код верификации", max_length=51)


class TgProcessedUpdate(models.Model):
    """Модель для запоминания последнего обработанного сообщения"""
    update_id = models.IntegerField(verbose_name="ID последнего обработанного сообщения")
