# Generated by Django 2.2 on 2019-04-10 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='register',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('mqttuser', models.CharField(max_length=100)),
                ('mqttpass', models.CharField(max_length=100)),
                ('port', models.IntegerField()),
            ],
        ),
    ]
