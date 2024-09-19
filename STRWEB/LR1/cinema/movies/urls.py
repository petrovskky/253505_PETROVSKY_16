from django.urls import include, re_path
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

    re_path(r'^partner/create$', views.create_partner, name='create_partner'),
    re_path(r'^partner/delete$', views.delete_partner, name='delete_partner'),

    re_path(r'^afisha/', include(afishapatterns)),
    re_path(r'^afisha/(?P<movie_id>\d+)/$', views.movie_detail, name='movie_detail'),

    re_path(r'^news/$', views.news, name='news'),
    re_path(r'^news/(?P<news_id>\d+)/', views.news_full, name='news_full'),
    re_path(r'^news/create$', views.create_news, name='create_news'),
    re_path(r'^news/edit$', views.edit_news_by_id, name='edit_news_by_id'),
    re_path(r'^news/delete$', views.delete_news_by_id, name='delete_news_by_id'),

    re_path(r'^info/$', views.info, name='info'),
    re_path(r'^info/edit$', views.edit_info, name='edit_info'),

    re_path(r'^contacts/$', views.contacts, name='contacts'),

    re_path(r'^reviews/$', views.reviews, name='reviews'),
    re_path(r'^reviews/create$', views.create_review, name='create_review'),
    re_path(r'^reviews/delete$', views.delete_review_by_id, name='delete_review_by_id'),

    re_path(r'^faq/$', views.faq, name='faq'),
    re_path(r'^faq/create$', views.create_faq, name='create_faq'),
    re_path(r'^faq/edit$', views.edit_faq_by_id, name='edit_faq_by_id'),
    re_path(r'^faq/delete$', views.delete_faq_by_id, name='delete_faq_by_id'),

    re_path(r'^cart/$', views.cart, name='cart'),
    re_path(r'^cart/pay$', views.pay_for_cart, name='pay_for_cart'),
    re_path(r'^cart/edit$', views.edit_cart_item, name='edit_cart_item'),
    re_path(r'^cart/delete$', views.delete_cart_item, name='delete_cart_item'),

    re_path(r'^profile/$', views.profile, name='profile'),

    re_path(r'^privacy/$', views.privacy, name='privacy'),

    re_path(r'^tickets/$', views.get_tickets, name='get_tickets'),
    re_path(r'^tickets/edit$', views.edit_ticket_by_id, name='edit_ticket_by_id'),
    re_path(r'^tickets/delete$', views.delete_ticket_by_id, name='delete_ticket_by_id'),

    re_path(r'^users/$', views.get_users, name='get_users'),
    re_path(r'^users/edit$', views.edit_employee_by_id, name='edit_employee_by_id'),
    re_path(r'^users/positions/$', views.positions, name='positions'),
    re_path(r'^users/positions/delete$', views.delete_position_by_id, name='delete_position_by_id'),
    re_path(r'^users/positions/edit$', views.edit_position_by_id, name='edit_position_by_id'),
    re_path(r'^users/positions/create$', views.create_position, name='create_position'),

    re_path(r'^statistics/$', views.get_statisctics, name='get_statistics'),

    re_path(r'^make-employee/(?P<id>\d+)/$', views.make_employee, name='make_employee'),
    re_path(r'^make-client/(?P<id>\d+)/$', views.make_client, name='make_client'),

    re_path(r'^make-ticket/(?P<id>\d+)/$', views.make_ticket, name='make_ticket'),

    re_path(r'^add-to-cart/$', views.add_to_cart, name='add_to_cart'),

    re_path(r'^coupons/$', views.coupons, name='coupons'),
    re_path(r'^coupons/create$', views.create_coupon, name='create_coupon'),
    re_path(r'^coupons/delete$', views.delete_coupon_by_id, name='delete_coupon_by_id'),

    re_path(r'^vacancies/$', views.vacancies, name='vacancies'),
    re_path(r'^vacancies/(?P<vacancy_id>\d+)/$', views.vacancy_detail, name='vacancy_detail'),
    re_path(r'^vacancies/create$', views.create_vacancy, name='create_vacancy'),
    re_path(r'^vacancies/edit$', views.edit_vacancy_by_id, name='edit_vacancy_by_id'),
    re_path(r'^vacancies/delete$', views.delete_vacancy_by_id, name='delete_vacancy_by_id'),

    re_path(r'^user/registration/$', views.registration, name='registration'),

    re_path(r'^sandbox/$', views.sandbox, name='sandbox')
]
