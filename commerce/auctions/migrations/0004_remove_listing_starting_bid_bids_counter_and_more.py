# Generated by Django 4.2.5 on 2023-09-13 08:56

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listing_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='starting_bid',
        ),
        migrations.AddField(
            model_name='bids',
            name='counter',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bids',
            name='listing',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auctions.listing'),
        ),
        migrations.AddField(
            model_name='bids',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='bids', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comments',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comments',
            name='comment',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AddField(
            model_name='comments',
            name='listing',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.listing'),
        ),
        migrations.AddField(
            model_name='listing',
            name='bid',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='listing',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 13, 8, 56, 32, 38773, tzinfo=datetime.timezone.utc)),
        ),
    ]
