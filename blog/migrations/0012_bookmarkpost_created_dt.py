# Generated by Django 3.0.3 on 2022-01-09 19:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20211208_0109'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmarkpost',
            name='created_dt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]