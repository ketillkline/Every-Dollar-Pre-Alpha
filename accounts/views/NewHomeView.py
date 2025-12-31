from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import View
from accounts.static.accounts.database import Bill, Income
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist

class NewHomeView(View):
    def dispatch(self, request, *args, **kwargs):
        self.errors = set([])
        self.income_errors= set([])
        self.user = request.user
        self.template_name = "new_home.html"
        self.request = request
        try:
            self.income = Income.objects.filter(user=self.user).latest("start_date")
        except ObjectDoesNotExist:
            self.income = None

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        bills = Bill.objects.all().filter(user=self.user).order_by("-pay_day")
        total_bills = Bill.objects.aggregate(total=Sum("amount"))
        return render(request, self.template_name, {"bills": bills, "total_bills": total_bills['total'],
                                                    "income": self.income})

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


    def add_bill(self, request: HttpRequest):

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
        bills = Bill.objects.filter(user=self.user).all().order_by("-pay_day")

        if self.errors:
            return render(request, self.template_name, {"errors": self.errors, "bill_fields": fields,
                                                        "income": self.income, "bills": bills})

        new_bill = Bill.objects.create(**fields, user=self.user)
        bills = Bill.objects.all().filter(user=self.user).order_by("-pay_day")
        total_bills = Bill.objects.aggregate(total=Sum("amount"))
        return render(request, self.template_name, {"bills": bills, "total_bills": total_bills['total'], "income": self.income})

    def delete_bill(self, request: HttpRequest):
        bill_id = request.POST.get("bill_id")
        Bill.objects.filter(user=self.user, id=bill_id).delete()
        bills = Bill.objects.filter(user=self.user).order_by("-pay_day")
        total_bills = Bill.objects.aggregate(total=Sum("amount"))

        return render(request, self.template_name, {"bills": bills, "income": self.income, "total_bills": total_bills['total']})

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

        fields = {"amount": paycheck, "start_date": start_date, "end_date": end_date}

        if self.income_errors:
            return render(request, self.template_name, {"fields": fields})

        bills = Bill.objects.all().filter(user=self.user).order_by("-pay_day")
        self.income = Income.objects.create(**fields, user=self.user)
        total_bills = Bill.objects.aggregate(total=Sum("amount"))
        return render(request, self.template_name, {"income": self.income, "bills": bills, "total_bills": total_bills['total']})

    def save_edited_bill(self, request: HttpRequest):
        bill_id = request.POST.get("bill_id")
        print(bill_id)
        target_bill = Bill.objects.get(user=self.user, id=bill_id)
        if not target_bill:
            print("Not here")

        name = request.POST.get("edited_bill_name")
        amount = request.POST.get("edited_bill_amount")
        pay_day = request.POST.get("edited_bill_payday")

        edited_fields = {"name": name, "amount": amount, "pay_day": pay_day}

        for field, value in edited_fields.items():
            setattr(target_bill, field, value)
        target_bill.save()

        bills = Bill.objects.filter(user=self.user).all().order_by("-pay_day")
        total_bills = Bill.objects.aggregate(total=Sum("amount"))

        return render(request, self.template_name, {"bills": bills, "income": self.income,
                                                    "total_bills": total_bills['total'] })









