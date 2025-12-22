from django.http import HttpRequest
from django.shortcuts import render, redirect
from accounts.static.accounts.database import Expense
from django.views import View

class ExpenseView(View):
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.user = request.user
        self.template_name = "expenses.html"
        self.errors = []
        self.expenses = Expense.objects.filter(user=self.user).all().order_by("-date")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # expenses = Expense.objects.all().order_by("-date")
        return render(request, self.template_name, {"expenses": self.expenses, "user": self.user})

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
        Expense.objects.filter(user=request.user).all().delete()
        return render(request, self.template_name, {"expenses": self.expenses})

    def clear_single(self, request, *args, **kwargs):
        expense_id = request.POST.get("expense_id")
        if not expense_id:
            self.errors.append("Invalid ID. Please try again")
        Expense.objects.filter(id=expense_id, user=request.user).delete()
        expenses = Expense.objects.filter(user=self.user).order_by("-date")
        return render(request, self.template_name, {"expenses": expenses})

    def edit(self, request, *args, **kwargs):
        expense_id = request.POST.get("expense_id")
        expense = Expense.objects.get(id=expense_id, user=request.user)
        print(expense.value)
        old_fields = {"name": expense.name, "date": expense.date, "id": expense.id, "value": expense.value,
                      "method": expense.method,
                      "category": expense.category, "description": expense.description,
                      "frequency": expense.frequency}

        return render(request, self.template_name, {"old_fields": old_fields ,"editing": True, "expenses": self.expenses})


    def cancel(self, request, *args, **kwargs):
        return render(request, self.template_name, {"editing": False, "expenses": self.expenses})

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

        new_expense = Expense.objects.create(**fields, user=self.user)
        print(f"added {name} ")
        expenses = Expense.objects.all().filter(user=self.user).order_by("-date")
        return render(request, self.template_name, {"expenses": expenses})


    def add_edited(self, request, *args, **kwargs):
        edit_errors = []
        missing = []
        expense_id = request.POST.get("expense_id")
        expense = Expense.objects.get(id=expense_id, user=request.user)

        old_fields = {"name": expense.name, "date": expense.date, "id": expense.id, "value": expense.value,
                      "method": expense.method,
                      "category": expense.category, "description": expense.description,
                      "frequency": expense.frequency}

        name = request.POST.get("edited_name")
        if not name:
            missing.append("name")
        date = request.POST.get("edited_date") or None
        value = request.POST.get("edited_value")
        if not value:
            missing.append("value")
        method = request.POST.get("edited_method")
        if not method:
            missing.append("method")
        frequency = request.POST.get("edited_frequency")
        if not frequency:
            missing.append("frequency")
        category = request.POST.get("edited_category")
        description = request.POST.get("edited_description")

        if missing:
            edit_errors.append("Please fill in all required fields.")

        if edit_errors:
            return render(request, self.template_name, {"edit_errors": edit_errors,
                                                        "expenses": self.expenses, "editing": True, "old_fields": old_fields})


        edited_fields = {"name": name, "date": date, "value": value, "method": method, "frequency": frequency,
                  "category": category, "description": description}

        for field, value in edited_fields.items():
            setattr(expense, field, value)

        expense.save()

        expenses = Expense.objects.filter(user=request.user).all().order_by("-date")

        return render(request, self.template_name, {"expenses": expenses, "editing": False})