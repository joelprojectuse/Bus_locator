from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('Routesearch', views.Routesearch, name="Routesearch"),
    path('routedriver', views.Routedriver, name="routedriver"),
    path('driver_page', views.driver_page, name="driver_page"),
    path('create', views.create, name="create"),
    path('delete', views.delete, name="delete"),
    path('update', views.update, name="update"),
    path('login', views.login_page, name="login"),
    path('logout', views.logout_page, name="logout"),
]
