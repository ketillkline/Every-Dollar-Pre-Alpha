import re
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError

class StrongPasswordValidator:
    def validate(self, password, user=None):

        if not re.search(r"[A-Z]", password):
            raise ValidationError (_("Password must contain 1 uppercase"))

        if not re.search(r"[a-z]", password):
            raise ValidationError (_("Password must contain 1 lowercase"))

        if not re.search(r"\d", password):
            raise ValidationError (_("Password must contain 1 number"))

        if not re.search(r"[!@#$%^&*()-+{}"':;><.,?/]', password):
            raise ValidationError (_("Password must contain 1 special character"))
