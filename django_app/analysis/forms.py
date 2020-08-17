from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.core.validators import RegexValidator
from .validators import name_validation


class AnalysisForm(forms.Form):

    name = forms.CharField(label='Name:', max_length=20, validators=[
        RegexValidator(r'^[a-zA-Z]+$', 'Enter a Valid Name( Letters Only )')
    ])
    c = [("M", "Male"), ("F", "Female")]

    sex = forms.ChoiceField(choices=c, widget=forms.RadioSelect, label="Sex:")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            "name",
            "sex",
            Submit('submit', "Submit", css_class="btn-success")
        )
