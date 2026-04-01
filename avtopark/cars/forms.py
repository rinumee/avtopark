from django import forms
from .models import Car

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'color', 'license_plate', 'transmission', 
                  'fuel_type', 'price_per_day', 'price_per_hour', 'deposit', 'mileage', 
                  'seats', 'doors', 'air_conditioner', 'image', 'description', 'status']
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mashina brendi'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Model'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Yil'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rangi'}),
            'license_plate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Davlat raqami'}),
            'transmission': forms.Select(attrs={'class': 'form-control'}),
            'fuel_type': forms.Select(attrs={'class': 'form-control'}),
            'price_per_day': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Kunlik narx (so\'m)'}),
            'price_per_hour': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Soatlik narx (so\'m)', 'required': False}),
            'deposit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Depozit (so\'m)'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Kilometraj'}),
            'seats': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "O'rinlar soni"}),
            'doors': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Eshiklar soni'}),
            'air_conditioner': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tavsif'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }