import calendar
from collections import Counter, OrderedDict
from django.http import Http404, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from matplotlib import pyplot as plt
import matplotlib
from io import BytesIO

from movies.apis.ip import IpAPI
from movies.apis.nationality import NationalityAPI
from movies.forms import CompanyInfoForm, CouponForm, CustomUserCreationForm, EmployeeForm, GenreDeletionForm, GenreForm, HallDeletionForm, HallForm, MovieDeletionForm, MovieForm, NewsForm, ReviewForm, ShowtimeDeletionForm, ShowtimeForm, TicketForm
from .models import CompanyInfo, Coupon, Employee, Hall, Movie, News, Review, Showtime, Genre, Ticket
from django.contrib.auth.models import Group
from .models import User

from django.contrib.auth import login, authenticate #

from datetime import datetime #

import logging

logging.basicConfig(level=logging.INFO, filename="py_log.log",
                    format="%(asctime)s %(levelname)s %(message)s")

def registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            birth_date = form.cleaned_data.get('birth_date')
            user = authenticate(username=username, password=password, birth_date=birth_date)
            login(request, user)
            logging.info(f'Register success: Username: {user.username}')
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def index(request):
    return render(request, 'main.html')

def afisha(request):
    selected_date = request.GET.get('date', None)
    selected_genre = request.GET.get('genre', None)
    search_movie_title = request.GET.get('movie_title', '')
    genres = Genre.objects.all()
    showtimes = Showtime.objects.all()

    if selected_date is not None and selected_date.strip() != '':
        showtimes = showtimes.filter(time__date=selected_date)

    if selected_genre is not None and selected_genre.strip() != '':
        showtimes = showtimes.filter(movie__genres__name__icontains=selected_genre)

    if search_movie_title.strip() != '':
        showtimes = showtimes.filter(movie__title__icontains=search_movie_title)

    movies = showtimes.values_list('movie', flat=True).distinct()
    movie_objects = map(lambda movie_id: Movie.objects.get(id=movie_id), movies)
    movies = list(movie_objects)

    if selected_date:
        request.session['selected_date'] = selected_date

    if selected_genre:
        request.session['selected_genre'] = selected_genre

    if search_movie_title:
        request.session['search_movie_title'] = search_movie_title

    context = {'movies': movies, 'genres': genres, 'selected_date': selected_date, 'selected_genre': selected_genre, 'search_movie_title': search_movie_title}
    return render(request, 'afisha.html', context)

def news(request):
    news_list = News.objects.all()
    logging.info("News successful got")  # Getting news logging
    return render(request, 'news.html', { 'news_list' : news_list })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_info(request):
    company_info = get_object_or_404(CompanyInfo)
    if request.method == 'POST':
        form = CompanyInfoForm(request.POST, instance=company_info)
        if form.is_valid():
            form.save()
            return redirect('/info')
    else:
        form = CompanyInfoForm(instance=company_info)

    return render(request, 'edit_afisha_item.html', { 'form' : form, 'item_name' : form.Meta.model.__name__ })

def info(request):
    info = None
    try:
        info = CompanyInfo.objects.all().first().info
    except CompanyInfo.DoesNotExist:
        info = "No company information available."
    except AttributeError as exc:
        info = "Company information is not available."
        logging.error(f"Error accessing 'info' attribute: {exc}")

    return render(request, 'info.html', { 'info' : info })

def contacts(request):
    staff = Employee.objects.all().filter(user__is_superuser=False)
    return render(request, 'contacts.html', { 'staff' : staff })

@login_required
def profile(request):
    import tzlocal
    def get_user_time():
        user_timezone = tzlocal.get_localzone()
        current_date = datetime.now(user_timezone).date()
        current_date_formatted = current_date.strftime("%d/%m/%Y")
        calendar_text = calendar.HTMLCalendar().formatmonth(datetime.now(user_timezone).year, datetime.now(user_timezone).month)

        return {
            "user_timezone": user_timezone,
            "current_date_formatted": current_date_formatted,
            "calendar_text": calendar_text,
        }

    user_tz_context = get_user_time()

    ip = IpAPI.get_ip()['ip']

    nationality = NationalityAPI.get_ip(request.user.first_name)['country'][0]['country_id'] if NationalityAPI.get_ip(request.user.first_name)['country'] else None

    if request.user.is_staff:
        tickets = Ticket.objects.all().filter(cashier__user__id=request.user.id)
    else:
        tickets = Ticket.objects.all().filter(client__id=request.user.id)

    return render(request, 'profile.html', { 'tickets' : tickets, 'ip' : ip, 'nationality' : nationality } | user_tz_context)

