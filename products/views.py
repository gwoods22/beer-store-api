import json

from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from .models import Store, Product, Price
from django.shortcuts import render
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from collections import defaultdict
from django.db.models import Q
import bisect 
from operator import itemgetter
from django.views.decorators.cache import cache_page

def _response(request, result, encoder=DjangoJSONEncoder):
    if request.GET.get('format', None) == 'html':
        output = '<table>'
        if isinstance(result, dict):
            for key, value in result.items():
                output += '<tr><th>%s</th><td>%s</td></tr>' % (key, value)
        elif isinstance(result, list):
            first_row = True
            for line in result:
                if first_row:
                    first_row = False
                    output += '<tr>'
                    for key, value in line.items():
                        output += '<th>%s</th>' % key
                    output += '</tr>'
                output += '<tr>'
                for key, value in line.items():
                    output += '<td>%s</td>' % value
                output += '</tr>'
        output += '</table>'
        return HttpResponse(output)

    return JsonResponse(result, safe=False, encoder=encoder)

def home(request):
    """
    Returns home page
    """
    on_sale = Product.objects.filter(on_sale=True).distinct('beer_id')
    
    return render(request, 'index.html', context={'on_sale': list(on_sale.values())})
    
@cache_page(60 * 60)
def deals(request):
    """
    Returns home page
    """
    qs = Product.objects
    
    grouped_products = {}
    grouped_products['Singles'] = qs.filter(size__startswith='1 X').exclude(size__icontains='keg')
    grouped_products['Small Packs'] = qs.filter(Q(size__startswith='2 X')\
                            | Q(size__startswith='3 X')\
                            | Q(size__startswith='4 X')\
                            | Q(size__startswith='5 X')\
                            | Q(size__startswith='6 X')\
                            | Q(size__startswith='7 X')\
                            | Q(size__startswith='8 X')\
                            | Q(size__startswith='9 X'))
    grouped_products['Medium Packs'] = qs.filter(Q(size__startswith='10 X')\
                            | Q(size__startswith='11 X')\
                            | Q(size__startswith='12 X')\
                            | Q(size__startswith='13 X')\
                            | Q(size__startswith='14 X')\
                            | Q(size__startswith='15 X')\
                            | Q(size__startswith='16 X')\
                            | Q(size__startswith='17 X')\
                            | Q(size__startswith='18 X')\
                            | Q(size__startswith='19 X')\
                            | Q(size__startswith='20 X'))
    grouped_products['Large Packs'] = qs.filter(Q(size__startswith='21 X')\
                            | Q(size__startswith='22 X')\
                            | Q(size__startswith='23 X')\
                            | Q(size__startswith='24 X')\
                            | Q(size__startswith='25 X')\
                            | Q(size__startswith='26 X')\
                            | Q(size__startswith='27 X')\
                            | Q(size__startswith='28 X')\
                            | Q(size__startswith='29 X')\
                            | Q(size__startswith='30 X')\
                            | Q(size__startswith='36 X')\
                            | Q(size__startswith='48 X'))
    grouped_products['Kegs'] = qs.filter(size__icontains='keg')

    deals = {}
    for size_category, size_filtered_products in grouped_products.items():
        for type_category in list(Product.objects.order_by().values_list('category',flat=True).distinct()):
            if type_category != 'Non-Alcoholic Beer':    
                products = size_filtered_products.filter(category=type_category)
                product_dicts = []
                for product in products:
                    product_dict = model_to_dict(product)

                    price_obj = Price.objects.filter(product=product).order_by('-created_date').first()
                    if price_obj:
                        current_price = price_obj.price
                        size = product.size.replace('NEW', '').split()
                        units = int(size[0])
                        mls = int(size[-2])

                        product_dict['price_per_100ml'] = round((float(current_price) / (units*mls/100.0)),2)
                        product_dict['current_price'] = current_price

                        product_dicts.append(product_dict)
                sorted_deals = sorted(product_dicts, key=itemgetter('price_per_100ml')) 
                deals[size_category] = deals.get(size_category) or {}
                deals[size_category][type_category] = sorted_deals[:10]
    
    return render(request, 'deals.html', context={'deals': deals, 'ordered_size_categories': ['Singles', 'Small Packs', 'Medium Packs', 'Large Packs', 'Kegs']})

