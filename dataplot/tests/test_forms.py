from django.test import TestCase
from dataplot.forms import QueryForm


class QueryFormTest(TestCase):
    def test_query_form_start_date_field_label(self):
        form = QueryForm()
        self.assertTrue(form.fields['start_date'].label is None or form.fields['start_date'].label == 'start_date')

    def test_query_form_end_date_field_label(self):
        form = QueryForm()
        self.assertTrue(form.fields['end_date'].label is None or form.fields['end_date'].label == 'end_date')

    def test_query_form_asset_field_label(self):
        form = QueryForm()
        self.assertTrue(form.fields['asset'].label is None or form.fields['asset'].label == 'asset')

    def test_query_form_column_field_label(self):
        form = QueryForm()
        self.assertTrue(form.fields['column'].label is None or form.fields['column'].label == 'column')

    def test_query_form_correct_inputs(self):
        start_date = '2020-10-02'
        end_date = '2020-10-10'
        asset = 'WTG01'
        column = 'Amb_Temp_Avg'
        form = QueryForm(data={'start_date': start_date,
                               'end_date': end_date,
                               'asset': asset,
                               'column': column})
        self.assertTrue(form.is_valid())

    def test_query_form_end_date_before_start_date(self):
        start_date = '2020-10-10'
        end_date = '2020-10-02'
        asset = 'WTG01'
        column = 'Amb_Temp_Avg'
        form = QueryForm(data={'start_date': start_date,
                               'end_date': end_date,
                               'asset': asset,
                               'column': column})
        self.assertFalse(form.is_valid())
