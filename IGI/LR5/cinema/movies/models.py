from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, timedelta, date
from django.contrib.auth.models import AbstractUser

class Genre(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Hall(models.Model):
    name = models.CharField(max_length=20)
    capacity = models.PositiveIntegerField(
        validators=[MaxValueValidator(300)],
        default=0
    )

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=70)
    country = models.CharField(max_length=20)
    genres = models.ManyToManyField(Genre, related_name='movies')
    budget = models.FloatField(default=0)
    poster = models.ImageField(upload_to='posters/')
    description = models.CharField(max_length=1000)
    rate = models.DecimalField(max_digits=3, decimal_places=1, default=0)  # TODO
    age_category = models.PositiveIntegerField(
        validators=[MinValueValidator(0)], default=0
    )
    duration = models.DurationField(default=timedelta(hours=2, minutes=30))
    language = models.CharField(max_length=20, default='ru')

    def display_genres(self):
        """
        Creates a string for the Genres. This is required to display genres in Admin.
        """
        return ', '.join([ genre.name for genre in self.genres.all()[:3] ])
    display_genres.short_description = 'Genres'

    def __str__(self):
        return f"{self.title} ({self.country})"

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    time = models.DateTimeField()
    price = models.FloatField(
        validators=[MinValueValidator(0)], default=0
    )

    def __str__(self):
        return f"Movie: {str(self.movie)} | Hall: {self.hall} | Time: {self.time.strftime('%Y-%m-%d %H:%M')} | Price: {self.price}"

class User(AbstractUser):
    birth_date = models.DateField(null=True)
    photo = models.ImageField(upload_to='employee_photos/', null=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    @property
    def age(self):
        if self.birth_date:
            today = date.today()
            age = today.year - self.birth_date.year
            if today.month < self.birth_date.month or (today.month == self.birth_date.month and today.day < self.birth_date.day):
                age -= 1
            return age
        else:
            return None

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    position = models.CharField(max_length=100, default='Cashier')

    def __str__(self):
        return self.user.username

class Coupon(models.Model):
    code_phrase = models.CharField(max_length=100, unique=True)
    discount = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(1.00)]
    )
    clients_used = models.ManyToManyField(User, blank=True)

    def use_coupon(self, client):
        if client not in self.clients_used.all():
            self.clients_used.add(client)
            self.save()
            return True
        else:
            return False

class Ticket(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    cashier = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    time = models.DateTimeField()
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        if self.client is not None:
            client_name = self.client.username
        else:
            client_name = ''
        if self.cashier is not None:
            cashier_name = self.cashier.user.username
        else:
            cashier_name = ''
        return f"Ticket ({self.showtime}), Client: {client_name}, Cashier: {cashier_name}, Buy time: {self.time}"

class CompanyInfo(models.Model):
    info = models.CharField(max_length=10000)

    def __str__(self):
        return f"Company Info: {self.info[:50]}..." if len(self.info) > 50 else f"Company Info: {self.info}"

class News(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='news_images/')
    description = models.CharField(max_length=3000)

    def __str__(self):
        return f"News Title: {self.title}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=3, decimal_places=1, default=0)  # TODO
    description = models.CharField(max_length=3000)
    time = models.DateTimeField()

    def __str__(self):
        return f"Review by {self.user.username} - Rating: {self.rate}/10"
