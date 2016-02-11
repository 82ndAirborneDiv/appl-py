# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-10 18:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AndroidProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_play_link', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='AndroidRelease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apk_file', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='IosProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bundle_id', models.CharField(max_length=50)),
                ('apple_app_store_link', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='IosRelease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ipa_file', models.FileField(upload_to='')),
                ('manifest_file', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectOverview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('icon', models.ImageField(upload_to='')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('source_code_link', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='ProjectScreenshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('screenshot', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('project_code_name', models.SlugField(max_length=30)),
                ('is_archived', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('major_version', models.PositiveSmallIntegerField()),
                ('minor_version', models.PositiveSmallIntegerField()),
                ('point_version', models.PositiveSmallIntegerField()),
                ('build_version', models.PositiveSmallIntegerField()),
                ('is_archived', models.BooleanField(default=False)),
                ('what_is_new', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='projectoverview',
            name='project_title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.ProjectTitle'),
        ),
        migrations.AddField(
            model_name='projectoverview',
            name='screenshots',
            field=models.ManyToManyField(to='apps.ProjectScreenshot'),
        ),
        migrations.AddField(
            model_name='iosrelease',
            name='release',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.Release'),
        ),
        migrations.AddField(
            model_name='iosproject',
            name='project_overview',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.ProjectOverview'),
        ),
        migrations.AddField(
            model_name='androidrelease',
            name='release',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apps.Release'),
        ),
    ]
