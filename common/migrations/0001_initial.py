# Generated by Django 3.2.15 on 2022-08-14 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='记录创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='记录最后修改时间')),
            ],
        ),
    ]
