# Generated by Django 3.0.4 on 2020-03-15 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_current_price'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['price_per_100ml'], name='products_pr_price_p_05c9c6_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['price_per_abv'], name='products_pr_price_p_88517d_idx'),
        ),
    ]
