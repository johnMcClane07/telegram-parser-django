# Generated by Django 5.1.1 on 2024-10-02 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_comment_polarity'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnsatisfiedCustomers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='sender_phone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
