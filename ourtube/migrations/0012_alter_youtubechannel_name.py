# Generated by Django 4.1.4 on 2023-01-21 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ourtube', '0011_remove_membership_unique_members_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youtubechannel',
            name='name',
            field=models.CharField(max_length=128),
        ),
    ]