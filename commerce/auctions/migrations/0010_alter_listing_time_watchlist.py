# Generated by Django 4.2.5 on 2023-09-15 08:44

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_listing_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 15, 8, 44, 54, 193, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing', models.ManyToManyField(blank=True, related_name='watch_listings', to='auctions.listing')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
