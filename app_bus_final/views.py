import requests
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.core import serializers
from django.views.generic import TemplateView, View, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib import messages
from .models import *


def home(request):
    return render(request, "app_bus_final/home.html")


def Routesearch(request):
    u = []
    v = []
    if request.method == 'GET':
        fromloc = request.GET.get('from').lower()
        toloc = request.GET.get('to').lower()

        check = Route.objects.filter(
            route_List__contains=[fromloc, toloc])
        for i in check:
            u += Route.objects.filter(route_name=i)
        for j in u:
            if j.route_List.index(fromloc) < j.route_List.index(toloc):
                v += Route.objects.filter(route_name=j)
        first = DriverLocation.objects.filter(route_number__in=v).first()
        driver_loc = DriverLocation.objects.all()
        context = {
            "p": check,
            "v": v,
            "d": driver_loc,
            "f": first,
        }

    return render(request, "app_bus_final/maps.html", context)


def create(request):
    r = request.GET.get('routeNumber', None)
    d = request.GET.get('driverNumber', None)
    lat = request.GET.get('latitude', None)
    lon = request.GET.get('longitude', None)
    created_by = request.user

    obj = DriverLocation.objects.create(
        route_number=r,
        driver_number=d,
        latitude=lat,
        longitude=lon,
        created_by=created_by
    )

    return JsonResponse({'status': 'success', 'message': 'Created'})


def delete(request):
    id1 = request.POST.get('driverNumber', None)
    DriverLocation.objects.get(driver_number=id1).delete()
    return JsonResponse({'status': 'success', 'message': 'Ended successfully'})


def update(request):

    if request.method == 'POST':
        driver_number = request.POST.get('driverNumber')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        try:
            driver_location = DriverLocation.objects.get(
                driver_number=driver_number)
            # Update the existing DriverLocation object with new latitude and longitude
            driver_location.latitude = latitude
            driver_location.longitude = longitude
            driver_location.save()

        except ObjectDoesNotExist:
            # DriverLocation doesn't exist, create a new one
            DriverLocation.objects.create(
                driver_number=driver_number, latitude=latitude, longitude=longitude)

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def Routedriver(request):

    context = {
        'username': request.user.username,
        "did": DriverLocation.objects.all(),

    }
    return render(request, "app_bus_final/routedriver.html", context)


def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(
            request, "logged out successfully")
        return redirect('login')


# def login_page(request):
#     if request.method == 'POST':
#         name = request.POST.get('username')
#         pswd = request.POST.get('password')
#         remember_me = request.POST.get('remember_me')

#         user = authenticate(request, username=name, password=pswd)
#         if user is not None:
#             login(request, user)
#             if remember_me:
#                 # Set a longer session duration for "Remember Me"
#                 request.session.set_expiry(1209600)  # 2 weeks in seconds
#             else:
#                 # Use the default session duration
#                 # Use the session framework's default
#                 request.session.set_expiry(0)

#             messages.success(
#                 request, "logged in successfully ")
#             return redirect('routedriver')
#         else:
#             messages.error(
#                 request, "Invalid username or password")
#             return redirect('/login')
#     return render(request, "app_bus_final/login.html")
def login_page(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        pswd = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        user = authenticate(request, username=name, password=pswd)
        if user is not None:
            login(request, user)

            if remember_me:
                # Set a longer session duration for "Remember Me"
                request.session.set_expiry(1209600)  # 2 weeks in seconds
            else:
                # Use the default session duration
                request.session.set_expiry(0)

            messages.success(request, "Logged in successfully.")
            return redirect('routedriver')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('/login')

    return render(request, "app_bus_final/login.html")


@login_required(login_url='login')
def driver_page(request):
    return redirect('routedriver')
