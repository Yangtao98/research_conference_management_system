# Generated by Django 4.1.2 on 2022-11-12 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_bid_num_active_bids'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='bid',
            old_name='submitted',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='conferencechair',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='miscuser',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='paper',
            old_name='submitted',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='submitted',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='review',
            old_name='body',
            new_name='review',
        ),
        migrations.RenameField(
            model_name='reviewer',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='systemadmin',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='bid',
            name='num_active_bids',
        ),
        migrations.RemoveField(
            model_name='review',
            name='bid',
        ),
        migrations.AddField(
            model_name='review',
            name='evaluation',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='review',
            name='paper',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='website.paper'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reviewer',
            name='current_workload',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='PaperReview',
        ),
    ]