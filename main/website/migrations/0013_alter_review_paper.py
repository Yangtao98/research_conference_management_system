# Generated by Django 4.1.2 on 2022-11-15 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_alter_comment_parent_alter_comment_parent_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='paper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='child_review', to='website.paper'),
        ),
    ]
