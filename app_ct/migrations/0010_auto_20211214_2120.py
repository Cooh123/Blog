# Generated by Django 3.1.7 on 2021-12-14 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_ct', '0009_auto_20211209_2211'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_at'], 'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
    ]
