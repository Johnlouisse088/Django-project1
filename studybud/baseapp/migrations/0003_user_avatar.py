# Generated by Django 5.0.1 on 2024-03-13 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0002_user_bio_user_name_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]