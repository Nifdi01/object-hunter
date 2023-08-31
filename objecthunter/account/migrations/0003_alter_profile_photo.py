# Generated by Django 4.2.4 on 2023-08-31 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0002_alter_profile_photo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="photo",
            field=models.ImageField(
                blank=True,
                default="defaults/userprofile.png",
                upload_to="users/%Y/%m/%d/",
            ),
        ),
    ]
