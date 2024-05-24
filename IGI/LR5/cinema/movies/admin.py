from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Coupon, News, Review, User
from .models import Genre, Hall, Movie, Showtime, Ticket, CompanyInfo


# admin.site.register(Genre)
# admin.site.register(Hall)
# admin.site.register(Movie)
# admin.site.register(Showtime)

admin.site.register(User, UserAdmin)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    pass

class MoviesInstanceInline(admin.TabularInline):
    model = Showtime
    extra = 0

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'rate', 'duration', 'country', 'language', 'display_genres')
    list_filter = ('rate', 'language')
    inlines = [MoviesInstanceInline]

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'hall', 'time')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    pass

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    pass

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    pass
