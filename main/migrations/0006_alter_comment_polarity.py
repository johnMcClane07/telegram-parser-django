# Generated by Django 5.1.1 on 2024-10-02 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_comment_polarity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='polarity',
            field=models.CharField(default='Неизвестно', max_length=100),
        ),
    ]