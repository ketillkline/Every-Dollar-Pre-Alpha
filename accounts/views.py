from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from utils.classes import Budget
from accounts.static.accounts.database import Expense


def login_view(request: HttpRequest):
    match request.method:
        case "GET":
            return render(request, 'login.html')
        case "POST":
            username = request.POST.get('username').strip()
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                print('got here')
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'login.html', {'error': 'Invalid credentials. Please try again.'})


def signup_view(request: HttpRequest):
    match request.method:
        case "GET":
            return render(request, 'signup.html')
        case "POST":
            errors = []
            username = request.POST.get('username').strip()
            password = request.POST.get('password')
            email = request.POST.get('email').strip()

        #------ EMPTY-------------#
            if not username or not password or not email:
                errors.append("Please fill in all required fields.")
        #---- FORMAT OK -----------#
            try:
                validate_password(password)
            except ValidationError:
                errors.append("Password does not fit required criteria. Please try again")

            try:
                validator = EmailValidator()
                validator(email)
            except ValidationError:
                errors.append("Invalid email. Please try again.")
        # ----- EXISTS -------------#
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                errors.append("Username or email alread associated with an account.")

        # one render at the end with the errors
            if errors:
                return render(request, 'signup.html', {'errors': errors, 'username':username, 'email':email})
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return redirect('login')


def recovery_view(request: HttpRequest):
    match request.method:
        case "GET":
            return render(request, 'recovery.html')
        case "POST":
            errors = []
            username = request.POST.get('username').strip()
            email = request.POST.get('email').strip()

            try:
                validator = EmailValidator()
                validator(email)
            except ValidationError as e:
                for msg in e:
                    errors.append(msg)

            if not username or not email:
                errors.append("Please fill in all required fields")


            if not User.objects.filter(username=username, email=email).exists():
                errors.append("Credentials don't match an existing account. "
                              "Please try again.")
            if errors:
                return render(request, 'recovery.html', {'errors': errors})

            print('here')
            return redirect('reset', username=username)



def reset_view(request: HttpRequest, username: str):
    match request.method:
        case "GET":
            return render(request, 'reset.html')
        case "POST":
            errors = []
            new_password = request.POST.get('password')
            re_password = request.POST.get('re_password')


            if new_password != re_password:
                errors.append("Passwords do not match. Please try again.")
            try:
                validate_password(new_password)
                validate_password(re_password)
            except ValidationError as e:
                for msg in e:
                    errors.append(msg)

            if errors:
                return render(request, 'reset.html', {'errors': errors})

            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            print('here')
            return redirect('login')


@login_required(login_url='login')
def home_view(request: HttpRequest):
    match request.method:
        case "GET":
            return render(request, 'home.html')
        case "POST":
            action = request.POST.get("action")
            if action == "submit":

                errors = []

                expenses: float = sum(Expense.objects.values_list("value", flat=True))
                paycheck: str = request.POST.get("paycheck")

                try:
                    paycheck = float(paycheck)
                except ValueError:
                    errors.append("Please enter a number for your paycheck")

                if errors:
                    return render(request, "home.html", {"errors": errors})

                gas = Expense.objects.filter(name="Gas", frequency="Monthly").first()
                gas = gas.value / 2
                print(gas)
                leftover = (paycheck - expenses/2)
                print(f"{paycheck} - {expenses/2} = {leftover}")
                to_savings = round((leftover * 0.7), 2)
                print(f"{leftover} * 0.7 = {to_savings}")
                free_money = round((leftover * 0.3) ,2)

                return render(request, "home.html", {"to_savings": to_savings, "free_money": free_money, "gas": gas})

def logout_view(request: HttpRequest):
    logout(request)
    return redirect('login')


def expenses_view(request: HttpRequest):
    match request.method:
        case "GET":
            expenses = Expense.objects.all().order_by("-date")
            return render(request, 'expenses.html', {'expenses': expenses} )
        case "POST":
            action = request.POST.get("action")

            if action == "clear_all":
                Expense.objects.all().delete()
                return redirect("expenses")

            budget = Budget()
            errors = []
# ----------- VARIABLE DECLARATION -------------------------------------- #
            name = request.POST.get("name")
            date = request.POST.get("date") or None
            value = request.POST.get("value")
            method = request.POST.get("method")
            frequency = request.POST.get("frequency")
            category = request.POST.get("category")
            description = request.POST.get("description")
            if not name or not value or not frequency or not method:
                errors.append("Please fill in all required fields")
            try:
                value=float(value)
            except ValueError:
                if not name or not value or not frequency or not method:
                    pass
                else:
                    errors.append("Please enter a number for a value")



            if errors:
                return render(request, 'expenses.html', {'errors': errors, 'expenses': Expense.objects.all().order_by("-date"),
                                                         "name": name, "date": date, "value": value, "method": method,
                                                         "frequency": frequency, "category": category,
                                                         "description": description} )

            Expense.objects.create(name=name, date=date, value=value, frequency=frequency, method=method,
                                   category=category, description=description)
            print(method)
            expenses = Expense.objects.all().order_by("-date")
            return render(request, 'expenses.html', {'expenses': expenses} )
