from django.shortcuts import render, redirect, get_object_or_404
from .models import Restaurant, Menu
from decimal import Decimal


def home(request):
    restaurants = Restaurant.objects.all()
    menus = Menu.objects.all()

    if request.method == "POST":
        # Add Restaurant
        if 'add_restaurant' in request.POST:
            restaurant = Restaurant(name=request.POST['name'], location=request.POST['location'])
            restaurant.save()

        # Edit Restaurant
        elif 'edit_restaurant' in request.POST:
            restaurant = get_object_or_404(Restaurant, id=request.POST['restaurant_id'])
            restaurant.name = request.POST['name']
            restaurant.location = request.POST['location']
            restaurant.save()

        # Delete Restaurant
        elif 'delete_restaurant' in request.POST:
            restaurant = get_object_or_404(Restaurant, id=request.POST['restaurant_id'])
            restaurant.delete()

        # Add Menu
        elif 'add_menu' in request.POST:
            restaurant = Restaurant.objects.get(id=request.POST['restaurant_id'])
            price = Decimal(request.POST['price'])  # Ensure price is a Decimal
            menu = Menu(restaurant=restaurant, cuisine_type=request.POST['cuisine_type'],
                        dish_name=request.POST['dish_name'], price=price)
            menu.save()

        # Edit Menu
        elif 'edit_menu' in request.POST:
            menu = get_object_or_404(Menu, id=request.POST['menu_id'])
            menu.cuisine_type = request.POST['cuisine_type']
            menu.dish_name = request.POST['dish_name']
            menu.price = Decimal(request.POST['price'])  # Ensure price is a Decimal
            menu.save()

        # Delete Menu
        elif 'delete_menu' in request.POST:
            menu = get_object_or_404(Menu, id=request.POST['menu_id'])
            menu.delete()

        return redirect('home')

    return render(request, 'menu_analyzer/home.html', {'restaurants': restaurants, 'menus': menus})


def compare_menus(request):
    location = request.GET.get('location', '')
    cuisine_type = request.GET.get('cuisine_type', '')
    price = request.GET.get('price', '')

    filters = {}

    if location:
        filters['restaurant__location'] = location
    if cuisine_type:
        filters['cuisine_type'] = cuisine_type
    if price:
        filters['price__lte'] = price  # This will filter prices less than or equal to the given price

    # Get the menus based on the filters applied
    menus = Menu.objects.filter(**filters)

    return render(request, 'menu_analyzer/compare_menus.html', {'menus': menus})