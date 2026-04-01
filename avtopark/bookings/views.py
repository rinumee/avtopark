from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from cars.models import Car
from .models import Booking
from .forms import BookingForm

def is_admin(user):
    return user.is_authenticated and (user.user_type == 'admin' or user.is_staff)

@login_required
def booking_list(request):
    if is_admin(request.user):
        bookings = Booking.objects.all().order_by('-created_at')
    else:
        bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'bookings/booking_list.html', {'bookings': bookings})

@login_required
def booking_create(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    if request.method == 'POST':
        print("=" * 50)
        print("POST request received")
        print("POST data:", request.POST)
        
        form = BookingForm(request.POST)
        
        if form.is_valid():
            print("Form is valid!")
            
            booking = form.save(commit=False)
            booking.user = request.user
            booking.car = car
            
            # Kunlar sonini hisoblash
            delta = booking.end_date - booking.start_date
            days = delta.days if delta.days > 0 else 1
            booking.total_price = car.price_per_day * days
            
            print(f"Start: {booking.start_date}, End: {booking.end_date}")
            print(f"Days: {days}, Total: {booking.total_price}")
            
            # Bronni tekshirish
            existing_bookings = Booking.objects.filter(
                car=car,
                status__in=['pending', 'confirmed', 'active'],
                start_date__lt=booking.end_date,
                end_date__gt=booking.start_date
            )
            
            if existing_bookings.exists():
                print("Existing bookings found!")
                messages.error(request, 'Bu vaqt oralig\'ida mashina band!')
                return render(request, 'bookings/booking_form.html', {
                    'form': form,
                    'car': car,
                    'title': 'Bron qilish'
                })
            
            try:
                booking.save()
                print(f"Booking saved! ID: {booking.id}")
                messages.success(request, f'{car.full_name} muvaffaqiyatli bron qilindi!')
                return redirect('booking_detail', booking_id=booking.id)
            except Exception as e:
                print(f"Error saving booking: {e}")
                messages.error(request, f'Xatolik: {e}')
                return render(request, 'bookings/booking_form.html', {
                    'form': form,
                    'car': car,
                    'title': 'Bron qilish'
                })
        else:
            print("Form is invalid!")
            print("Form errors:", form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            
            return render(request, 'bookings/booking_form.html', {
                'form': form,
                'car': car,
                'title': 'Bron qilish'
            })
    
    else:
        form = BookingForm()
    
    context = {
        'form': form,
        'car': car,
        'title': 'Bron qilish'
    }
    
    if is_admin(request.user):
        from accounts.models import CustomUser
        context['users'] = CustomUser.objects.filter(user_type='user')
    
    return render(request, 'bookings/booking_form.html', context)

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if not is_admin(request.user) and booking.user != request.user:
        messages.error(request, 'Sizga bu bronni ko\'rishga ruxsat yo\'q!')
        return redirect('booking_list')
    
    return render(request, 'bookings/booking_detail.html', {'booking': booking})

@login_required
def booking_cancel(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if not is_admin(request.user) and booking.user != request.user:
        messages.error(request, 'Ruxsat yo\'q!')
        return redirect('booking_list')
    
    if booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Bron bekor qilindi!')
    else:
        messages.error(request, 'Bu bronni bekor qilish mumkin emas!')
    
    return redirect('booking_detail', booking_id=booking.id)

@login_required
@user_passes_test(is_admin)
def booking_confirm(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.status == 'pending':
        booking.status = 'confirmed'
        booking.save()
        messages.success(request, 'Bron tasdiqlandi!')
    else:
        messages.error(request, 'Bu bronni tasdiqlash mumkin emas!')
    
    return redirect('booking_detail', booking_id=booking.id)

@login_required
@user_passes_test(is_admin)
def booking_activate(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.status == 'confirmed':
        booking.status = 'active'
        booking.save()
        booking.car.status = 'rented'
        booking.car.save()
        messages.success(request, 'Bron faollashtirildi!')
    else:
        messages.error(request, 'Bu bronni faollashtirish mumkin emas!')
    
    return redirect('booking_detail', booking_id=booking.id)

@login_required
@user_passes_test(is_admin)
def booking_complete(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.status == 'active':
        booking.status = 'completed'
        booking.save()
        booking.car.status = 'available'
        booking.car.save()
        messages.success(request, 'Bron tugatildi!')
    else:
        messages.error(request, 'Bu bronni tugatish mumkin emas!')
    
    return redirect('booking_detail', booking_id=booking.id)