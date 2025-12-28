from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import View
from accounts.static.accounts.database import Bill, Income


class NewHomeView(View):
    def dispatch(self, request, *args, **kwargs):
        self.errors = set([])
        self.income_errors= set([])
        self.user = request.user
        self.template_name = "new_home.html"
        self.request = request
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        bills = Bill.objects.all().filter(user=self.user).order_by("-pay_day")
        Income.objects.all().delete()
        return render(request, self.template_name, {"bills": bills, "add_new_clicked": False})

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        match action:
            case "add_bill":
                return self.add_bill(request)
            case "edit_bill":
                return self.edit_bill(request)
            case "delete_bill":
                return self.delete_bill(request)
            case "add_income":
                return self.add_income(request)


    def add_bill(self, request: HttpRequest):
        print("There were errors")
        name = request.POST.get("bill_name")
        if not name:
            self.errors.add("Please fill in all required fields")
        amount = request.POST.get("bill_amount")
        if not amount:
            self.errors.add("Please fill in all required fields")
        pay_day = request.POST.get("bill_pay_day")
        if not pay_day:
            self.errors.add("Please fill in all required fields")

        fields = {"name": name, "amount": amount, "pay_day": pay_day}

        if self.errors:

            return render(request, self.template_name, {"errors": self.errors, "bill_fields": fields})

        new_bill = Bill.objects.create(**fields, user=self.user)
        bills = Bill.objects.all().filter(user=self.user).order_by("-pay_day")
        return render(request, self.template_name, {"bills": bills, "add_new_clicked": False})

    def delete_bill(self, request: HttpRequest):
        bill_id = request.POST.get("bill_id")
        Bill.objects.filter(user=self.user, id=bill_id).delete()
        bills = Bill.objects.filter(user=self.user).order_by("-pay_day")
        return render(request, self.template_name, {"bills": bills})

    def add_income(self, request: HttpRequest):
        paycheck = request.POST.get("paycheck")
        if not paycheck:
            self.income_errors.add("Please fill in all required fields")
        start_date = request.POST.get("start_date")
        if not start_date:
            self.income_errors.add("Please fill in all required fields")
        end_date = request.POST.get("end_date")
        if not end_date:
            self.income_errors.add("Please fill in all required fields")

        fields = {"paycheck": paycheck, "start_date": start_date, "end_date": end_date}

        if self.income_errors:
            return render(request, self.template_name, {"fields": fields})










