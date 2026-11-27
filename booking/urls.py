from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('destinations/', views.destinations_view, name='destinations'),
    path('place/<int:place_id>/', views.place_detail, name='place_detail'),
    path("add-destination/", views.add_destination, name="add_destination"),
    path("edit-destination/<int:place_id>/", views.edit_destination, name="edit_destination"),
    path("delete-destination/<int:place_id>/", views.delete_destination, name="delete_destination"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("booking/<int:destination_id>/", views.booking_view, name="booking"),
    path("my-bookings/", views.my_bookings_view, name="my_bookings"),
]


