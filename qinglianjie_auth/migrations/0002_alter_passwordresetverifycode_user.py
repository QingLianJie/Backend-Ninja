# Generated by Django 3.2.15 on 2022-08-14 09:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qinglianjie_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetverifycode',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='请求重置密码的用户'),
        ),
    ]
