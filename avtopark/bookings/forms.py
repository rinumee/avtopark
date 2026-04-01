from django import forms
from django.utils import timezone
import datetime
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'notes']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Qo\'shimcha ma\'lumot...'
            }),
        }
    
    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date:
            # Vaqt mintaqasini qo'shish
            if timezone.is_naive(start_date):
                start_date = timezone.make_aware(start_date, timezone.get_current_timezone())
            
            now = timezone.now()
            if start_date < now:
                raise forms.ValidationError('Boshlanish vaqti hozirgi vaqtdan keyin bo\'lishi kerak!')
        return start_date
    
    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')
        
        if end_date and start_date:
            # Vaqt mintaqasini qo'shish
            if timezone.is_naive(end_date):
                end_date = timezone.make_aware(end_date, timezone.get_current_timezone())
            
            if end_date <= start_date:
                raise forms.ValidationError('Tugash vaqti boshlanish vaqtidan keyin bo\'lishi kerak!')
            
            # Maksimal 30 kun
            if end_date - start_date > datetime.timedelta(days=30):
                raise forms.ValidationError('Bron muddati maksimal 30 kun bo\'lishi mumkin!')
        
        return end_date
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data