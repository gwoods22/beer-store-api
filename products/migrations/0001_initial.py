# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-02 11:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('size', models.CharField(max_length=255)),
                ('beer_id', models.IntegerField()),
                ('image_url', models.URLField()),
                ('category', models.CharField(default=b'N/A', max_length=255)),
                ('abv', models.DecimalField(decimal_places=1, max_digits=3)),
                ('style', models.CharField(default=b'N/A', max_length=255)),
                ('attributes', models.CharField(default=b'N/A', max_length=255)),
                ('type', models.CharField(default=b'N/A', max_length=255)),
                ('brewer', models.CharField(default=b'N/A', max_length=255)),
                ('country', models.CharField(default=b'N/A', max_length=255)),
                ('on_sale', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('store_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('latitude', models.DecimalField(decimal_places=7, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=7, max_digits=9)),
                ('monday_open', models.CharField(max_length=50)),
                ('monday_close', models.CharField(max_length=50)),
                ('tuesday_open', models.CharField(max_length=50)),
                ('tuesday_close', models.CharField(max_length=50)),
                ('wednesday_open', models.CharField(max_length=50)),
                ('wednesday_close', models.CharField(max_length=50)),
                ('thursday_open', models.CharField(max_length=50)),
                ('thursday_close', models.CharField(max_length=50)),
                ('friday_open', models.CharField(max_length=50)),
                ('friday_close', models.CharField(max_length=50)),
                ('saturday_open', models.CharField(max_length=50)),
                ('saturday_close', models.CharField(max_length=50)),
                ('sunday_open', models.CharField(max_length=50)),
                ('sunday_close', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='stores',
            field=models.ManyToManyField(blank=True, to='products.Store'),
        ),
        migrations.AddField(
            model_name='price',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product'),
        ),
    ]
