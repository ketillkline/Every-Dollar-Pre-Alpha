import re
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError

class StrongPasswordValidator:
    def validate(self, password, user=None):

        if len(password) < 8:
            raise ValidationError (_("Error"))

        if not re.search(r"[A-Z]", password):
            raise ValidationError (_("Error"))

        if not re.search(r"[a-z]", password):
            raise ValidationError (_("Error"))

        if not re.search(r"[!@#$%^&*()-+{}[]\|"':;><.,?/]', password):
            raise ValidationError (_("Error"))
