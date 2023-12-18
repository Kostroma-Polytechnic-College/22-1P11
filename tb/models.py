from django.db.models import Model, ForeignKey, CASCADE, PositiveIntegerField, TextField, BooleanField, DateTimeField
from datetime import datetime as dt

class TelegramUser(Model):
    uid = PositiveIntegerField(
        default=0,
        verbose_name="ИД пользователя",
    )

    name = TextField(
        default = "Без имени",
        verbose_name="Имя"
    )

    is_admin = BooleanField(
        default=False,
        verbose_name="Администратор"
    )

    context = TextField(
        default='{}',
        verbose_name="Контекст"
    )

    def __str__(self):
        return f'{self.uid} - {self.name}'

    class Meta:
        verbose_name = 'Пользователь ТГ'
        verbose_name_plural = 'Пользователи ТГ'

class Travel(Model):
    user = ForeignKey(
        TelegramUser, 
        on_delete=CASCADE,
        verbose_name="Поездка")
    
    start_datetime = DateTimeField(
        default=dt.now(),
        verbose_name="Дата и время начала выезда"
    )
    end_datetime = DateTimeField(
        default=dt.now(),
        verbose_name="Дата и время окончания выезда"
    )

    def __str__(self):
        return f'{self.start_datetime.date()}: {self.start_datetime.strftime("%H:%M")}-{self.end_datetime.strftime("%H:%M")}'

    class Meta:
        verbose_name = 'Поездка'
        verbose_name_plural = 'Поездки'