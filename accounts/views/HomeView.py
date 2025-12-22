from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.static.accounts.database import Expense, Income
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.views import View

class HomeView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.user = request.user
        self.template_name = "home.html"
        self.paycheck = None
        self.errors = set()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        paycheck = request.POST.get("paycheck")
        if not paycheck:
            self.errors.add("Please fill in all fields.")
        try:
            paycheck = float(paycheck)
        except ValueError:
            if not paycheck:
                pass
            else:
                self.errors.add("Please enter a number for the paycheck")
        frequency = request.POST.get("frequency")
        if not frequency:
            self.errors.add("Please fill in all fields.")

        aggression = request.POST.get("aggression")
        try:
            aggression = float(aggression)
        except ValueError:
            self.errors.add("Please fill in all fields.")
        date = request.POST.get("date")
        if not date:
            self.errors.add("Please fill in all fields.")

        fields = {"value": paycheck, "frequency": frequency, "aggression": aggression, "date": date,
                  "user": self.user}

        if self.errors:
            return render(request, self.template_name, {"paycheck_input": False, "errors": self.errors, "fields": fields})


        income = Income(**fields)

        expense_total = self.get_expense_values(income)
        end_date = self.get_end_date(income, date)


        return render(request, "budget.html", {"income": income, "to_savings": self.get_allocations(income)[0],
                                               "free_money": self.get_allocations(income)[1], "expense_total": expense_total,
                                               "end_date": end_date})

    def get_expense_values(self, income: Income):
        frequencies_dict = {"Monthly": 1, "Bi-Weekly": 2, "Weekly": 4, "Daily": 30}
        expenses = list(Expense.objects.filter(user=self.user).all())
        aligned_frequency = frequencies_dict.get(income.frequency)
        expense_values = []
        for expense in expenses:
            if expense.frequency == "One-Time":
                expense_values.append(expense.value)
                continue
            frequency_id = frequencies_dict.get(expense.frequency)
            new_value = (frequency_id/aligned_frequency) * expense.value
            expense_values.append(new_value)
        return sum(expense_values)



    def get_allocations(self, income: Income):
        aggression = income.aggression / 100
        leftover = income.value - self.get_expense_values(income)
        to_savings = round(leftover * aggression, 2)
        free_money = round(leftover - to_savings, 2)
        return [to_savings, free_money]

    def get_end_date(self, income: Income, date: str):
        date_object = datetime.strptime(date, "%Y-%m-%d").date()
        frequency_dict = {"Bi-Weekly": 14, "Weekly": 7, "Daily": 1}
        if income.frequency == "Monthly":
            end_date = date_object + relativedelta(months=1)
            return end_date
        else:
            days_added = frequency_dict.get(income.frequency)
            end_date = date_object + timedelta(days=days_added)
            return end_date
