from django.shortcuts import render, redirect
from accounts.forms import UserForm
from accounts.models import UserProfile
from accounts.models import Transactions

# Create your views here.
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import (authenticate,
                                 login,
                                 logout
                                 )
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserRegistrationForm
from .forms import Deposit_form
from .forms import Withdrawl_form
from .models import User

def home(request):
    return render(request, 'accounts/home.html')

def user_login(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('user_success'))
        else:
            context["error"] = "Provide valid credentials !!"
            return render(request, "accounts/login.html", context)
    else:
        return render(request, "accounts/login.html", context)

@login_required(login_url="/login/")
def success(request):
    context = {}
    context['user'] = request.user
    return render(request, "accounts/success.html", context)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))



def register_view(request):  
    if request.user.is_authenticated:
        return redirect("home")
    else:
        title = "Create a Bank Account"
        form = UserRegistrationForm(
            request.POST or None,
            request.FILES or None
            )

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            new_user = authenticate(email=user.email, password=password)
            login(request, new_user)

            return redirect("home")

        context = {"title": title, "form": form}

        return render(request, "accounts/form.html", context)

def deposit(request):
    if not request.user.is_authenticated:
        raise Http404
    else:
        title = "Deposit"
        form = Deposit_form(request.POST or None,
                            request.FILES or None)

        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.user = request.user
            # adds users deposit to balance.
            deposit.user.balance += deposit.amount
            deposit.user.save()
            deposit.save()
            messages.success(request, 'You Have Deposited {} $.'
                            .format(deposit.amount))
            return redirect("home")

        context = {
                    "title": title,
                    "form": form
        }
        return render(request, "accounts/form.html", context)


def withdrawl(request):
    if not request.user.is_authenticated:
        raise Http404
    else:
        title = "Withdrawl"
        form = Withdrawl_form(request.POST or None)

        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.user = request.user

            if withdrawal.user.balance >= withdrawal.amount:

                withdrawal.user.balance -= withdrawal.amount
                withdrawal.user.save()
                withdrawal.save()
                return redirect("home")

            else:
                return render(request, "Error You Can't Withdraw Please Return To Previous Page"
                )

        context = {
                    "title": title,
                    "form": form
                  }
        return render(request, "accounts/form.html", context)


@login_required(login_url="/login/")
def account_details(request):
    # if request.user.is_authenticated:
        return render(request, "accounts/account_details.html")








