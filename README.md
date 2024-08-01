# Expense Tracker

## Overview
The Expense Tracker is a Django-based application designed to help users manage their daily expenses by tracking income and expenses, calculating balances, and handling different expense types and sharing methods.

## Features
- **User Registration**: Allows new users to create an account.
- **Expense Management**: Users can add expenses, specify the type and method of sharing, and the application updates their profile balance accordingly.
- **Profile Overview**: Displays the user's current balance and a list of expenses.

## Installation

1. **Clone the repository**
    ```sh
    git clone https://github.com/Lakshya0018UP/Expense-Tracker.git
    cd Expense-Tracker
    ```

2. **Install the dependencies**
    ```sh
    pip install -r requirements.txt
    ```

3. **Apply migrations**
    ```sh
    python manage.py migrate
    ```

4. **Run the server**
    ```sh
    python manage.py runserver
    ```

## Usage

### User Registration
- URL: `/create_user/`
- Methods: `GET`, `POST`
- Functionality: 
  - Displays a registration form for new users.
  - On form submission (`POST` request), it validates and saves the user data.
  - Creates a new `Profile` with default income, expenses, and balance set to zero.
  - Redirects to the `index` page upon successful registration.

### Index Page
- URL: `/`
- Methods: `GET`, `POST`
- Functionality: 
  - Displays the user's current profile balance and a list of expenses.
  - Allows users to add new expenses with specified type and sharing method.
  - Updates the user's profile balance based on the expense details.

## Code Explanation

### `views.py`
```python
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
