# Generated by Django 3.1.6 on 2021-03-02 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20210301_1616'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='current_price',
            new_name='current_offer',
        ),
    ]
