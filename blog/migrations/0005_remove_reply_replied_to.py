# Generated by Django 4.1.5 on 2023-04-09 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_reply_replied_to'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reply',
            name='replied_to',
        ),
    ]
