# Generated by Django 3.2.15 on 2022-09-03 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CourseInfo',
            fields=[
                ('id', models.CharField(db_index=True, max_length=32, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(db_index=True, max_length=128)),
                ('type', models.CharField(db_index=True, max_length=32)),
                ('category', models.CharField(db_index=True, max_length=64)),
                ('test', models.CharField(db_index=True, max_length=8)),
                ('credit', models.FloatField(db_index=True)),
                ('nature', models.CharField(db_index=True, max_length=64)),
                ('period', models.FloatField(db_index=True)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CourseStatisticsResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statistics', models.TextField(default='{"all": {"total": 0, "exam": {}, "test": {}}}')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.courseinfo')),
            ],
        ),
    ]
