# Generated by Django 5.0.7 on 2024-07-29 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_region_district'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='district',
            options={'verbose_name': 'Tuman', 'verbose_name_plural': 'Tuman'},
        ),
        migrations.AlterModelOptions(
            name='region',
            options={'verbose_name': 'Viloyat', 'verbose_name_plural': 'Viloyat'},
        ),
    ]