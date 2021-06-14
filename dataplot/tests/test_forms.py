from django.test import TestCase
from dataplot.forms import QueryForm


class QueryFormTest(TestCase):
    def test_query_form_start_date_field_label(self):
        form = QueryForm()
        self.assertTrue(form.fields['start_date'].label is None or form.fields['start_date'].label == 'start_date')

    def test_query_form_start_date_length(self):
        form = QueryForm()
        max_length = form.fields['start_date'].max_length
        self.assertEqual(max_length, 100)

    def test_query_form_start_date_initial_value(self):
        form = QueryForm()
        initial_value = form.fields['start_date'].initial['start_date']
        self.assertEqual(initial_value, '')

    def test_query_form_end_date_field_label(self):
        form = QueryForm()
        self.assertTrue(form.fields['end_date'].label is None or form.fields['end_date'].label == 'end_date')

    def test_query_form_end_date_length(self):
        form = QueryForm()
        max_length = form.fields['end_date'].max_length
        self.assertEqual(max_length, 100)

    def test_query_form_end_date_initial_value(self):
        form = QueryForm()
        initial_value = form.fields['end_date'].initial['end_date']
        self.assertEqual(initial_value, '')
        
    def test_query_form_asset_field_label(self):
        form = QueryForm()
        self.assertTrue(form.fields['asset'].label is None or form.fields['asset'].label == 'asset')

    def test_query_form_asset_length(self):
        form = QueryForm()
        max_length = form.fields['asset'].max_length
        self.assertEqual(max_length, 100)

    def test_query_form_asset_initial_value(self):
        form = QueryForm()
        initial_value = form.fields['asset'].initial['asset']
        self.assertEqual(initial_value, '')

    def test_query_form_asset_error_message(self):
        form = QueryForm()
        error_message = form.fields['asset'].error_messages['required']
        self.assertEqual(error_message, 'Error! Query(s) incorrectly entered. Please revise and try again.')
        
    def test_query_form_column_field_label(self):
        form = QueryForm()
        self.assertTrue(form.fields['column'].label is None or form.fields['column'].label == 'column')

    def test_query_form_column_length(self):
        form = QueryForm()
        max_length = form.fields['column'].max_length
        self.assertEqual(max_length, 100)

    def test_query_form_column_initial_value(self):
        form = QueryForm()
        initial_value = form.fields['column'].initial['column']
        self.assertEqual(initial_value, '')

    def test_query_form_column_error_message(self):
        form = QueryForm()
        error_message = form.fields['column'].error_messages['required']
        self.assertEqual(error_message, 'Error! Query(s) incorrectly entered. Please revise and try again.')
        
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
