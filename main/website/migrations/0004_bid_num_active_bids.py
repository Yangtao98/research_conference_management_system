# Generated by Django 4.1.2 on 2022-11-11 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_paperreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='num_active_bids',
            field=models.IntegerField(default=0),
        ),
    ]