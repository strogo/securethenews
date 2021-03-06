# Generated by Django 2.2.14 on 2020-11-30 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0023_auto_20201130_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='onion_address',
            field=models.URLField(blank=True, help_text='The Onion address for this site. This field takes precedence over the Onion-Location header from scan results for determining if a site is available over Onion services.'),
        ),
    ]
