from django.urls import path

from . import views

app_name = "index"
urlpatterns = [
    path("", views.home, name="home"),
    path("search/longnews_ajax", views.longnews_ajax, name="longnews_ajax"),
    path("search/flashnews_ajax", views.flashnews_ajax, name="flashnews_ajax"),
    path("search/promotion_infos_ajax", views.promotion_infos_ajax, name="promotion_infos_ajax"),
    path("search/car_infos_ajax", views.car_infos_ajax, name="car_infos_ajax"),
    path("demo/", views.demo, name="demo"),
    path("search/", views.search, name="search"),
    path("data/rank", views.rank, name="rank"),
    path("login/", views.login, name="login"),
    path("sign/", views.sign, name="sign"),
    path("logout/", views.logout, name="logout"),
]
