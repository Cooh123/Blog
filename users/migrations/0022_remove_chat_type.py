# Generated by Django 3.1.7 on 2022-02-02 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_chat_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='type',
        ),
    ]
