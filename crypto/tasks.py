from celery import shared_task
from. models import User
from. models import Table
from .utils import get_random_code

from celery.decorators import periodic_task
from celery.task.schedules import crontab
import requests

@shared_task
def get_crypto():
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false'

    info = requests.get(url).json()

    for item in info:
        p, _ = Crypto.objects.get_or_create(name=item)['name'])
        p.image = item['image']
        p.price = item['current_price']
        p.rank = item['market_cap_rank']
        p.market_cap = item['market_cap']
        p.circulation = item['circulating_supply']
        p.save()

@periodic_task(run_every=(contrab(minute='*/1')))
def get_crypto_current():
    get_crypto.delay()


