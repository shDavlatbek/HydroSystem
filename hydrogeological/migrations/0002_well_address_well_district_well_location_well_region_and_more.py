# Generated by Django 5.0.6 on 2024-07-03 13:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('hydrogeological', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='well',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='well',
            name='district',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='well',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wells', to='common.location'),
        ),
        migrations.AddField(
            model_name='well',
            name='region',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='well',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.CreateModel(
            name='Coordinate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat_degree', models.IntegerField(blank=True, null=True)),
                ('lat_minute', models.IntegerField(blank=True, null=True)),
                ('lat_second', models.FloatField(blank=True, null=True)),
                ('lon_degree', models.IntegerField(blank=True, null=True)),
                ('lon_minute', models.IntegerField(blank=True, null=True)),
                ('lon_second', models.FloatField(blank=True, null=True)),
                ('x', models.IntegerField(blank=True, null=True)),
                ('y', models.IntegerField(blank=True, null=True)),
                ('well', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coordinates', to='hydrogeological.well')),
            ],
        ),
    ]