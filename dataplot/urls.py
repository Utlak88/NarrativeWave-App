from django.urls import path
from dataplot import views

app_name = "dataplot"
urlpatterns = [
    path("", views.get_from_parquet, name="get_from_parquet"),
    path("consume_rest_api/", views.consume_rest_api, name="consume_rest_api"),
    path("all_possible_parquet_queries/", views.all_possible_parquet_queries, name="all_possible_parquet_queries"),
]
