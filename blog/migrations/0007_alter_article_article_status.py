# Generated by Django 4.1.5 on 2023-02-23 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_article_article_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_status',
            field=models.CharField(choices=[('d', 'Draft'), ('p', 'Public'), ('u', 'Unlisted')], default='d', max_length=1),
        ),
    ]