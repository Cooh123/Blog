# Generated by Django 3.0.3 on 2022-01-09 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20211220_0001'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(default='Леша', max_length=20),
            preserve_default=False,
        ),
    ]