def movie_detail(request, movie_id):
    selected_movie = get_object_or_404(Movie, id=movie_id)
    showtimes_of_selected_movie = Showtime.objects.all().filter(movie__id=movie_id)

    return render(request, 'movie_detail.html', { 'movie' : selected_movie, 'showtimes' : showtimes_of_selected_movie })

def create_item_template(request, cur_form):
    if request.method == 'POST':
        form = cur_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('afisha')
    else:
        form = cur_form()

    return render(
        request,
        'create_afisha_item.html',
        { 'form': form, 'item_name' : form.Meta.model.__name__ }
    )

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_genre(request):
    return create_item_template(request, GenreForm)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_hall(request):
    return create_item_template(request, HallForm)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('get_movies'))
    else:
        form = MovieForm()

    return render(
        request,
        'create_afisha_item.html',
        { 'form': form, 'item_name' : form.Meta.model.__name__ }
    )

def create_showtime_movie(request, movie_id):
    if request.method == 'POST':
        form = Showtime(request.POST)
        if form.is_valid():
            form.save()
            return redirect('afisha')
    else:
        selected_movie = Movie.objects.get(id=movie_id)
        form = ShowtimeForm(initial={'movie': selected_movie})
        form.fields['movie'].disabled = True

    return render(
        request,
        'create_afisha_item.html',
        { 'form': form, 'item_name' : form.Meta.model.__name__ }
    )

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_showtime(request):
    return create_item_template(request, ShowtimeForm)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def get_users(request):
    users = User.objects.all()
    staff_list = [user for user in users if user.is_staff == True]
    client_list = [user for user in users if user not in staff_list]
    return render(request,'users.html',{'staff': staff_list, 'clients' : client_list})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_employee_by_id(request):
    employee_id = request.GET.get('employee_id')
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('/users')
    else:
        form = EmployeeForm(instance=employee)

    return render(request, 'edit_afisha_item.html', {'form': form, 'item_name' : form.Meta.model.__name__})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def make_employee(request, id):
    if request.method == 'POST':
        try:
            user = User.objects.get(id=id)
            employee = Employee(user=user)
            employee.save()
            user.is_staff = True
            user.save()
        except User.DoesNotExist:
            pass
        return redirect('/users/')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def make_client(request, id):
    if request.method == 'POST':
        #staff_group = Group.objects.get(name='Cinema Staff')
        user = User.objects.get(id=id)
        try:
            employee = Employee.objects.get(user=user)
            employee.delete()
        except Exception as ex:
            print(f'Error in function make_client: {ex.args[0]}')
        user.is_staff = False
        user.save()
        #staff_group.user_set.remove(user)
        return redirect('/users/')

@login_required
def make_ticket(request, id):
    if request.method == 'POST':
        entered_code = request.POST.get('entered_code')
        coupon = None
        if entered_code.strip() != '':
            try:
                coupon = Coupon.objects.get(code_phrase=entered_code)
            except Coupon.DoesNotExist:
                return render(request, 'use_coupon.html', { 'error': 'There is no such coupon. Enter an existing coupon or leave the field blank' })

            if not coupon.use_coupon(request.user):
                return render(request, 'use_coupon.html', { 'error': 'This coupon has already been used' })

        user = request.user
        showtime = Showtime.objects.get(id=id)
        time = datetime.now()
        if request.user.is_staff:
            try:
                employee = Employee.objects.get(user=request.user)
                new_ticket = Ticket(cashier=employee, showtime=showtime, time=time)
            except Exception as ex:
                print(f'Error in function make_ticket: {ex.args[1]}')
        else:
            new_ticket = Ticket(client=user, showtime=showtime, time=time)

        if coupon:
            new_ticket.coupon = coupon

        new_ticket.save()
        return redirect('/afisha')

    return render(request, 'use_coupon.html')

