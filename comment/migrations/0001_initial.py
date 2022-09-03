# Generated by Django 3.2.15 on 2022-09-03 07:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0001_initial'),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseComment',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='common.basemodel')),
                ('content', models.TextField(max_length=100)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('anonymous', models.BooleanField(default=False)),
                ('anonymous_name', models.CharField(db_index=True, default='匿名', max_length=32)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.courseinfo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('common.basemodel',),
        ),
    ]
