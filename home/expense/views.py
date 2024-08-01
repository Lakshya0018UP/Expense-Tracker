# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from .models import Profile, Expense

def create_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            profile = Profile(user=user, income=0, expenses=0, balance=0)
            profile.save()
            return redirect('index')
    else:
        form = UserRegistrationForm()

    return render(request, 'create_user.html', {'form': form})

def index(request):
    profile = Profile.objects.filter(user=request.user).first()
    expenses = Expense.objects.filter(user=request.user)
    if request.method == "POST":
        text = request.POST.get("type")
        expense_type = request.POST.get("expense_type")
        amount = request.POST.get("amount")
        parti = request.POST.get("participants")
        method = request.POST.get("method")

        expense = Expense(name=text, parti=parti, expense_type=expense_type, user=request.user, method=method, amount=amount)
        expense.save()
        if expense_type == "Positive" and method == "Equal":
            profile.balance += (float(amount)) / len(parti.split(","))
            profile.expenses += (float(amount)) / len(parti.split(","))
        elif expense_type == "Positive" and method == "Exact":
            profile.balance += float(amount)
        elif expense_type == "Positive" and method == "Percentage":
            profile.balance += float(amount)
        else:
            profile.expenses += float(amount)
            profile.balance -= float(amount)

        profile.save()
        return redirect("/")

    context = {"profile": profile, "expenses": expenses}
    return render(request, "index.html", context)
