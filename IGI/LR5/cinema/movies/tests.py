from unittest.mock import patch
from django.test import RequestFactory, TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.files.uploadedfile import SimpleUploadedFile

from movies.models import CompanyInfo, Coupon, Employee, Genre, Hall, Movie, News, Review, Showtime, Ticket
from movies.views import afisha, contacts, get_movies_stat_context, make_employee, make_ticket, profile
from .forms import CompanyInfoForm, CustomUserCreationForm, EmployeeForm, GenreForm, HallForm, MovieForm, NewsForm
from datetime import date, datetime, timedelta
from django.contrib.staticfiles import finders

from django.utils import timezone
import pytz

User = get_user_model()

def get_test_image():
    image_path = finders.find('tests_image.jpg')

    with open(image_path, 'rb') as f:
        image_content = f.read()

    # Simulate a valid form submission
    valid_image = SimpleUploadedFile("valid_image.jpg", image_content, content_type="image/jpeg")

    return valid_image

class RegistrationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('registration')  # Ensure your URL name matches your URL configuration

    def test_registration_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        self.assertIsInstance(response.context['form'], CustomUserCreationForm)

    def test_registration_view_post_invalid(self):
        response = self.client.post(self.url, {
            'username': '',
            'email': 'invalid',
            'password1': 'password123',
            'password2': 'password123',
            'birth_date': '2007-01-01',
            'phone_number': 'invalid',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        self.assertFalse(response.context['form'].is_valid())
        self.assertIn('username', response.context['form'].errors)
        self.assertIn('email', response.context['form'].errors)
        self.assertIn('birth_date', response.context['form'].errors)
        self.assertIn('phone_number', response.context['form'].errors)

    def test_registration_view_post_valid(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'strong_password123',
            'password2': 'strong_password123',
            'birth_date': '2000-01-01',
            'photo': get_test_image(),
            'phone_number': '+375291234567',
        })

        # Check if the user was created
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(check_password('strong_password123', user.password))
        self.assertEqual(user.birth_date, date(2000, 1, 1))

        # Check if the user is authenticated
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)

        # Check redirection to the home page
        self.assertRedirects(response, '/')

class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main.html')

class AfishaViewTestCase(TestCase):
    def setUp(self):
        # Create test data: genres, movies, and showtimes
        self.genre1 = Genre.objects.create(name='Action')
        self.genre2 = Genre.objects.create(name='Comedy')

        self.movie1 = Movie.objects.create(title='Movie 1', country='USA', poster=get_test_image())
        self.movie1.genres.add(self.genre1)
        self.movie2 = Movie.objects.create(title='Movie 2', country='UK', poster=get_test_image())
        self.movie2.genres.add(self.genre2)

        self.hall1 = Hall.objects.create(name='1')

        self.showtime1 = Showtime.objects.create(movie=self.movie1, time=date.today(), hall=self.hall1)
        self.showtime2 = Showtime.objects.create(movie=self.movie2, time=date.today(), hall=self.hall1)

        self.client = Client()

    def test_afisha_view(self):
        # Test view without any parameters
        response = self.client.get(reverse('afisha'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['movies']), 2)  # All movies should be listed
        self.assertEqual(len(response.context['genres']), 2)  # All genres should be available

        # Test view with date parameter
        response = self.client.get(reverse('afisha') + '?date=' + str(date.today()))
        self.assertEqual(len(response.context['movies']), 2)  # All movies should be listed

        # Test view with genre parameter
        response = self.client.get(reverse('afisha') + '?genre=Action')
        self.assertEqual(len(response.context['movies']), 1)  # Only movies with 'Action' genre should be listed

        # Test view with search_movie_title parameter
        response = self.client.get(reverse('afisha') + '?movie_title=Movie 1')
        self.assertEqual(len(response.context['movies']), 1)  # Only 'Movie 1' should be listed

class NewsViewTestCase(TestCase):
    def setUp(self):
        # Create test news articles
        self.news1 = News.objects.create(title='News 1', description='Description 1', image=get_test_image())
        self.news2 = News.objects.create(title='News 2', description='Description 2', image=get_test_image())

        self.client = Client()

    def test_news_view(self):
        # Test view without any parameters
        response = self.client.get(reverse('news'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['news_list']), 2)  # All news articles should be listed

        # Test view with news articles
        self.assertContains(response, 'News 1')  # News 1 title should be present in response
        self.assertContains(response, 'News 2')  # News 2 title should be present in response

