# Generated by Django 5.1.1 on 2024-10-02 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_comment_polarity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='polarity',
            field=models.CharField(choices=[('negative', 'Негативный'), ('positive', 'Позитивный'), ('neutral', 'Нейтральный'), ('skip', 'Неизвестно')], default='Неизвестно', max_length=100),
        ),
    ]
