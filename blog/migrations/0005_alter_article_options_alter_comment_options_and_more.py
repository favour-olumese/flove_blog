# Generated by Django 4.1.5 on 2023-08-28 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_writer_saved_articles_alter_article_likes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-pub_date']},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-date']},
        ),
        migrations.AlterModelOptions(
            name='reply',
            options={'ordering': ['date']},
        ),
    ]