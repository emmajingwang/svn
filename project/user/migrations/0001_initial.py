# Generated by Django 4.0.6 on 2022-07-18 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scheduledtask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('frequency', models.CharField(max_length=200)),
            ],
        ),
    ]