def get_movies_stat_context():
    movies = Movie.objects.all()
    movie_stats = {}

    tickets = Ticket.objects.all()

    for movie in movies:
        cur_tickets = tickets.filter(showtime__movie__id=movie.id)
        revenue = 0
        for ticket in cur_tickets:
            revenue += ticket.showtime.price
        movie_stats[movie] = {
            'tickets_sold' : cur_tickets.count(),
            'revenue' : revenue,
        }


    #------------- Graphs -------------#

    #------------- Tickets Sold -------------#
    movie_stats = OrderedDict(sorted(movie_stats.items(), key=lambda x: x[1]['tickets_sold'], reverse=True))

    movie_names = [movie.title for movie in movie_stats.keys()]
    tickets_sold = [stats['tickets_sold'] for stats in movie_stats.values()]

    matplotlib.use('agg')

    plt.figure(figsize=(10, 8))
    plt.bar(range(len(movie_names)), tickets_sold, width=0.8)

    plt.xlabel('Movie name')
    plt.ylabel('Number of tickets sold')
    plt.title('Ticket sales histogram')

    plt.xticks(range(len(movie_names)), movie_names, rotation=45)

    plt.gcf().autofmt_xdate()
    plt.subplots_adjust(bottom=0.3)

    buf = BytesIO()
    plt.savefig(buf, format='svg')
    svg_tickets = buf.getvalue().decode('utf-8')

    #------------- Total Revenue -------------#
    movie_stats = OrderedDict(sorted(movie_stats.items(), key=lambda x: x[1]['revenue'], reverse=True))

    movie_names = [movie.title for movie in movie_stats.keys()]
    revenue_list = [stats['revenue'] for stats in movie_stats.values()]

    plt.figure(figsize=(10, 8))
    plt.bar(range(len(movie_names)), revenue_list, width=0.8)

    plt.xlabel('Movie name')
    plt.ylabel('Total revenue')
    plt.title('Revenue histogram')

    plt.xticks(range(len(movie_names)), movie_names, rotation=45)

    plt.gcf().autofmt_xdate()
    plt.subplots_adjust(bottom=0.3)

    buf = BytesIO()
    plt.savefig(buf, format='svg')
    svg_revenue = buf.getvalue().decode('utf-8')

    #---------------------------------#

    context = {
        'stat_type': 'movies',
        'movie_stats' : movie_stats,
        'histogram_tickets' : svg_tickets,
        'histogram_revenue' : svg_revenue,
    }

    return context

def get_clients_stat_context():
    clients = User.objects.all().filter(is_staff=False)
    client_stats = {}

    tickets = Ticket.objects.all()

    for client in clients:
        cur_tickets = tickets.filter(client__id=client.id)
        genres_stat = Counter()
        for ticket in cur_tickets:
            genres = ticket.showtime.movie.genres.all()
            for genre in genres:
                genres_stat[genre] += 1
        favourite_genre = max(genres_stat, key=genres_stat.get, default=None)

        client_stats[client] = {
            'tickets_purchased' : cur_tickets.count(),
            'favourite_genre' : favourite_genre,
        }

    #------------- Graphs -------------#

    #------------- Age -------------#
    age_list = [client.age for client in client_stats.keys() if client.age is not None]

    intervals = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    counts = Counter(
        [
            i for age in age_list for i in intervals[:-1] if age >= i and age < i + 10
        ]
    )

    matplotlib.use('agg')

    plt.figure(figsize=(10, 8))
    plt.bar(counts.keys(), counts.values())

    plt.xlabel('Age intervals')
    plt.ylabel('Count')
    plt.title('Age histogram')

    plt.xticks(intervals[:-1], [f"{i}-{i+10}" for i in intervals[:-1]])

    plt.gcf().autofmt_xdate()
    plt.subplots_adjust(bottom=0.3)

    buf = BytesIO()
    plt.savefig(buf, format='svg')
    svg_age = buf.getvalue().decode('utf-8')

    #---------------------------------#

    context = {
        'stat_type': 'clients',
        'client_stats' : client_stats,
        'histogram_age' : svg_age
    }
    return context