def get_price_per_100ml(product):
    current_price = Price.objects.filter(product=product).order_by('-created_date').first().price
    size = product.size.replace('NEW', '').split()
    units = int(size[0])
    mls = int(size[-2])
    
    return float(current_price) / (units*mls/100.0)

def stores(request):
    """
    Returns data on all Beer Store locations
    city -- The stores' city
    """
    stores = Store.objects.all()

    # get options
    city = request.GET.get('city', None)

    # filter if options are set
    if city is not None:
        stores = stores.filter(city=city)
    
    # return data
    return _response(request, list(stores.values()))


def store_by_id(request, store_id):
    """
    Returns data on a Beer Store location with a specified store id
    """
    # get store by id
    store = Store.objects.get(store_id = int(store_id))

    # return data
    return _response(request, model_to_dict(store))


def stores_with_product(request, product_id):
    """
    Returns all stores with a specified product
    city -- The stores' city
    """
    stores = Store.objects.filter(product__product_id=int(product_id))
    
    # get options
    city = request.GET.get('city', None)

    # filter if options are set
    if city is not None:
        stores = stores.filter(city=city)

    # return data
    return _response(request, list(stores.values()))


def products(request):
    """
    Returns data on all Beer Store products
    category -- The products's category 
    type -- The product's type
    brewer -- The products's brewer
    country -- The product's country of origin
    on_sale -- If the product is on sale (true|false)
    """
    products = Product.objects.all()

    # get options
    category = request.GET.get('category', None)
    type = request.GET.get('type', None)
    brewer = request.GET.get('brewer', None)
    country = request.GET.get('country', None)
    on_sale = request.GET.get('on_sale', None)

    # filter if options are set
    if category is not None:
        products = products.filter(category=category)
 
    if type is not None:
        products = products.filter(type=type)

    if brewer is not None:
        products = products.filter(brewer=brewer)

    if country is not None:
        products = products.filter(country=country)

    if on_sale == "true":
        products = products.filter(on_sale=True)
 
    # return data
    return _response(request, list(products.values()))


def product_by_id(request, product_id):
    """
    Returns data on a Beer Store product with a specified product id
    """
    # get product by id
    product = Product.objects.get(product_id = int(product_id))

    # class ProductEncoder(DjangoJSONEncoder):
    #     def default(self, o):
    #         if isinstance(o, Store):
    #             return super().encode(model_to_dict(o))
    #         return super().default(o)

    qs = Price.objects.filter(product=product).order_by('-created_date')[:30]

    model_dict = model_to_dict(product)
    model_dict['prices'] = [{'x': float(o.created_date.strftime('%s'))* 1000, 'y': float(o.price)} for o in qs]
    model_dict['current_price'] = qs.first().price
    
    # return data   
    return _response(request, model_dict)
    
def product_prices_by_id(request, product_id):
    # get product by id
    product = Product.objects.get(product_id = int(product_id))

    qs = Price.objects.filter(product=product).order_by('-created_date')[:30]
    
    model_dict = model_to_dict(product)
    model_dict['prices'] = json.dumps([{'x': float(o.created_date.strftime('%s'))* 1000, 'y': float(o.price)} for o in qs])
    model_dict['current_price'] = qs.first().price
    
    size = model_dict['size'].replace('NEW', '').split()
    units = int(size[0])
    mls = int(size[-2])
    model_dict['price_per_100ml'] = round((float(model_dict['current_price']) / (units*mls/100)),2)
    
    model_dict['price_per_abv'] = round((float(model_dict['current_price']) / (float(model_dict['abv'])*units*mls/100)),2)
    
    # return data   
    return render(request, 'product_prices.html', context={'params': model_dict})

