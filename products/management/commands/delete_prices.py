# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from products.models import Product, Price

class Command(BaseCommand):
    def handle(self, *args, **options):
       if Price.objects.count() > 5500:
           num_to_delete = Price.objects.count() - 5500
           Price.objects.filter(pk__in=Price.objects.order_by("created_date").values_list('pk')[:num_to_delete]).delete()