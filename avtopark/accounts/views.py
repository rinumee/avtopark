from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from .forms import UserRegistrationForm, UserLoginForm
from cars.models import Car
from bookings.models import Booking
from .models import CustomUser

def login_view(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'admin' or request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('user_dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.user_type == 'admin' or user.is_staff:
                    return redirect('admin_dashboard')
                return redirect('user_dashboard')
        messages.error(request, 'Foydalanuvchi nomi yoki parol xato!')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    if request.user.user_type == 'admin' or request.user.is_staff:
        return redirect('admin_dashboard')
    return redirect('user_dashboard')

@login_required
def user_dashboard(request):
    if request.user.user_type == 'admin' or request.user.is_staff:
        return redirect('admin_dashboard')
    
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    available_cars = Car.objects.filter(status='available')[:6]
    
    context = {
        'bookings': bookings,
        'available_cars': available_cars,
        'user': request.user,
    }
    return render(request, 'accounts/user_dashboard.html', context)

def is_admin(user):
    return user.is_authenticated and (user.user_type == 'admin' or user.is_staff)

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_cars = Car.objects.count()
    available_cars = Car.objects.filter(status='available').count()
    total_bookings = Booking.objects.count()
    active_bookings = Booking.objects.filter(status='active').count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    total_users = CustomUser.objects.filter(user_type='user').count()
    
    recent_bookings = Booking.objects.all().order_by('-created_at')[:10]
    recent_cars = Car.objects.all().order_by('-created_at')[:10]
    
    context = {
        'total_cars': total_cars,
        'available_cars': available_cars,
        'total_bookings': total_bookings,
        'active_bookings': active_bookings,
        'pending_bookings': pending_bookings,
        'total_users': total_users,
        'recent_bookings': recent_bookings,
        'recent_cars': recent_cars,
    }
    return render(request, 'accounts/admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_user_list(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    
    total_users = users.count()
    admin_users = users.filter(user_type='admin').count()
    regular_users = users.filter(user_type='user').count()
    
    context = {
        'users': users,
        'total_users': total_users,
        'admin_users': admin_users,
        'regular_users': regular_users,
    }
    return render(request, 'accounts/admin_user_list.html', context)

@login_required
@user_passes_test(is_admin)
def admin_user_create(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type', 'user')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Bu foydalanuvchi nomi band!')
        elif CustomUser.objects.filter(phone=phone).exists():
            messages.error(request, 'Bu telefon raqam band!')
        else:
            user = CustomUser.objects.create(
                username=username,
                full_name=full_name,
                phone=phone,
                email=email,
                password=make_password(password),
                user_type=user_type,
                is_staff=(user_type == 'admin'),
                is_superuser=(user_type == 'admin')
            )
            messages.success(request, f'{username} muvaffaqiyatli yaratildi!')
            return redirect('admin_user_list')
    
    return render(request, 'accounts/admin_user_create.html')

@login_required
@user_passes_test(is_admin)
def admin_user_edit(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        user.full_name = request.POST.get('full_name', user.full_name)
        user.phone = request.POST.get('phone', user.phone)
        user.email = request.POST.get('email', user.email)
        user.user_type = request.POST.get('user_type', user.user_type)
        user.is_active = request.POST.get('is_active') == 'on'
        user.is_staff = (user.user_type == 'admin')
        user.is_superuser = (user.user_type == 'admin')
        
        new_password = request.POST.get('new_password')
        if new_password:
            user.password = make_password(new_password)
            messages.success(request, f'{user.username} paroli yangilandi!')
        
        user.save()
        messages.success(request, f'{user.username} ma\'lumotlari yangilandi!')
        return redirect('admin_user_list')
    
    context = {'edit_user': user}
    return render(request, 'accounts/admin_user_edit.html', context)

@login_required
@user_passes_test(is_admin)
def admin_user_delete(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    if user == request.user:
        messages.error(request, 'O\'zingizni o\'chira olmaysiz!')
        return redirect('admin_user_list')
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'{username} foydalanuvchisi o\'chirildi!')
        return redirect('admin_user_list')
    
    context = {'delete_user': user}
    return render(request, 'accounts/admin_user_confirm_delete.html', context)

@login_required
@user_passes_test(is_admin)
def admin_settings(request):
    from django.conf import settings
    
    if request.method == 'POST':
        site_name = request.POST.get('site_name')
        if site_name:
            request.session['site_name'] = site_name
            messages.success(request, 'Sozlamalar saqlandi!')
        return redirect('admin_settings')
    
    context = {
        'site_name': request.session.get('site_name', 'AVTOPARK'),
        'debug_mode': settings.DEBUG,
        'timezone': settings.TIME_ZONE,
        'total_cars': Car.objects.count(),
        'total_users': CustomUser.objects.count(),
        'total_bookings': Booking.objects.count(),
    }
    return render(request, 'accounts/admin_settings.html', context)

@login_required
@user_passes_test(is_admin)
def admin_profile_edit(request):
    """Admin o'z profilini tahrirlash"""
    admin_user = request.user
    
    if request.method == 'POST':
        admin_user.full_name = request.POST.get('full_name', admin_user.full_name)
        admin_user.phone = request.POST.get('phone', admin_user.phone)
        admin_user.email = request.POST.get('email', admin_user.email)
        
        new_password = request.POST.get('new_password')
        if new_password:
            admin_user.password = make_password(new_password)
            messages.success(request, 'Parol yangilandi!')
        
        admin_user.save()
        messages.success(request, 'Profil ma\'lumotlari yangilandi!')
        return redirect('admin_profile_edit')
    
    context = {'admin_user': admin_user}
    return render(request, 'accounts/admin_profile_edit.html', context)

@login_required
@user_passes_test(is_admin)
def admin_change_password(request):
    """Admin parolini o'zgartirish"""
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        user = request.user
        if not user.check_password(old_password):
            messages.error(request, 'Eski parol noto\'g\'ri!')
        elif new_password != confirm_password:
            messages.error(request, 'Yangi parollar mos kelmadi!')
        elif len(new_password) < 6:
            messages.error(request, 'Parol kamida 6 belgidan iborat bo\'lishi kerak!')
        else:
            user.password = make_password(new_password)
            user.save()
            messages.success(request, 'Parol muvaffaqiyatli o\'zgartirildi!')
            return redirect('admin_settings')
    
    return render(request, 'accounts/admin_change_password.html')