# Generated by Django 3.0.4 on 2020-03-15 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20200315_1953'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['size'], name='products_pr_size_425055_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['category'], name='products_pr_categor_14b9c0_idx'),
        ),
    ]