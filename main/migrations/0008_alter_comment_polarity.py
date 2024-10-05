# Generated by Django 5.1.1 on 2024-10-02 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_comment_polarity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='polarity',
            field=models.CharField(choices=[('Негативный', 'negative'), ('Позитивный', 'positive'), ('Нейтральный', 'neutral'), ('Неизвестно', 'skip')], default='Неизвестно', max_length=100),
        ),
    ]
