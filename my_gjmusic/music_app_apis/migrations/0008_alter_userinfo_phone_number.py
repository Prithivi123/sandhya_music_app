# Generated by Django 4.1.3 on 2023-04-02 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_app_apis', '0007_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='phone_number',
            field=models.BigIntegerField(),
        ),
    ]