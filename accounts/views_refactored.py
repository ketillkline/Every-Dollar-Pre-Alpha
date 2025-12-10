from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.views import View
from utils.classes import Budget
from accounts.static.accounts.database import Expense

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

            if action == "clear_single":
                expenses = Expense.objects.all().order_by("-date")
                expense_id = request.POST.get("expense_id")
                Expense.objects.filter(id=expense_id).delete()
                expenses = Expense.objects.all().order_by("-date")
                return render(request, 'expenses.html', {'expenses': expenses})

            if action == "edit":
                expense_id = request.POST.get("expense_id")
                target_expense = Expense.objects.get(id=expense_id)
                expenses = Expense.objects.all().order_by("-date")
                return render(request, 'expenses.html', {'expenses': expenses, 'editing': True, "target_expense": target_expense})

            if action == 'cancel':
                expenses = Expense.objects.all().order_by("-date")
                return render(request, 'expenses.html',
                              {'expenses': expenses, 'editing': False,})
            if action == 'add_edited':
                expenses = Expense.objects.all().order_by("-date")
                expense_id = request.POST.get('expense_id')
                if not expense_id:
                    return render(request, "expenses.html", {"edit_error": "Please fill in all required fields", "editing": True, "expenses": expenses})
                target_expense = Expense.objects.get(id=expense_id)
                target_expense.name = request.POST.get("edited_name")
                target_expense.date = request.POST.get("edited_date")
                target_expense.value = request.POST.get("edited_value")
                try:
                    target_expense.value = float(target_expense.value)
                except ValueError:
                    errors.append("Error message")
                target_expense.frequency = request.POST.get("edited_frequency")
                target_expense.method = request.POST.get("edited_method")
                target_expense.category = request.POST.get("edited_category")
                target_expense.description = request.POST.get("edited_description")
                if not target_expense.name or not target_expense.value or not target_expense.frequency or not target_expense.method:
                    return render(request, 'expenses.html', {'edit_error': "Please fill in all required fields", 'editing': True, 'expenses': expenses,
                                                             "target_expense.name": target_expense.name, "target_expense.date": target_expense.date,
                                                             "target_expense.value": target_expense.value, "target_expense.frequency": target_expense.frequency,
                                                             "target_expense.method": target_expense.method, "target_expense.category": target_expense.category,
                                                             "target_expense.description": target_expense.description})
                target_expense.save()
                expenses = Expense.objects.all().order_by("-date")
                return render(request, 'expenses.html', {'expenses': expenses, 'editing': False})

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
