# Generated by Django 3.1.7 on 2022-01-17 08:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0014_bookmarkuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookmarkuser',
            name='obj',
        ),
        migrations.AddField(
            model_name='bookmarkuser',
            name='who_added',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='who_added', to='auth.user', verbose_name='Кого добавили'),
            preserve_default=False,
        ),
    ]
