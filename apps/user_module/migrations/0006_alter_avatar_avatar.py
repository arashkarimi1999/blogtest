# Generated by Django 4.2.5 on 2023-10-09 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_module', '0005_remove_user_avatars_avatar_user_alter_avatar_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='User-avatar', verbose_name='avatar gallery '),
        ),
    ]