@login_required
@user_passes_test(lambda u: u.is_superuser)
def get_statisctics(request):
    if request.method == 'POST':
        stat_type = request.POST.get('stat_type')

        if stat_type == 'clients':
            context = get_clients_stat_context()
        elif stat_type == 'movies':
            context = get_movies_stat_context()
        else:
            context = {}

        return render(request, 'statistics.html', context)

    return render(request, 'statistics.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def get_movies(request):
    movies = Movie.objects.all()

    search_movie_title = request.GET.get('movie_title', '')
    search_movie_country = request.GET.get('movie_country', '')
    selected_genre = request.GET.get('genre', None)
    genres = Genre.objects.all()

    if search_movie_title.strip() != '':
        movies = movies.filter(title__icontains=search_movie_title)

    if search_movie_country.strip() != '':
        movies = movies.filter(country__icontains=search_movie_country)

    if selected_genre is not None and selected_genre.strip() != '':
        movies = movies.filter(genres__name__icontains=selected_genre)

    if search_movie_title:
        request.session['search_movie_title'] = search_movie_title

    if search_movie_country:
        request.session['search_movie_country'] = search_movie_country

    if selected_genre:
        request.session['selected_genre'] = selected_genre

    return render(request, 'movies.html', { 'movies' : movies, 'genres' : genres, 'search_movie_title' : search_movie_title, 'search_movie_country' : search_movie_country, 'selected_genre' : selected_genre })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_movie_by_id(request):
    if request.method == 'POST':
        try:
            movie_id = request.POST.get('movie_id')
            movie = Movie.objects.get(id=movie_id)
            movie.delete()
        except Movie.DoesNotExist:
            pass
        return redirect('/afisha/movies')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_movie_by_id(request):
    movie_id = request.GET.get('movie_id')
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('/afisha/movies')
    else:
        form = MovieForm(instance=movie)

    return render(request, 'edit_afisha_item.html', {'form': form, 'item_name' : form.Meta.model.__name__})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def get_genres(request):
    genres = Genre.objects.all()
    if request.method == 'POST':
        pass
    return render(request, 'genres.html', { 'genres' : genres })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_genre_by_id(request):
    if request.method == 'POST':
        genre_id = request.POST.get('genre_id')
        try:
            genre = Genre.objects.get(id=genre_id)
            genre.delete()
        except Genre.DoesNotExist:
            pass
        return redirect('/afisha/genres')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_genre_by_id(request):
    genre_id = request.GET.get('genre_id')
    genre = get_object_or_404(Genre, pk=genre_id)
    if request.method == 'POST':
        form = GenreForm(request.POST, instance=genre)
        if form.is_valid():
            form.save()
            return redirect('/afisha/genres')
    else:
        form = GenreForm(instance=genre)

    return render(request, 'edit_afisha_item.html', {'form': form, 'item_name' : form.Meta.model.__name__})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def get_halls(request):
    halls = Hall.objects.all()
    if request.method == 'POST':
        pass
    return render(request, 'halls.html', { 'halls' : halls })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_hall_by_id(request):
    if request.method == 'POST':
        hall_id = request.POST.get('hall_id')
        try:
            hall = Hall.objects.get(id=hall_id)
            hall.delete()
        except Hall.DoesNotExist:
            pass
        return redirect('/afisha/halls')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_hall_by_id(request):
    hall_id = request.GET.get('hall_id')
    hall = get_object_or_404(Hall, pk=hall_id)
    if request.method == 'POST':
        form = HallForm(request.POST, instance=hall)
        if form.is_valid():
            form.save()
            return redirect('/afisha/halls')
    else:
        form = HallForm(instance=hall)

    return render(request, 'edit_afisha_item.html', {'form': form, 'item_name' : form.Meta.model.__name__})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def get_showtimes(request):
    showtimes = Showtime.objects.all()
    search_movie_title = request.GET.get('movie_title', '')
    selected_date = request.GET.get('date', None)
    sort_by = request.POST.get('sort_by', '')

    if search_movie_title.strip() != '':
        showtimes = showtimes.filter(movie__title__icontains=search_movie_title)
    if selected_date is not None and selected_date.strip() != '':
        showtimes = showtimes.filter(time__date=selected_date)

    if selected_date:
        request.session['selected_date'] = selected_date

    if search_movie_title:
        request.session['search_movie_title'] = search_movie_title

    tickets = Ticket.objects.all().filter(showtime__in=showtimes)

    profits = {}
    for showtime in showtimes:
        cur_tickets = tickets.filter(showtime=showtime)
        cur_profit = sum([ticket.showtime.price for ticket in cur_tickets if ticket.showtime == showtime])
        profits[showtime] = cur_profit

    if sort_by.strip() != '':
        profits = dict(sorted(profits.items(), key=lambda x: x[1], reverse=True))

    return render(request, 'showtimes.html', { 'profits' : profits, 'selected_date': selected_date, 'search_movie_title' : search_movie_title})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_showtime_by_id(request):
    if request.method == 'POST':
        showtime_id = request.POST.get('showtime_id')
        try:
            showtime = Showtime.objects.get(id=showtime_id)
            showtime.delete()
        except Showtime.DoesNotExist:
            pass
        return redirect('/afisha/showtimes')

    return redirect('/afisha/showtimes')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_showtime_by_id(request):
    showtime_id = request.GET.get('showtime_id')
    showtime = get_object_or_404(Showtime, pk=showtime_id)
    if request.method == 'POST':
        form = ShowtimeForm(request.POST, instance=showtime)
        if form.is_valid():
            form.save()
            return redirect('/afisha/showtimes')
    else:
        form = ShowtimeForm(instance=showtime)

    return render(request, 'edit_afisha_item.html', {'form': form, 'item_name' : form.Meta.model.__name__})

@login_required
@user_passes_test(lambda u: u.is_staff)
def get_tickets(request):
    tickets = Ticket.objects.all()

    if request.method == 'POST':
        pass
    else:
        selected_from_date = request.GET.get('from_date', None)
        selected_to_date = request.GET.get('to_date', None)
        search_movie_title = request.GET.get('movie_title', '')
        search_client_username = request.GET.get('client_username', '')
        search_cashier_username = request.GET.get('cashier_username', '')

        if selected_from_date is not None and selected_from_date.strip() != '':
            selected_from_date_datetime = datetime.strptime(selected_from_date, '%Y-%m-%d')
            tickets = tickets.filter(time__date__gte=selected_from_date_datetime)
            request.session['selected_from_date'] = selected_from_date

        if selected_to_date is not None and selected_to_date.strip() != '':
            selected_to_date_datetime = datetime.strptime(selected_to_date, '%Y-%m-%d').date()
            tickets = tickets.filter(time__date__lte=selected_to_date_datetime)
            request.session['selected_to_date'] = selected_to_date

        if search_movie_title:
            tickets = tickets.filter(showtime__movie__title__icontains=search_movie_title)
            request.session['search_movie_title'] = search_movie_title

        if search_client_username:
            tickets = tickets.filter(client__username__icontains=search_client_username)
            request.session['search_client_username'] = search_client_username

        if search_cashier_username:
            tickets = tickets.filter(cashier__user__username__icontains=search_cashier_username)
            request.session['search_cashier_username'] = search_cashier_username

        profit = sum([ticket.showtime.price for ticket in tickets])

        return render(request, 'tickets.html', { 'tickets' : tickets, 'profit' : profit,'selected_from_date' : selected_from_date, 'selected_to_date' : selected_to_date, 'search_movie_title' : search_movie_title, 'search_client_username' : search_client_username, 'search_cashier_username' : search_cashier_username })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_ticket_by_id(request):
    ticket_id = request.GET.get('ticket_id')
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('/tickets')
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'edit_afisha_item.html', {'form': form, 'item_name' : form.Meta.model.__name__})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('news'))
    else:
        form = NewsForm()

    return render(
        request,
        'create_afisha_item.html',
        { 'form': form, 'item_name' : form.Meta.model.__name__ }
    )

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_news_by_id(request):
    news_id = request.GET.get('news_id')
    news = get_object_or_404(News, pk=news_id)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            return redirect(reverse('tickets'))
    else:
        form = NewsForm(instance=news)

    return render(request, 'edit_afisha_item.html', {'form': form, 'item_name' : form.Meta.model.__name__})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_news_by_id(request):
    if request.method == 'POST':
        news_id = request.POST.get('news_id')
        news = News.objects.get(id=news_id)
        news.delete()
        return redirect(reverse('news'))

