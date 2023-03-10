# Generated by Django 4.1.2 on 2022-11-01 09:32

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import website.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('user_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255, null=True)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'user_account_author',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('paper_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=255)),
                ('status', models.IntegerField(default=0)),
                ('submitted', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('upload', models.FileField(upload_to=website.models.user_directory_path)),
                ('submitting_author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.author')),
            ],
            options={
                'db_table': 'paper',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user_profile_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('profile_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'user_profile',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SystemAdmin',
            fields=[
                ('user_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255, null=True)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('user_role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.userprofile')),
            ],
            options={
                'db_table': 'user_account_system_admin',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Reviewer',
            fields=[
                ('user_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255, null=True)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('max_workload', models.IntegerField(default=0)),
                ('user_role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.userprofile')),
            ],
            options={
                'db_table': 'user_account_reviewer',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PaperReview',
            fields=[
                ('paperreview_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('status', models.IntegerField(default=0)),
                ('submitted', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('paper', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='website.paper')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='website.reviewer')),
            ],
            options={
                'db_table': 'paper_review',
            },
        ),
        migrations.CreateModel(
            name='PaperBid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(default=0)),
                ('paper', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='website.paper')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='website.reviewer')),
            ],
            options={
                'db_table': 'paper_bid',
            },
        ),
        migrations.CreateModel(
            name='PaperAuthor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='website.author')),
                ('paper', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='website.paper')),
            ],
            options={
                'db_table': 'paper_author',
            },
        ),
        migrations.CreateModel(
            name='MiscUser',
            fields=[
                ('user_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255, null=True)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('user_role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.userprofile')),
            ],
            options={
                'db_table': 'user_account_miscellaneous',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ConferenceChair',
            fields=[
                ('user_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255, null=True)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('user_role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.userprofile')),
            ],
            options={
                'db_table': 'user_account_conference_chair',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='author',
            name='user_role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.userprofile'),
        ),
    ]
