from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import View
from accounts.static.accounts.database import Bill, Income
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, date, timedelta
import calendar
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(LoginRequiredMixin, View):
    login_url = "/login/"
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_base_context(request))

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        match action:
            case "add_bill":
                return self.add_bill(request)
            case "save_edited_bill":
                return self.save_edited_bill(request)
            case "delete_bill":
                return self.delete_bill(request)
            case "add_income":
                return self.add_income(request)
            case "clear_all_incomes":
                return self.clear_all_incomes(request)


    def add_bill(self, request: HttpRequest):
        errors = set([])
        name = request.POST.get("bill_name")
        if not name:
            errors.add("Please fill in all required fields")
        amount = request.POST.get("bill_amount")
        if not amount:
            errors.add("Please fill in all required fields")
        pay_day = request.POST.get("bill_pay_day")
        if not pay_day:
            errors.add("Please fill in all required fields")

        fields = {"name": name, "amount": amount, "pay_day": pay_day}

        if errors:
            return render(request, self.template_name, {"errors": errors,
                                                        **self.get_base_context(request)})

        new_bill = Bill.objects.create(**fields, user=request.user)
        return render(request, self.template_name, self.get_base_context(request))

    def delete_bill(self, request: HttpRequest):

        bill_id = request.POST.get("bill_id")

        Bill.objects.filter(user=request.user, id=bill_id).delete()

        return render(request, self.template_name, self.get_base_context(request))

    def add_income(self, request: HttpRequest):
        income_errors = set([])
        paycheck = request.POST.get("paycheck")
        if not paycheck:
            income_errors.add("New Income not submitted. Please fill in all required fields.")
        start_date = request.POST.get("start_date")
        if not start_date:
            income_errors.add("New Income not submitted. Please fill in all required fields.")
        end_date = request.POST.get("end_date")
        if not end_date:
            income_errors.add("New Income not submitted. Please fill in all required fields.")
        fields = {"amount": paycheck, "start_date": start_date, "end_date": end_date}

        if income_errors:
            return render(request, self.template_name, {"fields": fields,
                                                        "errors": income_errors, **self.get_base_context(request)})

        new_income = Income.objects.create(**fields, user=request.user)


        context = self.get_base_context(request)

        return render(request, self.template_name, context)

    def save_edited_bill(self, request: HttpRequest):
        errors = set([])
        bill_id = request.POST.get("bill_id")

        target_bill = Bill.objects.get(user=request.user, id=bill_id)
        name = request.POST.get("edited_bill_name")
        amount = request.POST.get("edited_bill_amount")
        pay_day = request.POST.get("edited_bill_payday")


        edited_fields = {"name": name, "amount": amount, "pay_day": pay_day}

        for field, value in edited_fields.items():
            setattr(target_bill, field, value)
        target_bill.save()


        return render(request, self.template_name, self.get_base_context(request))

    def get_date_object(self, date: str):
        if type(date) == str:
            return datetime.strptime(date, "%Y-%m-%d").date()
        return date

    def get_pay_period(self, start_date, end_date):
        if type(start_date) == str and type(end_date) == str:
            start_date = self.get_date_object(start_date)
            end_date = self.get_date_object(end_date)
            delta = end_date - start_date
            return delta.days
        else:
            delta = end_date - start_date
            return delta.days

    def get_base_context(self, request: HttpRequest):
        bills = Bill.objects.filter(user=request.user).all().order_by("-due", "-amount" ,"pay_day")
        total_bills = Bill.objects.filter(user=request.user).aggregate(total=Sum("amount"))
        income = self.get_income(request)
        if not income:
            self.is_due(bills, None, None)
            income = None
            pay_period_days = None
        else:
            income = self.get_income(request)
            self.is_due(list(Bill.objects.filter(user=request.user)), income.start_date, income.end_date)
            pay_period_days = self.get_pay_period(income.start_date, income.end_date)
        return {
            "bills": bills,
            "total_bills": total_bills['total'],
            "income": income,
            "pay_period_days": pay_period_days,
            "due_emoji": "✅"
        }

    def get_income(self, request: HttpRequest):
        return Income.objects.filter(user=request.user).first()

    def clear_all_incomes(self, request: HttpRequest):

        Income.objects.filter(user=request.user).all().delete()
        context = self.get_base_context(request)
        return render(request, self.template_name, context)

    def is_due(self, bills, start_date, end_date):

        if not start_date or not end_date:
            for bill in bills:
                bill.due = False
            return
        start_date = self.get_date_object(start_date)
        end_date = self.get_date_object(end_date)
        for bill in bills:
            bill_date = self.payday_to_date(int(bill.pay_day), start_date, end_date)
            if start_date <= bill_date <= end_date:
                bill.due = True

            else:
                bill.due = False

            bill.save()

    def payday_to_date(self, payday: int, start_date, end_date):
        start_year, start_month = start_date.year, start_date.month
        start_days = calendar.monthrange(start_year, start_month)[1]
        clamped_days = min(payday, start_days)
        bill_date = date(start_year, start_month, clamped_days)

        if start_date <= bill_date <= end_date:
            return bill_date
        end_year, end_month = end_date.year, end_date.month
        end_days = calendar.monthrange(end_year, end_month)[1]
        clamped_days = min(payday, end_days)
        bill_date = date(end_year, end_month, clamped_days)
        return bill_date













