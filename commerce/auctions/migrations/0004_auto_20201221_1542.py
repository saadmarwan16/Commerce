# Generated by Django 3.1.4 on 2020-12-21 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20201221_0844'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auctionlistings',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='bids',
            old_name='auction_id',
            new_name='auction',
        ),
        migrations.RenameField(
            model_name='bids',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='auction_id',
            new_name='auction',
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='watchlist',
            old_name='auction_id',
            new_name='auction',
        ),
        migrations.RenameField(
            model_name='watchlist',
            old_name='user_id',
            new_name='user',
        ),
    ]