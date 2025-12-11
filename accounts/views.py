from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from utils.classes import Budget
from accounts.static.accounts.database import Expense
from django.views import View


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


class ExpenseView(View):
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.user = request.user
        self.template_name = "expenses.html"
        self.errors = []
        self.expenses = Expense.objects.all().order_by("-date")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # expenses = Expense.objects.all().order_by("-date")
        return render(request, self.template_name, {"expenses": self.expenses})

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")

        match action:
            case "clear_all":
                return self.clear_all(request)
            case "clear_single":
                return self.clear_single(request)
            case "edit":
                return self.edit(request, *args, **kwargs)
            case "cancel":
                return self.cancel(request)
            case "add":
                return self.add(request)
            case "add_edited":
                return self.add_edited(request)



    def clear_all(self, request, *args, **kwargs):
        Expense.objects.all().delete()
        return render(request, self.template_name, {"expenses": self.expenses})

    def clear_single(self, request, *args, **kwargs):
        expense_id = request.POST.get("expense_id")
        if not expense_id:
            self.errors.append("Invalid ID. Please try again")
        Expense.objects.filter(id=expense_id).delete()
        expenses = Expense.objects.all().order_by("-date")
        return render(request, self.template_name, {"expenses": expenses})

    def edit(self, request, *args, **kwargs):
        expense_id = request.POST.get("expense_id")
        expense = Expense.objects.get(id=expense_id)
        old_fields = {"name": expense.name, "date": expense.date, "id": expense.id}

        return render(request, self.template_name, {"old_fields": old_fields ,"editing": True, "target_expense": expense, "expenses": self.expenses})


    def cancel(self, request, *args, **kwargs):
        pass

    def add(self, request, *args, **kwargs):
        missing = []
        # --------- GETTING VALUES ----------------------------------------------------------------------- #

        name = request.POST.get("name")
        if not name:
            missing.append("name")
        date = request.POST.get("date") or None
        value = request.POST.get("value")
        if not value:
            missing.append("value")
        method = request.POST.get("method")
        if not method:
            missing.append("method")
        frequency = request.POST.get("frequency")
        if not frequency:
            missing.append("frequency")
        category = request.POST.get("category")
        description = request.POST.get("description")

        # --------- ERROR HANDLING ----------------------------------------------------------------------- #

        try:
            value = float(value)
        except ValueError:
            if missing:
                pass
            else:
                self.errors.append("Please input a number as a value")

        if missing:
            self.errors.append("Please fill in all required fields")

        fields = {"name": name, "date": date, "value": value, "method": method, "frequency": frequency,
                  "category": category, "description": description}

        if self.errors:
            return render(request, self.template_name, {"errors": self.errors, "expenses": self.expenses,
                                                        "fields": fields})

        # --------- GENERATING OBJECT ----------------------------------------------------------------------- #

        new_expense = Expense.objects.create(**fields)
        print(f"added {name} ")
        expenses = Expense.objects.all().order_by("-date")
        return render(request, self.template_name, {"expenses": expenses})


    def add_edited(self, request, *args, **kwargs):
        edit_errors = []

        old_fields = {"name": expense.name, "date": expense.date, "id": expense.id}

        name = request.POST.get("edited_name")

        edited_fields = {"name": name}

        for field, value in edited_fields.items():
            setattr(expense, field, value)

        expense.save()

        expenses = Expense.objects.all().order_by("-date")



class HomeView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.user = request.user
        self.template_name = "home.html"
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest):
        return render(request, self.template_name)

    def post(self, request: HttpRequest):
        pass


