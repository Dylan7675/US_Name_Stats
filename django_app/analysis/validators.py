from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import re

def name_validation(val):
    if not re.match('^[a-zA-Z]+$', val):
        raise ValidationError("Enter a Valid Name(Letters Only)")
