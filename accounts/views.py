from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm

from .forms import CustomUserCreationForm


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get("next") or "index")
    else:
        form = AuthenticationForm()

    context = {"form": form}

    if form.errors:
        messages.warning(request, form.non_field_errors())

    return render(request, "login.html", context)


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("index")
    else:
        form = CustomUserCreationForm()

    context = {"form": form}

    if form.errors:
        for error in form.errors:
            for e in form.errors[error]:
                messages.warning(request, e)

    return render(request, "signup.html", context)


def logout(request):
    auth_logout(request)
    return redirect("index")
