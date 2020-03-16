from django.conf.urls import url
from products import views

urlpatterns = [

    url(
        regex=r"^on-sale/$",
        view=views.home,
        name="landing_page"
    ),
    
        url(
        regex=r"^$",
        view=views.ProductsListView.as_view(),
        name="deals_page"
    ),

    url(
        regex=r"^all-beers/$",
        view=views.ProductsListView.as_view(),
        name='product-list'
    ),

    # /stores
    url(
        regex=r"^stores/$",
        view=views.stores,
        name="api-stores"
    ),

    # /stores/{store_id}
    url(
        regex=r"^stores/(?P<store_id>[0-9]+)/$",
        view=views.store_by_id,
        name="api-stores-id"
    ),

    # /products
    url(
        regex=r"^products/$",
        view=views.products,
        name="api-products"
    ),

    # /beers
    url(
        regex=r"^beers/$",
        view=views.beers,
        name="api-beers"
    ),

    # /beers/{product_id}
    url(
        regex=r"^beers/(?P<beer_id>[0-9]+)/$",
        view=views.beer_by_id,
        name="beer_store_api"
    ),
    
        # /beers/{product_id}
    url(
        regex=r"^beer_prices/(?P<beer_id>[0-9]+)/$",
        view=views.beer_prices_by_id,
        name="beer_store_api"
    ),

    # /beers/{product_id}
    url(
        regex=r"^beers/(?P<beer_id>[0-9]+)/products/$",
        view=views.beer_products,
        name="beer_store_api"
    ),

    # /products/{product_id}
    url(
        regex=r"^products/(?P<product_id>[0-9]+)/$",
        view=views.product_by_id,
        name="beer_store_api"
    ),
    
    # /product_prices/{product_id}
    url(
        regex=r"^product_prices/(?P<product_id>[0-9]+)/$",
        view=views.product_prices_by_id,
        name="beer_store_api"
    ),

    # /stores/{store_id}/products
    url(
        regex=r"^stores/(?P<store_id>[0-9]+)/products/$",
        view=views.products_at_store,
        name="beer_store_api"
    ),

    # /products/{product_id}/stores
    url(
        regex=r"^products/(?P<product_id>[0-9]+)/stores/$",
        view=views.stores_with_product,
        name="beer_store_api"
    ),
    
    url(r'^search/?$', view=views.search, name='beer_search'),
]