def products_at_store(request, store_id):
    """
    Returns all products at a specified store
    category -- The products's category 
    type -- The product's type
    brewer -- The products's brewer
    country -- The product's country of origin
    on_sale -- If the product is on sale (true|false)
    size -- Size keyword
    """
    products = Product.objects.filter(stores__store_id=int(store_id))
    
    # get options
    category = request.GET.get('category', None)
    type = request.GET.get('type', None)
    brewer = request.GET.get('brewer', None)
    country = request.GET.get('country', None)
    on_sale = request.GET.get('on_sale', None)
    size = request.GET.get('size', None)

    # filter if options are set
    if category is not None:
        products = products.filter(category=category)
 
    if type is not None:
        products = products.filter(type=type)

    if brewer is not None:
        products = products.filter(brewer=brewer)

    if country is not None:
        products = products.filter(country=country)

    if size is not None:
        products = products.filter(size__icontains=size)

    if on_sale == "true":
        products = products.filter(on_sale=True)

    #return data
    return _response(request, list(products.values()))


def beer_products(request, beer_id):
    """
    Returns all products of a beer with a specified beer id
    """
    # get the beer's products
    products = Product.objects.filter(beer_id = int(beer_id))

    on_sale = request.GET.get('on_sale', None)
    
    if on_sale == "true":
        products = products.filter(on_sale=True)

    # return data
    return _response(request, list(products.values()))
    
def beer_prices_by_id(request, beer_id):
    """
    Returns all products of a beer with a specified beer id
    """
    # get the beer's products
    products = Product.objects.filter(beer_id = int(beer_id))
    params = {}
    params['products'] = {}
    model_dict = {}
    ids = []
    for product in products:
        qs = Price.objects.filter(product=product).order_by('-created_date')[:30]
        model_dict = model_to_dict(product)
        model_dict['prices'] = json.dumps([{'x': float(o.created_date.strftime('%s'))* 1000, 'y': float(o.price)} for o in qs])
        model_dict['current_price'] = qs.first().price
        
        ids.append(model_dict['product_id'])
        
        size = model_dict['size'].replace('NEW', '').split()
        container = size[2]
        model_dict['units'] = int(size[0])
        
        mls = int(size[-2])
        model_dict['price_per_100ml'] = round((float(model_dict['current_price']) / (model_dict['units']*mls/100)),2)
        
        params['products'][container] = params['products'].get(container) or []
        params['products'][container].append(model_dict)
    
    for container, product_list in params['products'].items():
        params['products'][container] = sorted(product_list, key=itemgetter('units')) 

    params['base'] = model_dict
    
    # return data
    return render(request, 'beer_prices.html', context={'params': params, 'ids': json.dumps(ids)})

def beers(request):
    """
    Returns all beers
    category -- The beer's category 
    type -- The beer's type
    brewer -- The beer's brewer
    country -- The beer's country of origin
    on_sale -- If at least one of the beer's products is on sale (true|false)
    """
    beers = Product.objects.distinct('beer_id')
    
    # get options
    category = request.GET.get('category', None)
    type = request.GET.get('type', None)
    brewer = request.GET.get('brewer', None)
    country = request.GET.get('country', None)
    on_sale = request.GET.get('on_sale', None)

    # filter if options are set
    if category is not None:
        beers = beers.filter(category=category)
 
    if type is not None:
        beers = beers.filter(type=type)

    if brewer is not None:
        beers = beers.filter(brewer=brewer)

    if country is not None:
        beers = beers.filter(country=country)

    if on_sale == "true":
        beers = beers.filter(on_sale=True)

    # return data
    return _response(request, list(beers.values()))

def search(request):
    beers = Product.objects
    
    if request.method == 'GET': 
        search_query = request.GET.get('search_box', None)
        
        vector = SearchVector('name', 'brewer')
        query = SearchQuery(search_query)
        beers = beers.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.00000000000001).order_by('-rank', 'beer_id').distinct('rank','beer_id')
        
        return render(request, 'search.html', context={'beers': list(beers.values()), 'query': search_query})


def beer_by_id(request, beer_id):
    """
    Returns a beer with a specified beer id
    """
    # get beer
    beer = Product.objects.filter(beer_id = int(beer_id)).first()

    # return data
    return _response(request, model_to_dict(beer))
