from django.db import models

class Car(models.Model):
    TRANSMISSION_CHOICES = (
        ('manual', 'Mexanik'),
        ('automatic', 'Avtomat'),
    )
    
    FUEL_CHOICES = (
        ('petrol', 'Benzin'),
        ('diesel', 'Dizel'),
        ('gas', 'Gaz'),
        ('electric', 'Elektrik'),
    )
    
    STATUS_CHOICES = (
        ('available', 'Mavjud'),
        ('rented', 'Ijarada'),
        ('maintenance', 'Texnik xizmatda'),
        ('unavailable', 'Mavjud emas'),
    )
    
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    color = models.CharField(max_length=50)
    license_plate = models.CharField(max_length=20, unique=True)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mileage = models.IntegerField(default=0)
    seats = models.IntegerField(default=5)
    doors = models.IntegerField(default=4)
    air_conditioner = models.BooleanField(default=True)
    image = models.ImageField(upload_to='cars/', null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.brand} {self.model} ({self.license_plate})"
    
    @property
    def full_name(self):
        return f"{self.brand} {self.model}"