def reviews(request):
    reviews = Review.objects.all()
    return render(request, 'reviews.html', { 'reviews' : reviews })

@login_required
def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.time = datetime.now()
            review.save()
            return redirect(reverse('reviews'))
    else:
        form = ReviewForm()

    return render(
        request,
        'create_afisha_item.html',
        { 'form': form, 'item_name' : form.Meta.model.__name__ }
    )

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_review_by_id(request):
    if request.method == 'POST':
        review_id = request.POST.get('review_id')
        review = Review.objects.get(id=review_id)
        review.delete()
        return redirect(reverse('reviews'))

def privacy(request):
    return render(request, 'privacy_policy.html')

def coupons(request):
    coupons = Coupon.objects.all()
    return render(request, 'coupons.html', { 'coupons' : coupons })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('coupons'))
    else:
        form = CouponForm()

    return render(
        request,
        'create_afisha_item.html',
        {
            'form' : form,
            'item_name' : form.Meta.model.__name__
        }
    )

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_coupon_by_id(request):
    if request.method == 'POST':
        coupon_id = request.POST.get('coupon_id')
        try:
            coupon = Coupon.objects.get(id=coupon_id)
            coupon.delete()
        except Coupon.DoesNotExist:
            logging.info(f"Error in function 'delete_coupon_by_id':Coupon with id {coupon_id} does not exist.")

        return redirect(reverse('coupons'))




