# Generated by Django 4.1.2 on 2022-11-14 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_alter_review_paper'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent_review',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.review'),
        ),
    ]
