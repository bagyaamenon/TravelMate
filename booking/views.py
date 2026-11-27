from django.shortcuts import render, get_object_or_404, redirect
from .models import Destination
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import UserProfile
from .models import Booking
from django.core.paginator import Paginator



def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            auth_login(request, user)
            return redirect("dashboard")

        return render(request, "login.html", {
            "error": "Invalid username or password!"
        })

    return render(request, "login.html")



@login_required(login_url="login")
def dashboard(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    return render(request, "dashboard.html", {
        "username": request.user.username,
        "profile": profile
    })


@login_required(login_url="login")
def destinations_view(request):

    destinations_list = Destination.objects.all()

    paginator = Paginator(destinations_list, 2)

    page_number = request.GET.get('page')

    destinations = paginator.get_page(page_number)

    return render(
        request,
        "destinations.html",
        {"destinations": destinations}
    )

    


def place_detail(request, place_id):
    destination = get_object_or_404(Destination, id=place_id)
    return render(
        request,
        "place_detail.html",
        {"destination": destination}
    )
@login_required(login_url="login")
def add_destination(request):
    if request.method == "POST":
        name = request.POST.get("name")
        location = request.POST.get("location")
        description = request.POST.get("description")
        category = request.POST.get("category")
        price = request.POST.get("price")

        Destination.objects.create(
            name=name,
            location=location,
            description=description,
            category=category,
            price=price
        )

        return redirect("destinations")

    return render(request, "add_destination.html")
@login_required(login_url="login")
def edit_destination(request, place_id):
    destination = get_object_or_404(Destination, id=place_id)

    if request.method == "POST":
        destination.name = request.POST.get("name")
        destination.location = request.POST.get("location")
        destination.description = request.POST.get("description")
        destination.category = request.POST.get("category")
        destination.price = request.POST.get("price")

        destination.save()

        return redirect("destinations")

    return render(
        request,
        "edit_destination.html",
        {"destination": destination}
    )
@login_required(login_url="login")
def delete_destination(request, place_id):
    destination = get_object_or_404(Destination, id=place_id)

    if request.method == "POST":
        destination.delete()

    return redirect("destinations")
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "signup.html", {
                "error": "Passwords do not match!"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "Username already exists!"
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect("login")

    return render(request, "signup.html")
def logout_view(request):
    logout(request)
    return redirect("login")

from datetime import date, datetime
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


@login_required(login_url="login")
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = UserProfileForm(instance=profile)

    return render(request, "profile.html", {
        "form": form,
        "profile": profile
    })


@login_required(login_url="login")
def booking_view(request, destination_id):
    destination = get_object_or_404(
        Destination,
        id=destination_id
    )

    if request.method == "POST":

        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        travel_date = request.POST.get("travel_date", "")
        persons = request.POST.get("persons", "")

        error = ""

        if not full_name or len(full_name) > 100:
            error = "Please enter a valid full name."

        elif not email:
            error = "Please enter your email address."

        else:
            try:
                validate_email(email)

                if (
                    not phone
                    or len(phone) < 7
                    or len(phone) > 15
                    or not all(c in "0123456789+ -" for c in phone)
                ):
                    raise ValueError

                travel_date = datetime.strptime(
                    travel_date, "%Y-%m-%d"
                ).date()

                if travel_date < date.today():
                    raise ValueError

                persons = int(persons)

                if persons < 1 or persons > 100:
                    raise ValueError

                Booking.objects.create(
                    user=request.user,
                    destination=destination,
                    full_name=full_name,
                    email=email,
                    phone=phone,
                    travel_date=travel_date,
                    persons=persons
                )

                return render(request, "booking_success.html", {
                    "destination": destination,
                    "full_name": full_name
                })

            except (ValidationError, ValueError, TypeError):
                error = (
                    "Please check your details. Enter a valid email, "
                    "phone number, future travel date, and number of persons."
                )

        return render(request, "booking_form.html", {
            "destination": destination,
            "today": date.today().isoformat(),
            "error": error
        })

    return render(request, "booking_form.html", {
        "destination": destination,
        "today": date.today().isoformat()
    })
@login_required(login_url="login")
def my_bookings_view(request):
    bookings = Booking.objects.filter(
        user=request.user
    ).select_related("destination").order_by("-booking_date")

    return render(request, "my_bookings.html", {
        "bookings": bookings
    })


