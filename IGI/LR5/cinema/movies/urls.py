from django.urls import include, path, re_path
from . import views

from django.urls import re_path
from . import views

afishapatterns = [
    re_path(r'^$', views.afisha, name='afisha'),

    re_path(r'^movies/$', views.get_movies, name='get_movies'),
    re_path(r'^movies/delete$', views.delete_movie_by_id, name='delete_movie_by_id'),
    re_path(r'^movies/edit$', views.edit_movie_by_id, name='edit_movie_by_id'),
    re_path(r'^movies/create$', views.create_movie, name='create_movie'),

    re_path(r'^genres/$', views.get_genres, name='get_genres'),
    re_path(r'^genres/delete$', views.delete_genre_by_id, name='delete_genre_by_id'),
    re_path(r'^genres/edit$', views.edit_genre_by_id, name='edit_genre_by_id'),
    re_path(r'^genres/create$', views.create_genre, name='create_genre'),

    re_path(r'^halls/$', views.get_halls, name='get_halls'),
    re_path(r'^halls/delete$', views.delete_hall_by_id, name='delete_hall_by_id'),
    re_path(r'^halls/edit$', views.edit_hall_by_id, name='edit_hall_by_id'),
    re_path(r'^halls/create$', views.create_hall, name='create_hall'),

    re_path(r'^showtimes/$', views.get_showtimes, name='get_showtimes'),
    re_path(r'^showtimes/delete$', views.delete_showtime_by_id, name='delete_showtime_by_id'),
    re_path(r'^showtimes/edit$', views.edit_showtime_by_id, name='edit_showtime_by_id'),
    re_path(r'^showtimes/create$', views.create_showtime, name='create_showtime'),
]

urlpatterns = [
    re_path(r'^$', views.index, name='index'),

    re_path(r'^afisha/', include(afishapatterns)),
    re_path(r'^afisha/(?P<movie_id>\d+)/$', views.movie_detail, name='movie_detail'),

    re_path(r'^news/$', views.news, name='news'),
    re_path(r'^news/create$', views.create_news, name='create_news'),
    re_path(r'^news/edit$', views.edit_news_by_id, name='edit_news_by_id'),
    re_path(r'^news/delete$', views.delete_news_by_id, name='delete_news_by_id'),

    re_path(r'^info/$', views.info, name='info'),
    re_path(r'^info/edit$', views.edit_info, name='edit_info'),

    re_path(r'^contacts/$', views.contacts, name='contacts'),

    re_path(r'^reviews/$', views.reviews, name='reviews'),
    re_path(r'^reviews/create$', views.create_review, name='create_review'),
    re_path(r'^reviews/delete$', views.delete_review_by_id, name='delete_review_by_id'),

    re_path(r'^profile/$', views.profile, name='profile'),

    re_path(r'^privacy/$', views.privacy, name='privacy'),

    re_path(r'^tickets/$', views.get_tickets, name='get_tickets'),
    re_path(r'^tickets/edit$', views.edit_ticket_by_id, name='edit_ticket_by_id'),

    re_path(r'^users/$', views.get_users, name='get_users'),
    re_path(r'^users/edit$', views.edit_employee_by_id, name='edit_employee_by_id'),

    re_path(r'^statistics/$', views.get_statisctics, name='get_statistics'),

    re_path(r'^make-employee/(?P<id>\d+)/$', views.make_employee, name='make_employee'),
    re_path(r'^make-client/(?P<id>\d+)/$', views.make_client, name='make_client'),

    re_path(r'^make-ticket/(?P<id>\d+)/$', views.make_ticket, name='make_ticket'),

    re_path(r'^coupons/$', views.coupons, name='coupons'),
    re_path(r'^coupons/create$', views.create_coupon, name='create_coupon'),
    re_path(r'^coupons/delete$', views.delete_coupon_by_id, name='delete_coupon_by_id'),

    re_path(r'^user/registration/$', views.registration, name='registration')
]
