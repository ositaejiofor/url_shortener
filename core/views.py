from django.shortcuts import render, redirect, get_object_or_404
from .models import ShortURL
from .utils import generate_code
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import ShortURL, generate_short_code
from django.contrib.auth import login
from django.contrib.auth import logout
from .models import ShortURL



def home(request):
    short = None

    if request.method == "POST":
        url = request.POST.get("url")
        days = request.POST.get("days")
        expires_at = None

        if days:
            try:
                expires_at = timezone.now() + timedelta(days=int(days))
            except ValueError:
                expires_at = None

        if url:
            short_code = generate_short_code()
            ShortURL.objects.create(
                user=request.user if request.user.is_authenticated else None,
                original_url=url,
                short_code=short_code,
                expires_at=expires_at
            )
            short = request.build_absolute_uri('/' + short_code)

    # Stats for authenticated users
    if request.user.is_authenticated:
        recent_links = ShortURL.objects.filter(user=request.user).order_by('-created_at')[:5]
        total_links = ShortURL.objects.filter(user=request.user).count()
        total_clicks = sum(link.clicks for link in ShortURL.objects.filter(user=request.user))
    else:
        recent_links = []
        total_links = 0
        total_clicks = 0

    context = {
        "short": short,
        "recent_links": recent_links,
        "total_links": total_links,
        "total_clicks": total_clicks,
    }
    return render(request, "core/home.html", context)


def redirect_url(request, code):
    short_url = get_object_or_404(ShortURL, short_code=code)

    if short_url.is_expired():
        return render(request, "expired.html")  # create a simple "link expired" page

    # increment click counter
    short_url.clicks += 1
    short_url.save()

    return redirect(short_url.original_url)


def stats(request, code):
    link = get_object_or_404(ShortURL, short_code=code)
    return render(request, "stats.html", {"link": link})


@login_required
def dashboard(request):
    short = None

    # Handle URL shortener form submission
    if request.method == "POST":
        url = request.POST.get("url")
        days = request.POST.get("days")

        if url:
            short_url = ShortURL(original_url=url, user=request.user)
            if days:
                short_url.expires_at = timezone.now() + timedelta(days=int(days))
            short_url.save()
            short = request.build_absolute_uri('/' + short_url.short_code)

    # Fetch stats
    links = ShortURL.objects.filter(user=request.user).order_by("-created_at")
    total_links = links.count()
    total_clicks = sum(link.clicks for link in links)
    recent_links = links[:5]

    context = {
        "links": links,
        "total_links": total_links,
        "total_clicks": total_clicks,
        "recent_links": recent_links,
        "short": short,
    }

    return render(request, "core/dashboard.html", context)


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})