class InfoViewTestCase(TestCase):
    def setUp(self):
        # Create test company information
        self.company_info = 'Test company information.'
        CompanyInfo.objects.create(info=self.company_info)

        self.client = Client()

    def test_info_view_with_info_available(self):
        # Test view when company information is available
        response = self.client.get(reverse('info'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.company_info)  # Company information should be present in response

    def test_info_view_with_no_info_available(self):
        # Delete existing company information
        CompanyInfo.objects.all().delete()

        # Test view when no company information is available
        response = self.client.get(reverse('info'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '')  # Response should not contain any company information

class EditInfoViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(username='testuser', password='testpassword')
        self.company_info = CompanyInfo.objects.create(info='Test Company')

    def test_edit_info_view_with_superuser(self):
        client = Client()
        superuser = User.objects.create_superuser(username='testadmin', password='testadmin')
        client.force_login(superuser)
        response = client.get(reverse('edit_info'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_afisha_item.html')
        self.assertIsInstance(response.context['form'], CompanyInfoForm)
        self.assertEqual(response.context['item_name'], 'CompanyInfo')

        data = {'info': 'Updated Test Company'}
        response = client.post(reverse('edit_info'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CompanyInfo.objects.get(pk=self.company_info.pk).info, 'Updated Test Company')

    def test_edit_info_view_with_non_superuser(self):
        user = User.objects.create_user(username='normaluser', password='normalpassword')
        client = Client()
        client.login(username='normaluser', password='normalpassword')
        response = client.get(reverse('edit_info'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + '?next=/info/edit')

class ContactsViewTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='john', password='john1234')
        self.user2 = User.objects.create(username='jane', password='jane1234')
        self.employee1 = Employee.objects.create(user=self.user1, position='Manager')
        self.employee2 = Employee.objects.create(user=self.user2, position='Developer')

    def test_contacts_view_with_client(self):
        client = Client()
        response = client.get(reverse('contacts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contacts.html')
        self.assertContains(response, self.employee1)
        self.assertContains(response, self.employee2)

class TestProfileView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='testuser', password='testpass')
        self.user2 = User.objects.create_user(username='testemployee', password='testpass')
        self.employee = Employee.objects.create(user=self.user2)

        self.genre1 = Genre.objects.create(name='Action')
        self.movie1 = Movie.objects.create(title='Movie 1', country='USA', poster=get_test_image())
        self.movie1.genres.add(self.genre1)
        self.hall1 = Hall.objects.create(name='1')
        self.showtime1 = Showtime.objects.create(movie=self.movie1, time=timezone.now(), hall=self.hall1)

        self.ticket1 = Ticket.objects.create(cashier=self.employee, time=timezone.now(), showtime=self.showtime1)
        self.ticket2 = Ticket.objects.create(client=self.user1, time=timezone.now(), showtime=self.showtime1)

    def test_profile_view_for_staff(self):
        self.user2.is_staff = True
        self.user2.save()
        self.client.force_login(self.user2)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.ticket2)

    def test_profile_view_for_client(self):
        self.user1.is_staff = False
        self.user1.save()
        self.client.force_login(self.user1)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.ticket1)

class TestMovieDetailView(TestCase):
    def setUp(self):
        self.client = Client()
        self.movie = Movie.objects.create(
            title='Test Movie',
            country='USA',
            poster='test_poster.jpg'
        )
        self.hall = Hall.objects.create(name='Test Hall')
        self.showtime1 = Showtime.objects.create(
            movie=self.movie,
            time='2023-05-23 14:00:00',
            hall=self.hall
        )
        self.showtime2 = Showtime.objects.create(
            movie=self.movie,
            time='2023-05-23 16:00:00',
            hall=self.hall
        )

    def test_movie_detail_view_with_valid_movie_id(self):
        response = self.client.get(reverse('movie_detail', args=[self.movie.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movie_detail.html')
        self.assertEqual(response.context['movie'], self.movie)
        self.assertQuerysetEqual(response.context['showtimes'], [self.showtime1, self.showtime2], ordered=False)

    def test_movie_detail_view_with_invalid_movie_id(self):
        response = self.client.get(reverse('movie_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

class TestCreateGenreView(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            username='testadmin', password='testpassword'
        )
        self.regular_user = User.objects.create_user(
            username='testuser', password='testpassword'
        )

    def test_create_genre_view_with_valid_data_by_superuser(self):
        self.client.login(username='testadmin', password='testpassword')
        response = self.client.post(reverse('create_genre'), data={'name': 'Test Genre'})
        self.assertRedirects(response, reverse('afisha'))
        self.assertTrue(Genre.objects.filter(name='Test Genre').exists())

    def test_create_genre_view_with_invalid_data_by_superuser(self):
        self.client.login(username='testadmin', password='testpassword')
        response = self.client.post(reverse('create_genre'), data={'name': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_afisha_item.html')
        self.assertFalse(Genre.objects.filter(name='').exists())

    def test_create_genre_view_by_regular_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('create_genre'))
        self.assertEqual(response.status_code, 302)

class TestCreateHallView(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            username='testadmin', password='testpassword'
        )
        self.regular_user = User.objects.create_user(
            username='testuser', password='testpassword'
        )

    def test_create_hall_view_with_valid_data_by_superuser(self):
        self.client.login(username='testadmin', password='testpassword')
        response = self.client.post(reverse('create_hall'), data={
            'name': 'Test Hall',
            'capacity': 100,
        })
        self.assertRedirects(response, reverse('afisha'))
        self.assertTrue(Hall.objects.filter(name='Test Hall').exists())

    def test_create_hall_view_with_invalid_data_by_superuser(self):
        self.client.login(username='testadmin', password='testpassword')
        response = self.client.post(reverse('create_hall'), data={'name': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_afisha_item.html')
        self.assertFalse(Hall.objects.filter(name='').exists())

    def test_create_hall_view_by_regular_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('create_hall'))
        self.assertEqual(response.status_code, 302)

class TestCreateMovieView(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            username='testadmin', password='testpassword'
        )
        self.regular_user = User.objects.create_user(
            username='testuser', password='testpassword'
        )

        self.genre1 = Genre.objects.create(name='Comedy')

    def test_create_movie_view_with_valid_data_by_superuser(self):
        self.client.login(username='testadmin', password='testpassword')
        response = self.client.post(reverse('create_movie'), data={
            'title': 'Test Movie',
            'description': 'Test description',
            'country': 'Test country',
            'genres': [self.genre1],
            'duration': 120,
            'image': get_test_image()
        }, files={'image': get_test_image()})
        self.assertEqual(response.status_code, 200)

    def test_create_movie_view_with_invalid_data_by_superuser(self):
        self.client.login(username='testadmin', password='testpassword')
        response = self.client.post(reverse('create_movie'), data={'title': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_afisha_item.html')
        self.assertFalse(Movie.objects.filter(title='').exists())

    def test_create_movie_view_by_regular_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('create_movie'))
        self.assertEqual(response.status_code, 302)

class TestCreateShowtimeView(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            username='testadmin', password='testpassword'
        )
        self.regular_user = User.objects.create_user(
            username='testuser', password='testpassword'
        )

    def test_create_showtime_view_with_invalid_data_by_superuser(self):
        self.client.login(username='testadmin', password='testpassword')
        response = self.client.post(reverse('create_showtime'), data={
            'movie': 1,
            'time': '2023-05-24 18:00:00',
            'hall': 1
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_afisha_item.html')
        self.assertFalse(Showtime.objects.filter(
            time='2023-05-24 18:00:00'
        ).exists())

    def test_create_showtime_view_by_regular_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('create_showtime'))
        self.assertEqual(response.status_code, 302)

class TestGetUsersView(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            username='testadmin', password='testpassword'
        )
        self.staff_user = User.objects.create_user(
            username='teststaff', password='testpassword', is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='testclient', password='testpassword'
        )

    def test_get_users_view_by_superuser(self):
        self.client.login(username='testadmin', password='testpassword')
        response = self.client.get(reverse('get_users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users.html')
        self.assertIn(self.staff_user, response.context['staff'])
        self.assertIn(self.regular_user, response.context['clients'])

    def test_get_users_view_by_regular_user(self):
        self.client.login(username='testclient', password='testpassword')
        response = self.client.get(reverse('get_users'))
        self.assertEqual(response.status_code, 302)

class EditEmployeeByIDViewTests(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='superuser', password='testpassword'
        )
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.employee = Employee.objects.create(
            user=User.objects.create_user(
                username='employee', password='testpassword'
            ),
            position='Manager'
        )

    def test_edit_employee_by_id_view_superuser(self):
        client = Client()
        client.login(username='superuser', password='testpassword')
        response = client.get(reverse('edit_employee_by_id') + f'?employee_id={self.employee.pk}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_afisha_item.html')
        self.assertIsInstance(response.context['form'], EmployeeForm)
        self.assertEqual(response.context['item_name'], 'Employee')

        new_position = 'Director'
        response = client.post(
            reverse('edit_employee_by_id') + f'?employee_id={self.employee.pk}',
            data={'position': new_position}
        )
        self.assertEqual(response.status_code, 302)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.position, new_position)

    def test_edit_employee_by_id_view_non_superuser(self):
        client = Client()
        client.login(username='testuser', password='testpassword')
        response = client.get(reverse('edit_employee_by_id') + f'?employee_id={self.employee.pk}')
        self.assertEqual(response.status_code, 302)

    def test_edit_employee_by_id_view_no_authentication(self):
        client = Client()
        response = client.get(reverse('edit_employee_by_id') + f'?employee_id={self.employee.pk}')
        self.assertEqual(response.status_code, 302)

class TestMakeEmployeeView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass', is_superuser=True)
        self.regular_user = User.objects.create_user(username='regularuser', password='regularpass')

    def test_make_employee_with_superuser(self):
        request = self.factory.post(reverse('make_employee', args=[self.regular_user.id]))
        request.user = self.user
        response = make_employee(request, self.regular_user.id)
        self.assertEqual(response.status_code, 302)
        self.regular_user.refresh_from_db()
        self.assertTrue(self.regular_user.is_staff)
        self.assertTrue(Employee.objects.filter(user=self.regular_user).exists())

    def test_make_employee_with_non_superuser(self):
        request = self.factory.post(reverse('make_employee', args=[self.regular_user.id]))
        request.user = self.regular_user
        response = make_employee(request, self.regular_user.id)
        self.assertEqual(response.status_code, 302)
        self.regular_user.refresh_from_db()
        self.assertFalse(self.regular_user.is_staff)
        self.assertFalse(Employee.objects.filter(user=self.regular_user).exists())

    def test_make_employee_with_invalid_id(self):
        request = self.factory.post(reverse('make_employee', args=[999]))
        request.user = self.user
        response = make_employee(request, 999)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Employee.objects.filter(user__id=999).exists())

class MakeTicketViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.staff_user = User.objects.create_user(username='staffuser', password='staffpass', is_staff=True)
        self.employee = Employee.objects.create(user=self.staff_user)
        self.hall = Hall.objects.create(name='1', capacity=300)
        self.movie = Movie.objects.create()
        self.movie = Movie.objects.create(
            title='Inception',
            country='USA',
            budget=200000000,
            poster=get_test_image(),
            description='A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea in the mind of a CEO.',
            rate=8.8,
            age_category=13,
            duration=timedelta(hours=2, minutes=28),
            language='en'
        )
        self.showtime = Showtime.objects.create(id=1, time=timezone.now(), hall=self.hall, movie=self.movie)
        self.coupon = Coupon.objects.create(code_phrase='TESTCOUPON', discount=0.20)

    def test_make_ticket_with_valid_coupon(self):
        request = self.factory.post(reverse('make_ticket', args=[self.showtime.id]), {'entered_code': 'TESTCOUPON'})
        request.user = self.user
        response = make_ticket(request, self.showtime.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ticket.objects.count(), 1)
        ticket = Ticket.objects.first()
        self.assertEqual(ticket.client, self.user)
        self.assertEqual(ticket.showtime, self.showtime)
        self.assertEqual(ticket.coupon, self.coupon)

    def test_make_ticket_with_invalid_coupon(self):
        request = self.factory.post(reverse('make_ticket', args=[self.showtime.id]), {'entered_code': 'INVALIDCOUPON'})
        request.user = self.user
        response = make_ticket(request, self.showtime.id)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There is no such coupon. Enter an existing coupon or leave the field blank')
        self.assertEqual(Ticket.objects.count(), 0)

    def test_make_ticket_with_used_coupon(self):
        request = self.factory.post(reverse('make_ticket', args=[self.showtime.id]), {'entered_code': 'TESTCOUPON'})
        request.user = self.user
        self.coupon.use_coupon(self.user)
        response = make_ticket(request, self.showtime.id)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This coupon has already been used')
        self.assertEqual(Ticket.objects.count(), 0)

    def test_make_ticket_for_staff_user(self):
        request = self.factory.post(reverse('make_ticket', args=[self.showtime.id]), {'entered_code': 'TESTCOUPON'})
        request.user = self.staff_user
        response = make_ticket(request, self.showtime.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ticket.objects.count(), 1)
        ticket = Ticket.objects.first()
        self.assertEqual(ticket.cashier, self.employee)
        self.assertEqual(ticket.showtime, self.showtime)
        self.assertEqual(ticket.coupon, self.coupon)

class TestGetMoviesStatContext(TestCase):
    def setUp(self):
        # Create some test data
        self.movie1 = Movie.objects.create(title='Movie 1')
        self.movie2 = Movie.objects.create(title='Movie 2')
        self.movie3 = Movie.objects.create(title='Movie 3')

        self.hall1 = Hall.objects.create(name='Hall 1')
        self.hall2 = Hall.objects.create(name='Hall 2')

        self.showtime1 = Showtime.objects.create(movie=self.movie1, hall=self.hall1, time='2023-05-01 10:00:00', price=10.0)
        self.showtime2 = Showtime.objects.create(movie=self.movie1, hall=self.hall2, time='2023-05-02 15:00:00', price=12.0)
        self.showtime3 = Showtime.objects.create(movie=self.movie2, hall=self.hall1, time='2023-05-03 20:00:00', price=15.0)
        self.showtime4 = Showtime.objects.create(movie=self.movie3, hall=self.hall2, time='2023-05-04 18:00:00', price=8.0)

        self.ticket1 = Ticket.objects.create(showtime=self.showtime1, time='2023-05-03 20:00:00')
        self.ticket2 = Ticket.objects.create(showtime=self.showtime1, time='2023-05-03 20:00:00')
        self.ticket3 = Ticket.objects.create(showtime=self.showtime2, time='2023-05-03 20:00:00')
        self.ticket4 = Ticket.objects.create(showtime=self.showtime3, time='2023-05-03 20:00:00')
        self.ticket5 = Ticket.objects.create(showtime=self.showtime3, time='2023-05-03 20:00:00')
        self.ticket6 = Ticket.objects.create(showtime=self.showtime4, time='2023-05-03 20:00:00')

    def test_get_movies_stat_context(self):
        context = get_movies_stat_context()

        # Check the structure of the context
        self.assertIn('stat_type', context)
        self.assertEqual(context['stat_type'], 'movies')
        self.assertIn('movie_stats', context)
        self.assertIn('histogram_tickets', context)
        self.assertIn('histogram_revenue', context)

        # Check the movie_stats data
        self.assertEqual(len(context['movie_stats']), 3)
        self.assertEqual(context['movie_stats'][self.movie1]['tickets_sold'], 3)
        self.assertEqual(context['movie_stats'][self.movie1]['revenue'], 32.0)
        self.assertEqual(context['movie_stats'][self.movie2]['tickets_sold'], 2)
        self.assertEqual(context['movie_stats'][self.movie2]['revenue'], 30.0)
        self.assertEqual(context['movie_stats'][self.movie3]['tickets_sold'], 1)
        self.assertEqual(context['movie_stats'][self.movie3]['revenue'], 8.0)

class GetStatisticsTestCase(TestCase):
    def setUp(self):
        # Create some genres
        genre1 = Genre.objects.create(name='Action')
        genre2 = Genre.objects.create(name='Comedy')

        # Create some movies
        self.movie1 = Movie.objects.create(title='Movie 1', country='USA', budget=1000000, description='A great movie', rate=7.5)
        self.movie2 = Movie.objects.create(title='Movie 2', country='Canada', budget=2000000, description='An awesome movie', rate=8.0)
        self.movie1.genres.set([genre1])
        self.movie2.genres.set([genre2])

        # Create a hall
        self.hall1 = Hall.objects.create(name='Hall 1', capacity=150)
        self.hall2 = Hall.objects.create(name='Hall 2', capacity=200)

        # Create showtimes
        self.showtime1 = Showtime.objects.create(movie=self.movie1, hall=self.hall1, time=timezone.now() + timedelta(days=1), price=10.0)
        self.showtime2 = Showtime.objects.create(movie=self.movie2, hall=self.hall2, time=timezone.now() + timedelta(days=2), price=15.0)

        # Create users
        self.client1 = User.objects.create_user(username='client1', password='password1', is_staff=False)
        self.client2 = User.objects.create_user(username='client2', password='password2', is_staff=False)
        self.admin = User.objects.create_superuser(username='admin', password='password', is_staff=True)

        # Create tickets
        self.ticket1 = Ticket.objects.create(showtime=self.showtime1, client=self.client1, time=timezone.now())
        self.ticket2 = Ticket.objects.create(showtime=self.showtime1, client=self.client2, time=timezone.now())
        self.ticket3 = Ticket.objects.create(showtime=self.showtime2, client=self.client1, time=timezone.now())

    def test_get_movies_statistics(self):
        # Test the POST request for movie statistics
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('get_statistics'), {'stat_type': 'movies'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statistics.html')
        self.assertIn('movie_stats', response.context)
        self.assertIn('histogram_tickets', response.context)
        self.assertIn('histogram_revenue', response.context)

    def test_get_clients_statistics(self):
        # Test the POST request for client statistics
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('get_statistics'), {'stat_type': 'clients'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statistics.html')
        self.assertIn('client_stats', response.context)
        self.assertIn('histogram_age', response.context)

    def test_unauthorized_access(self):
        # Test unauthorized access to the view
        response = self.client.post(reverse('get_statistics'), {'stat_type': 'movies'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/statistics/')

class GetMoviesTestCase(TestCase):
    def setUp(self):
        # Create genres
        self.genre_action = Genre.objects.create(name='Action')
        self.genre_comedy = Genre.objects.create(name='Comedy')

        # Create movies
        self.movie1 = Movie.objects.create(title='Movie 1', country='USA', description='A great action movie', rate=7.5)
        self.movie2 = Movie.objects.create(title='Movie 2', country='Canada', description='A hilarious comedy movie', rate=8.0)
        self.movie3 = Movie.objects.create(title='Movie 3', country='USA', description='Another action movie', rate=6.5)

        # Assign genres to movies
        self.movie1.genres.add(self.genre_action)
        self.movie2.genres.add(self.genre_comedy)
        self.movie3.genres.add(self.genre_action)

        # Create users
        self.superuser = User.objects.create_superuser(username='admin', password='password')
        self.regular_user = User.objects.create_user(username='user', password='password')

    def test_superuser_access(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('get_movies'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movies.html')

    def test_regular_user_access(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('get_movies'))
        self.assertEqual(response.status_code, 302)

    def test_anonymous_user_access(self):
        response = self.client.get(reverse('get_movies'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/afisha/movies/')  # Adjust the login URL if necessary

    def test_movie_title_filter(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('get_movies'), {'movie_title': 'Movie 1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Movie 1')
        self.assertNotContains(response, 'Movie 2')
        self.assertNotContains(response, 'Movie 3')

    def test_movie_country_filter(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('get_movies'), {'movie_country': 'Canada'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Movie 2')
        self.assertNotContains(response, 'Movie 1')
        self.assertNotContains(response, 'Movie 3')

    def test_genre_filter(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('get_movies'), {'genre': 'Action'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Movie 1')
        self.assertContains(response, 'Movie 3')
        self.assertNotContains(response, 'Movie 2')

    def test_combined_filters(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('get_movies'), {'movie_title': 'Movie', 'movie_country': 'USA', 'genre': 'Action'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Movie 1')
        self.assertNotContains(response, 'Movie 2')
        self.assertContains(response, 'Movie 3')

    def test_session_storage(self):
        self.client.login(username='admin', password='password')
        self.client.get(reverse('get_movies'), {'movie_title': 'Movie 1', 'movie_country': 'USA', 'genre': 'Action'})
        session = self.client.session
        self.assertEqual(session['search_movie_title'], 'Movie 1')
        self.assertEqual(session['search_movie_country'], 'USA')
        self.assertEqual(session['selected_genre'], 'Action')

class DeleteMovieByIdTestCase(TestCase):
    def setUp(self):
        # Create movies
        self.movie1 = Movie.objects.create(title='Movie 1', country='USA', description='A great action movie', rate=7.5)
        self.movie2 = Movie.objects.create(title='Movie 2', country='Canada', description='A hilarious comedy movie', rate=8.0)

        # Create users
        self.superuser = User.objects.create_superuser(username='admin', password='password')
        self.regular_user = User.objects.create_user(username='user', password='password')

    def test_superuser_can_delete_movie(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('delete_movie_by_id'), {'movie_id': self.movie1.id})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Movie.objects.filter(id=self.movie1.id).exists())

    def test_regular_user_cannot_delete_movie(self):
        self.client.login(username='user', password='password')
        response = self.client.post(reverse('delete_movie_by_id'), {'movie_id': self.movie1.id})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Movie.objects.filter(id=self.movie1.id).exists())

    def test_anonymous_user_cannot_delete_movie(self):
        response = self.client.post(reverse('delete_movie_by_id'), {'movie_id': self.movie1.id})
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, '/accounts/login/?next=/afisha/movies/delete')
        self.assertTrue(Movie.objects.filter(id=self.movie1.id).exists())

    def test_delete_non_existent_movie(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('delete_movie_by_id'), {'movie_id': 9999})  # Non-existent movie ID
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Movie.objects.filter(id=self.movie2.id).exists())  # Ensure other movies are unaffected

class EditMovieByIdTestCase(TestCase):
    def setUp(self):
        # Create genres
        self.genre_action = Genre.objects.create(name='Action')
        self.genre_comedy = Genre.objects.create(name='Comedy')

        # Create movies
        self.movie1 = Movie.objects.create(
            title='Inception',
            country='USA',
            budget=200000000,
            poster=get_test_image(),
            description='A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea in the mind of a CEO.',
            rate=8.8,
            age_category=13,
            duration=timedelta(hours=2, minutes=28),
            language='en'
        )
        self.movie2 = Movie.objects.create(
            title='Inception2',
            country='USA',
            budget=200000000,
            poster=get_test_image(),
            description='A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea in the mind of a CEO.',
            rate=8.8,
            age_category=13,
            duration=timedelta(hours=2, minutes=28),
            language='en'
        )

        # Create users
        self.superuser = User.objects.create_superuser(username='admin', password='password')
        self.regular_user = User.objects.create_user(username='user', password='password')

    def test_superuser_can_access_edit_form(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('edit_movie_by_id') + f'?movie_id={self.movie1.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], MovieForm)

    def test_regular_user_cannot_access_edit_form(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('edit_movie_by_id') + f'?movie_id={self.movie1.id}')
        self.assertEqual(response.status_code, 302)

    def test_edit_non_existent_movie(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('edit_movie_by_id') + '?movie_id=9999')  # Non-existent movie ID
        self.assertEqual(response.status_code, 404)  # Not found

class GetGenresTestCase(TestCase):
    def setUp(self):
        # Create genres
        self.genre1 = Genre.objects.create(name='Action')
        self.genre2 = Genre.objects.create(name='Comedy')

        # Create users
        self.superuser = User.objects.create_superuser(username='admin', password='password')
        self.regular_user = User.objects.create_user(username='user', password='password')

    def test_superuser_can_access_genres(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('get_genres'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'genres.html')
        self.assertQuerysetEqual(
            response.context['genres'],
            [self.genre1, self.genre2],
            ordered=False
        )

    def test_regular_user_cannot_access_genres(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('get_genres'))
        self.assertEqual(response.status_code, 302)

    def test_anonymous_user_cannot_access_genres(self):
        response = self.client.get(reverse('get_genres'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, '/accounts/login/?next=/afisha/genres/')

class DeleteGenreByIdTestCase(TestCase):
    def setUp(self):
        # Create genres
        self.genre1 = Genre.objects.create(name='Action')
        self.genre2 = Genre.objects.create(name='Comedy')

        # Create users
        self.superuser = User.objects.create_superuser(username='admin', password='password')
        self.regular_user = User.objects.create_user(username='user', password='password')

    def test_superuser_can_delete_genre(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('delete_genre_by_id'), {'genre_id': self.genre1.id})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Genre.objects.filter(id=self.genre1.id).exists())

    def test_regular_user_cannot_delete_genre(self):
        self.client.login(username='user', password='password')
        response = self.client.post(reverse('delete_genre_by_id'), {'genre_id': self.genre1.id})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Genre.objects.filter(id=self.genre1.id).exists())

    def test_anonymous_user_cannot_delete_genre(self):
        response = self.client.post(reverse('delete_genre_by_id'), {'genre_id': self.genre1.id})
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, '/accounts/login/?next=/afisha/genres/delete')
        self.assertTrue(Genre.objects.filter(id=self.genre1.id).exists())

    def test_delete_non_existent_genre(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('delete_genre_by_id'), {'genre_id': 9999})  # Non-existent genre ID
        self.assertEqual(response.status_code, 302)  # Still redirects
        self.assertTrue(Genre.objects.filter(id=self.genre2.id).exists())  # Ensure other genres are unaffected

class EditGenreByIdTestCase(TestCase):
    def setUp(self):
        # Create genres
        self.genre1 = Genre.objects.create(name='Action')
        self.genre2 = Genre.objects.create(name='Comedy')

        # Create users
        self.superuser = User.objects.create_superuser(username='admin', password='password')
        self.regular_user = User.objects.create_user(username='user', password='password')

    def test_superuser_can_access_edit_form(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('edit_genre_by_id') + f'?genre_id={self.genre1.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_afisha_item.html')
        self.assertIsInstance(response.context['form'], GenreForm)

    def test_regular_user_cannot_access_edit_form(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('edit_genre_by_id') + f'?genre_id={self.genre1.id}')
        self.assertEqual(response.status_code, 302)

    def test_anonymous_user_cannot_access_edit_form(self):
        response = self.client.get(reverse('edit_genre_by_id') + f'?genre_id={self.genre1.id}')
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_superuser_can_edit_genre(self):
        self.client.login(username='admin', password='password')
        new_data = {
            'name': 'Updated Action'
        }
        response = self.client.post(reverse('edit_genre_by_id') + f'?genre_id={self.genre1.id}', new_data)
        self.assertEqual(response.status_code, 302)
        self.genre1.refresh_from_db()
        self.assertEqual(self.genre1.name, 'Updated Action')

    def test_edit_non_existent_genre(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('edit_genre_by_id') + '?genre_id=9999')  # Non-existent genre ID
        self.assertEqual(response.status_code, 404)  # Not found

class GetHallsTestCase(TestCase):
    def setUp(self):
        # Create halls
        self.hall1 = Hall.objects.create(name='Main Hall', capacity=200)
        self.hall2 = Hall.objects.create(name='VIP Hall', capacity=50)

        # Create users
        self.superuser = User.objects.create_superuser(username='admin', password='password')
        self.regular_user = User.objects.create_user(username='user', password='password')

    def test_superuser_can_access_halls(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('get_halls'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'halls.html')
        self.assertQuerysetEqual(
            response.context['halls'],
            [self.hall1, self.hall2],
            ordered=False
        )

    def test_regular_user_cannot_access_halls(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('get_halls'))
        self.assertEqual(response.status_code, 302)

    def test_anonymous_user_cannot_access_halls(self):
        response = self.client.get(reverse('get_halls'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, '/accounts/login/?next=/afisha/halls/')

class DeleteHallByIdTestCase(TestCase):
    def setUp(self):
        # Create halls
        self.hall1 = Hall.objects.create(name='Main Hall', capacity=200)
        self.hall2 = Hall.objects.create(name='VIP Hall', capacity=50)

        # Create users
        self.superuser = User.objects.create_superuser(username='admin', password='password')
        self.regular_user = User.objects.create_user(username='user', password='password')

    def test_superuser_can_delete_hall(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('delete_hall_by_id'), {'hall_id': self.hall1.id})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Hall.objects.filter(id=self.hall1.id).exists())

    def test_regular_user_cannot_delete_hall(self):
        self.client.login(username='user', password='password')
        response = self.client.post(reverse('delete_hall_by_id'), {'hall_id': self.hall1.id})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Hall.objects.filter(id=self.hall1.id).exists())

    def test_anonymous_user_cannot_delete_hall(self):
        response = self.client.post(reverse('delete_hall_by_id'), {'hall_id': self.hall1.id})
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, '/accounts/login/?next=/afisha/halls/delete')

    def test_delete_non_existent_hall(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('delete_hall_by_id'), {'hall_id': 9999})  # Non-existent hall ID
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Hall.objects.filter(id=self.hall2.id).exists())  # Ensure other halls are unaffected

class EditHallByIdTestCase(TestCase):
    def setUp(self):
        # Create halls
        self.hall1 = Hall.objects.create(name='Main Hall', capacity=200)
        self.hall2 = Hall.objects.create(name='VIP Hall', capacity=50)

        # Create users
        self.superuser = User.objects.create_superuser(username='admin', password='password')
        self.regular_user = User.objects.create_user(username='user', password='password')

    def test_superuser_can_access_edit_form(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('edit_hall_by_id') + f'?hall_id={self.hall1.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_afisha_item.html')
        self.assertIsInstance(response.context['form'], HallForm)

    def test_regular_user_cannot_access_edit_form(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('edit_hall_by_id') + f'?hall_id={self.hall1.id}')
        self.assertEqual(response.status_code, 302)  # Forbidden

    def test_anonymous_user_cannot_access_edit_form(self):
        response = self.client.get(reverse('edit_hall_by_id') + f'?hall_id={self.hall1.id}')
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_superuser_can_edit_hall(self):
        self.client.login(username='admin', password='password')
        new_data = {
            'name': 'Updated Main Hall',
            'capacity': 250
        }
        response = self.client.post(reverse('edit_hall_by_id') + f'?hall_id={self.hall1.id}', new_data)
        self.assertEqual(response.status_code, 302)
        self.hall1.refresh_from_db()
        self.assertEqual(self.hall1.name, 'Updated Main Hall')
        self.assertEqual(self.hall1.capacity, 250)

    def test_edit_non_existent_hall(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('edit_hall_by_id') + '?hall_id=9999')  # Non-existent hall ID
        self.assertEqual(response.status_code, 404)  # Not found

class GetShowtimesTestCase(TestCase):
    def setUp(self):
        # Create movies
        self.movie1 = Movie.objects.create(
            title='Inception',
            country='USA',
            budget=200000000,
            poster=get_test_image(),
            description='A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea in the mind of a CEO.',
            rate=8.8,
            age_category=13,
            duration=timedelta(hours=2, minutes=28),
            language='en'
        )
        self.movie2 = Movie.objects.create(
            title='Inception2',
            country='USA',
            budget=200000000,
            poster=get_test_image(),
            description='A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea in the mind of a CEO.',
            rate=8.8,
            age_category=13,
            duration=timedelta(hours=2, minutes=28),
            language='en'
        )

        # Create hall
        self.hall = Hall.objects.create(name='1', capacity=300)

        # Create showtimes
        self.showtime1 = Showtime.objects.create(movie=self.movie1, time=datetime(2024, 5, 25, 10, 0), price=10.0, hall=self.hall)
        self.showtime2 = Showtime.objects.create(movie=self.movie2, time=datetime(2024, 5, 26, 15, 0), price=12.0, hall=self.hall)

        # Create tickets
        self.ticket1 = Ticket.objects.create(showtime=self.showtime1, time=datetime(2024, 5, 26, 15, 0))
        self.ticket2 = Ticket.objects.create(showtime=self.showtime1, time=datetime(2024, 5, 26, 15, 0))
        self.ticket3 = Ticket.objects.create(showtime=self.showtime2, time=datetime(2024, 5, 26, 15, 0))

        # Create users
        self.superuser = User.objects.create_superuser(username='admin', password='password')
        self.regular_user = User.objects.create_user(username='user', password='password')

    def test_superuser_can_access_showtimes(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('get_showtimes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'showtimes.html')

    def test_regular_user_cannot_access_showtimes(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('get_showtimes'))
        self.assertEqual(response.status_code, 302)  # Forbidden

    def test_anonymous_user_cannot_access_showtimes(self):
        response = self.client.get(reverse('get_showtimes'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, '/accounts/login/?next=/afisha/showtimes/')

    def test_showtimes_filter_by_date(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('get_showtimes') + '?date=2024-05-25')
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.showtime1, response.context['profits'].keys())
        self.assertNotIn(self.showtime2, response.context['profits'].keys())

    def test_showtimes_profit_calculation(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('get_showtimes'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['profits'][self.showtime1], 20.0)
        self.assertEqual(response.context['profits'][self.showtime2], 12.0)

class DeleteShowtimeByIdTestCase(TestCase):
    def setUp(self):
        # Create a test movie
        self.movie = Movie.objects.create(
            title='Inception',
            country='USA',
            budget=200000000,
            poster=get_test_image(),
            description='A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea in the mind of a CEO.',
            rate=8.8,
            age_category=13,
            duration=timedelta(hours=2, minutes=28),
            language='en'
        )

        # Create a test hall
        self.hall = Hall.objects.create(name='1', capacity=100)

        # Create a test showtime
        self.showtime = Showtime.objects.create(movie=self.movie, time='2024-05-25 10:00:00', price=10.0, hall=self.hall)

        # Create users
        self.superuser = User.objects.create_superuser(username='admin', password='password')
        self.regular_user = User.objects.create_user(username='user', password='password')

    def test_superuser_can_delete_showtime(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('delete_showtime_by_id'), {'showtime_id': self.showtime.id})
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertEqual(Showtime.objects.filter(id=self.showtime.id).count(), 0)  # Showtime should be deleted

    def test_delete_non_existent_showtime(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('delete_showtime_by_id'), {'showtime_id': 9999})  # Non-existent showtime ID
        self.assertEqual(response.status_code, 302)  # Redirect after deletion attempt

    def test_regular_user_cannot_access_delete_view(self):
        self.client.login(username='user', password='password')
        response = self.client.post(reverse('delete_showtime_by_id'))
        self.assertEqual(response.status_code, 302)

    def test_anonymous_user_cannot_access_delete_view(self):
        response = self.client.post(reverse('delete_showtime_by_id'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, '/accounts/login/?next=/afisha/showtimes/delete')

class EditShowtimeByIdTestCase(TestCase):
    def setUp(self):
        # Create a test movie
        self.movie = Movie.objects.create(
            title='Inception',
            country='USA',
            budget=200000000,
            poster=get_test_image(),
            description='A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea in the mind of a CEO.',
            rate=8.8,
            age_category=13,
            duration=timedelta(hours=2, minutes=28),
            language='en'
        )

        # Create a test hall
        self.hall = Hall.objects.create(name='1', capacity=100)

        # Create a test showtime
        self.showtime = Showtime.objects.create(movie=self.movie, time='2024-05-25 10:00:00', price=10.0, hall=self.hall)

        # Create users
        self.superuser = User.objects.create_superuser(username='admin', password='password')
        self.regular_user = User.objects.create_user(username='user', password='password')

    def test_superuser_can_access_edit_view(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('edit_showtime_by_id') + f'?showtime_id={self.showtime.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_afisha_item.html')

    def test_regular_user_cannot_access_edit_view(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('edit_showtime_by_id') + f'?showtime_id={self.showtime.id}')
        self.assertEqual(response.status_code, 302)

    def test_anonymous_user_cannot_access_edit_view(self):
        response = self.client.get(reverse('edit_showtime_by_id') + f'?showtime_id={self.showtime.id}')
        self.assertEqual(response.status_code, 302)  # Redirect to login

class GetTicketsTestCase(TestCase):
    def setUp(self):
        # Create a test movie
        self.movie = Movie.objects.create(
            title='Inception',
            country='USA',
            budget=200000000,
            poster=get_test_image(),
            description='A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea in the mind of a CEO.',
            rate=8.8,
            age_category=13,
            duration=timedelta(hours=2, minutes=28),
            language='en'
        )

        # Create a test hall
        self.hall = Hall.objects.create(name='1', capacity=100)

        # Create a test showtime
        self.showtime = Showtime.objects.create(movie=self.movie, time='2024-05-25 10:00:00', price=10.0, hall=self.hall)

        # Create a test user
        self.client_user = User.objects.create_user(username='client', password='password')
        self.employee_user = User.objects.create_user(username='cashier', password='password')
        self.employee = Employee.objects.create(user=self.employee_user)

        # Create test tickets
        self.ticket1 = Ticket.objects.create(showtime=self.showtime, client=self.client_user, cashier=self.employee, time=datetime(2024, 5, 25, 10, 0, 0))
        self.ticket2 = Ticket.objects.create(showtime=self.showtime, client=self.client_user, cashier=self.employee, time=datetime(2024, 5, 25, 10, 0, 0))

        # Create a superuser
        self.superuser = User.objects.create_superuser(username='admin', password='password')

    def test_superuser_can_access_tickets(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('get_tickets'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tickets.html')

    def test_regular_user_cannot_access_tickets(self):
        self.client.login(username='client', password='password')
        response = self.client.get(reverse('get_tickets'))
        self.assertEqual(response.status_code, 302)

    def test_anonymous_user_cannot_access_tickets(self):
        response = self.client.get(reverse('get_tickets'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, '/accounts/login/?next=/tickets/')

    def test_tickets_filtering_and_profit_calculation(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('get_tickets'))
        self.assertEqual(response.status_code, 200)

        # Check if tickets are filtered based on criteria
        self.assertIn(self.ticket1, response.context['tickets'])
        self.assertIn(self.ticket2, response.context['tickets'])

        # Check if profit is calculated correctly
        expected_profit = self.ticket1.showtime.price + self.ticket2.showtime.price
        self.assertEqual(response.context['profit'], expected_profit)

class EditTicketByIdTestCase(TestCase):
    def setUp(self):
        # Create a test movie
        self.movie = Movie.objects.create(
            title='Inception',
            country='USA',
            budget=200000000,
            poster=get_test_image(),
            description='A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea in the mind of a CEO.',
            rate=8.8,
            age_category=13,
            duration=timedelta(hours=2, minutes=28),
            language='en'
        )

        # Create a test hall
        self.hall = Hall.objects.create(name='1', capacity=100)

        # Create a test showtime
        self.showtime = Showtime.objects.create(movie=self.movie, time='2024-05-25 10:00:00', price=10.0, hall=self.hall)

        # Create a test user
        self.client_user = User.objects.create_user(username='client', password='password')
        self.employee_user = User.objects.create_user(username='cashier', password='password')
        self.employee = Employee.objects.create(user=self.employee_user)

        # Create test tickets
        self.ticket = Ticket.objects.create(showtime=self.showtime, client=self.client_user, cashier=self.employee, time=datetime(2024, 5, 25, 10, 0, 0))

        # Create a superuser
        self.superuser = User.objects.create_superuser(username='admin', password='password')

    def test_superuser_can_access_edit_view(self):
        self.client.login(username='admin', password='password')
        response = self.client.get(reverse('edit_ticket_by_id') + f'?ticket_id={self.ticket.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_afisha_item.html')

    def test_regular_user_cannot_access_edit_view(self):
        self.client.login(username='client', password='password')
        response = self.client.get(reverse('edit_ticket_by_id') + f'?ticket_id={self.ticket.id}')
        self.assertEqual(response.status_code, 302)

    def test_anonymous_user_cannot_access_edit_view(self):
        response = self.client.get(reverse('edit_ticket_by_id') + f'?ticket_id={self.ticket.id}')
        self.assertEqual(response.status_code, 302)  # Redirect to login

class NewsViewTests(TestCase):
    def setUp(self):
        # Create a superuser for testing
        self.superuser = User.objects.create_superuser(username='admin', password='admin123', email='admin@example.com')

    def test_access_create_news_as_superuser(self):
        # Login as superuser
        self.client.login(username='admin', password='admin123')

        # Access the create_news view
        response = self.client.get(reverse('create_news'))

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the view uses the correct template
        self.assertTemplateUsed(response, 'create_afisha_item.html')

    def test_access_create_news_as_regular_user(self):
        # Create a regular user for testing
        regular_user = User.objects.create_user(username='user', password='user123', email='user@example.com')

        # Login as regular user
        self.client.login(username='user', password='user123')

        # Access the create_news view
        response = self.client.get(reverse('create_news'))

        self.assertEqual(response.status_code, 302)

    def test_create_news_with_valid_data(self):
        self.client.login(username='admin', password='admin123')

        form_data = {
            'title': 'Test News',
            'image': get_test_image(),
            'description': 'Это описание тестовой новости.'
        }

        # Instantiate the form with the form data
        form = NewsForm(data=form_data, files={'image': form_data['image']})

        # Check if the form is valid
        self.assertTrue(form.is_valid())

        # Submit the form data
        response = self.client.post(reverse('create_news'), form_data)

        self.assertEqual(response.status_code, 302)

        self.assertTrue(News.objects.filter(title='Test News').exists())

    def test_create_news_with_invalid_data(self):
        # Login as superuser
        self.client.login(username='admin', password='admin123')

        # Create an invalid form data (e.g., missing required fields)
        form_data = {}

        # Submit the form data
        response = self.client.post(reverse('create_news'), form_data)

        # Check that the form is not valid and the user stays on the same page
        self.assertEqual(response.status_code, 200)

class ReviewsTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')

        # Create some test reviews
        self.review1 = Review.objects.create(user=self.user1, rate=4, description="Good movie", time=timezone.now())
        self.review2 = Review.objects.create(user=self.user2, rate=3, description="Average movie", time=timezone.now())

    def test_reviews_view(self):
        response = self.client.get(reverse('reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews.html')

        # Check if all reviews are passed to the template context
        reviews = response.context['reviews']
        self.assertEqual(reviews.count(), 2)
        self.assertIn(self.review1, reviews)
        self.assertIn(self.review2, reviews)

class CreateReviewTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_authenticated_user_can_access_create_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('create_review'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_afisha_item.html')

    def test_authenticated_user_can_create_review(self):
        self.client.login(username='testuser', password='password')
        new_review = {
            'user' : self.user,
            'rate' : 4,
            'description' : "Good movie",
            'time' : timezone.now()
        }
        response = self.client.post(reverse('create_review'), new_review)
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        created_review = Review.objects.last()  # Get the latest review object from the database
        self.assertEqual(created_review.user, self.user)  # Check if the user matches
        self.assertEqual(created_review.description, new_review['description'])  # Check if the description matches

    def test_anonymous_user_cannot_access_create_view(self):
        response = self.client.get(reverse('create_review'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, '/accounts/login/?next=/reviews/create')

class DeleteReviewByIdTestCase(TestCase):
    def setUp(self):
        # Create a superuser
        self.superuser = User.objects.create_superuser(username='admin', password='password')

        # Create a test review
        self.review = Review.objects.create(user=self.superuser, rate=5, description="Great movie", time=timezone.now())

    def test_superuser_can_access_delete_view(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('delete_review_by_id'), {'review_id': self.review.id})
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(Review.objects.filter(id=self.review.id).exists())  # Ensure the review is deleted

    def test_regular_user_cannot_access_delete_view(self):
        User.objects.create_user(username='user', password='password')
        self.client.login(username='user', password='password')
        response = self.client.post(reverse('delete_review_by_id'), {'review_id': self.review.id})
        self.assertEqual(response.status_code, 302)

    def test_anonymous_user_cannot_access_delete_view(self):
        response = self.client.post(reverse('delete_review_by_id'), {'review_id': self.review.id})
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertRedirects(response, '/accounts/login/?next=/reviews/delete')

    def test_admin_can_delete_review(self):
        self.client.login(username='admin', password='password')

        response = self.client.post(reverse('delete_review_by_id'), {'review_id': self.review.id})

        self.assertEqual(response.status_code, 302)

        self.assertFalse(Review.objects.filter(id=self.review.id).exists())

class PrivacyPolicyViewTestCase(TestCase):
    def test_privacy_policy_view(self):
        response = self.client.get(reverse('privacy'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'privacy_policy.html')

class CouponsViewTestCase(TestCase):
    def setUp(self):
        Coupon.objects.create(code_phrase='TEST1', discount=0.1)
        Coupon.objects.create(code_phrase='TEST2', discount=0.2)

    def test_coupons_view(self):
        response = self.client.get(reverse('coupons'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'coupons.html')

        coupons = response.context['coupons']
        self.assertEqual(coupons.count(), 2)

        self.assertContains(response, 'TEST1')
        self.assertContains(response, 'TEST2')

class CreateCouponViewTestCase(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='password')

    def test_admin_can_access_create_view(self):
        self.client.login(username='admin', password='password')

        response = self.client.get(reverse('create_coupon'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'create_afisha_item.html')

    def test_create_coupon(self):
        self.client.login(username='admin', password='password')

        response = self.client.post(reverse('create_coupon'), {'code_phrase': 'TEST', 'discount': 0.1})

        self.assertEqual(response.status_code, 302)

        self.assertTrue(Coupon.objects.filter(code_phrase='TEST').exists())

class DeleteCouponViewTestCase(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='password')

        self.coupon = Coupon.objects.create(code_phrase='TEST', discount=0.1)

    def test_delete_coupon(self):
        self.client.login(username='admin', password='password')

        url = reverse('delete_coupon_by_id')

        response = self.client.post(url, {'coupon_id': self.coupon.id})

        self.assertEqual(response.status_code, 302)

        self.assertFalse(Coupon.objects.filter(id=self.coupon.id).exists())

