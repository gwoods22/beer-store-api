beer-store-api
==============

## About ##
The Beer Store API is a free to use REST service that provides 
The Beer Store store, product, and availability information. The service 
periodically crawls The Beer Store website to collect data and serves padded JSON. 
This service has no official association with The Beer Store.

The Beer Store API is a side project, so I'll try to implement features when 
I get the chance. As of now, the data is pretty basic (ie. no meta data, no pagination), 
but should be enough to make some cool applications. I've tried to make sure the data is 
accurate as possible, but unfortunately I'm limited to the accuracy of The Beer Store website. 
For example, you'll notice that there's a store with coordinates that place it in the Atlantic Ocean 
just west of Africa. That's just what I scraped from the website.

## Getting Started

1. Install requirements using `pip install -r requirements.txt`  
    * if not installing with `library not found for -lssl` error try running:
    
        `env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install psycopg2`
2. Install postgres and setup database

3. Migrate and Run
    * `python3 manage.py makemigrations`
    * `python3 manage.py migrate`
    * `python3 manage.py runserver`

## How it was made ##
- Python
- Django
- Beautiful Soup (for scraping The Beer Store website)

See
[http://ontariobeerapi.ca/](http://ontariobeerapi.ca/)
