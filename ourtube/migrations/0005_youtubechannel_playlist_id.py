# Generated by Django 4.0.6 on 2022-12-22 06:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ourtube', '0004_youtubechannel_cahnnel_id_youtubechannel_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtubechannel',
            name='playlist_id',
            field=models.CharField(default=django.utils.timezone.now, max_length=128),
            preserve_default=False,
        ),
    ]
