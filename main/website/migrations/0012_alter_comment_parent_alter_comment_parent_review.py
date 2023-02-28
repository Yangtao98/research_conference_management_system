# Generated by Django 4.1.2 on 2022-11-14 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_alter_comment_parent_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='replies', to='website.comment'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent_review',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='website.review'),
        ),
    ]
