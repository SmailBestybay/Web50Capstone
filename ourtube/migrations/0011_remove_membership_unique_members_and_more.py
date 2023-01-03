# Generated by Django 4.1.4 on 2023-01-03 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ourtube', '0010_alter_youtubechannel_channel_id_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='membership',
            name='unique_members',
        ),
        migrations.AddConstraint(
            model_name='membership',
            constraint=models.UniqueConstraint(fields=('user', 'feed'), name='unique_members'),
        ),
    ]
