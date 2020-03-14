# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from products.models import Product, Price

class Command(BaseCommand):
    def handle(self, *args, **options):
       if Price.objects.count() > 10000:
           Price.objects.filter(pk__in=Price.objects.order_by("created_date").values_list('pk')[:4000]).delete()