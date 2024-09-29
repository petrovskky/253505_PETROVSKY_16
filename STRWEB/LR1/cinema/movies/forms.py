from datetime import date
from django import forms
from .models import CompanyInfo, Coupon, Employee, Faq, Genre, Hall, Movie, News, Partner, Position, Review, Showtime, Ticket, Vacancy
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.validators import RegexValidator

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name', ]

class GenreDeletionForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['genre_to_delete'] = forms.ModelChoiceField(queryset=Genre.objects.all(), empty_label=None)

    def delete_item(self):
        genre = self.cleaned_data['genre_to_delete']
        genre = Genre.objects.get(id=genre.id)
        genre.delete()

class HallForm(forms.ModelForm):
    class Meta:
        model = Hall
        fields = ['name', 'capacity']

class HallDeletionForm(forms.ModelForm):
    class Meta:
        model = Hall
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hall_to_delete'] = forms.ModelChoiceField(queryset=Hall.objects.all(), empty_label=None)

    def delete_item(self):
        hall = self.cleaned_data['hall_to_delete']
        hall = Hall.objects.get(id=hall.id)
        hall.delete()

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'country', 'genres', 'budget', 'poster', 'description', 'rate', 'age_category', 'duration', 'language']

class MovieDeletionForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['movie_to_delete'] = forms.ModelChoiceField(queryset=Movie.objects.all(), empty_label=None)

    def delete_item(self):
        movie = self.cleaned_data['movie_to_delete']
        movie = Movie.objects.get(id=movie.id)
        movie.delete()

class ShowtimeForm(forms.ModelForm):
    class Meta:
        model = Showtime
        fields = ['movie', 'hall', 'time', 'price']
        help_texts = {
            'time': 'Format: YYYY-MM-DD HH:MM',
        }

class ShowtimeDeletionForm(forms.ModelForm):  # TODO чтобы можно было фильтровать
    class Meta:
        model = Showtime
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['showtime_to_delete'] = forms.ModelChoiceField(queryset=Showtime.objects.all(), empty_label=None)

    def delete_item(self):
        showtime = self.cleaned_data['showtime_to_delete']
        showtime = Showtime.objects.get(id=showtime.id)
        showtime.delete()

class CustomUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(
        label='Date of Birth',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        )
    )

    phone_number = forms.CharField(
        label='Phone Number',
        validators=[
            RegexValidator(
                regex=r'^\+375[0-9]{2}[0-9]{3}[0-9]{2}[0-9]{2}$',
                message="Phone number must be in the format +375 (29) XXX-XX-XX"
            )
        ],
        widget=forms.TextInput(
            attrs={
                'placeholder': '+375 (29) 123-45-67'
            }
        )
    )

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            raise forms.ValidationError("You must be at least 18 years old to register.")
        return birth_date

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'birth_date', 'photo', 'phone_number']

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['showtime', 'client', 'cashier', 'time']
        help_texts = {
            'time': 'Format: YYYY-MM-DD HH:MM',
        }


class NewsForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 30, 'cols': 100}))

    class Meta:
        model = News
        fields = ['title', 'image', 'description']

class ReviewForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 30, 'cols': 100}))

    class Meta:
        model = Review
        fields = ['rate', 'description']

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['title',]

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['job', 'salary']

class VacancyForm(forms.ModelForm):
    responsibilities = forms.CharField(widget=forms.Textarea(attrs={'rows': 20, 'cols': 100}))
    expectations = forms.CharField(widget=forms.Textarea(attrs={'rows': 20, 'cols': 100}))
    offers = forms.CharField(widget=forms.Textarea(attrs={'rows': 20, 'cols': 100}))

    class Meta:
        model = Vacancy
        fields = ['job', 'employment', 'salary', 'work_experience', 'responsibilities', 'expectations', 'offers']

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code_phrase', 'discount', 'completion']
        widgets = {
            'completion': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }

class FaqForm(forms.ModelForm):
    question = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}))
    answer = forms.CharField(widget=forms.Textarea(attrs={'rows': 20, 'cols': 100}))

    class Meta:
        model = Faq
        fields = ['question', 'answer']

class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['name', 'logo', 'href']

class CompanyInfoForm(forms.ModelForm):
    information = forms.CharField(widget=forms.Textarea(attrs={'rows': 20, 'cols': 100}))
    history = forms.CharField(widget=forms.Textarea(attrs={'rows': 20, 'cols': 100}))
    details = forms.CharField(widget=forms.Textarea(attrs={'rows': 20, 'cols': 100}))
    certificate_ru_head = forms.CharField(widget=forms.Textarea(attrs={'rows': 20, 'cols': 100}))
    certificate_ru_tail = forms.CharField(widget=forms.Textarea(attrs={'rows': 20, 'cols': 100}))
    certificate_en_head = forms.CharField(widget=forms.Textarea(attrs={'rows': 20, 'cols': 100}))
    certificate_en_tail = forms.CharField(widget=forms.Textarea(attrs={'rows': 20, 'cols': 100}))

    class Meta:
        model = CompanyInfo
        fields = ['name',  'logo', 'information', 'history', 'video', 'certificate_ru_head', 'certificate_ru_tail', 'certificate_en_head', 'certificate_en_tail', 'details']