from django.urls import path
from .views import  index, FetchFuelPricesView
from .views import proxy_polling_endpoint
from .views import get_cities
from .views import submit_fuel_request
from .views import poll_fuel_data


urlpatterns = [
    path("", index, name="home"),
    path("fetch-prices/", FetchFuelPricesView.as_view(), name="fetch_prices"),
    path("proxy-poll/", proxy_polling_endpoint, name="proxy_poll"),
    path("get-cities/", get_cities, name="get_cities"),
    path("submit-fuel-request/", submit_fuel_request, name="submit_fuel_request"),
    path("poll-fuel-data/", poll_fuel_data, name="poll_fuel_data"),
]
