# Generated by Django 4.1.7 on 2023-03-09 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat01', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatting',
            name='from_user',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='chatting',
            name='to',
            field=models.IntegerField(),
        ),
    ]