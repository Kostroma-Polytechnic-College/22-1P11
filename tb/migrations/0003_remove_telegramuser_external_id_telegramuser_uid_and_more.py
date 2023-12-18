# Generated by Django 4.2.8 on 2023-12-18 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0002_telegramuser_context'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegramuser',
            name='external_id',
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='uid',
            field=models.PositiveIntegerField(default=0, verbose_name='ИД пользователя'),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='name',
            field=models.TextField(default='Без имени', verbose_name='Имя'),
        ),
    ]
