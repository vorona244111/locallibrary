from django import forms
from django.core.exceptions import ValidationError

from .models import Book, Author
from django.forms import ModelForm

import datetime


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text='Enter a date between now and 4 weeks (default 3 ).')

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        #check that date isn't past
        if data < datetime.date.today():
            raise ValidationError("Invalid date - renewal in past")

        #check that date isn't more than 4 weeks
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError("Invalid date - renewal more than 4 weeks ahead")

        # return clean data
        return data
