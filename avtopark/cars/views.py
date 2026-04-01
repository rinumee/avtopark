from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Car
from .forms import CarForm

def is_admin(user):
    return user.is_authenticated and (user.user_type == 'admin' or user.is_staff)

def car_list(request):
    cars = Car.objects.all().order_by('-created_at')
    paginator = Paginator(cars, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'cars': page_obj,
        'total_cars': cars.count(),
        'available_cars': Car.objects.filter(status='available').count(),
    }
    return render(request, 'cars/car_list.html', context)

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'cars/car_detail.html', {'car': car})

@login_required
@user_passes_test(is_admin)
def car_create(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save()
            messages.success(request, f'{car.full_name} muvaffaqiyatli qo\'shildi!')
            return redirect('car_list')
        else:
            messages.error(request, 'Formani to\'g\'ri to\'ldiring!')
    else:
        form = CarForm()
    
    return render(request, 'cars/car_form.html', {
        'form': form,
        'title': 'Yangi avtomobil qo\'shish',
        'button_text': 'Qo\'shish'
    })

@login_required
@user_passes_test(is_admin)
def car_edit(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, f'{car.full_name} muvaffaqiyatli yangilandi!')
            return redirect('car_list')
    else:
        form = CarForm(instance=car)
    
    return render(request, 'cars/car_form.html', {
        'form': form,
        'title': 'Avtomobilni tahrirlash',
        'button_text': 'Saqlash',
        'car': car
    })

@login_required
@user_passes_test(is_admin)
def car_delete(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    if request.method == 'POST':
        car_name = car.full_name
        car.delete()
        messages.success(request, f'{car_name} muvaffaqiyatli o\'chirildi!')
        return redirect('car_list')
    
    return render(request, 'cars/car_confirm_delete.html', {'car': car})