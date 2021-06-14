from django import forms
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class QueryForm(forms.Form):
    start_date = forms.CharField(max_length=100, initial={'start_date': ''})
    end_date = forms.CharField(max_length=100, initial={'end_date': ''})
    asset = forms.CharField(max_length=100, initial={'asset': ''}, error_messages={
        'required': 'Error! Query(s) incorrectly entered. Please revise and try again.'})
    column = forms.CharField(max_length=100, initial={'column': ''}, error_messages={
        'required': 'Error! Query(s) incorrectly entered. Please revise and try again.'})

    def clean(self):
        cleaned_data = super().clean()
        start_date_str = cleaned_data.get('start_date')
        end_date_str = cleaned_data.get('end_date')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        if end_date < start_date:
            raise ValidationError(_('Error! End date earlier than start date. Please revise and try again.'),
                                  code='invalid')

        return self.cleaned_data
