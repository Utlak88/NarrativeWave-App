from django.test import TestCase
from dataplot.models import Asset, Column


class AssetModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Asset.objects.create(asset='WTG01')

    def test_asset_label(self):
        asset = Asset.objects.get(id=1)
        field_label = asset._meta.get_field('asset').verbose_name
        self.assertEqual(field_label, 'asset')

    def test_asset_max_length(self):
        asset = Asset.objects.get(id=1)
        max_length = asset._meta.get_field('asset').max_length
        self.assertEqual(max_length, 100)

    def test_asset_blank(self):
        asset = Asset.objects.get(id=1)
        blank = asset._meta.get_field('asset').blank
        self.assertEqual(blank, False)

    def test_asset_value(self):
        asset = Asset.objects.get(id=1)
        value = asset.asset
        self.assertEqual(value, 'WTG01')


class ColumnModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Asset.objects.create(asset='WTG01')
        Column.objects.create(column='Amb_Temp_Avg', asset_id=1)

    def test_column_label(self):
        column = Column.objects.get(id=1)
        field_label = column._meta.get_field('column').verbose_name
        self.assertEqual(field_label, 'column')

    def test_column_max_length(self):
        column = Column.objects.get(id=1)
        max_length = column._meta.get_field('column').max_length
        self.assertEqual(max_length, 100)

    def test_column_blank(self):
        column = Column.objects.get(id=1)
        blank = column._meta.get_field('column').blank
        self.assertEqual(blank, True)

    def test_column_default(self):
        column = Column.objects.get(id=1)
        default = column._meta.get_field('column').default
        self.assertEqual(default, '')

    def test_column_value(self):
        column = Column.objects.get(id=1)
        value = column.column
        self.assertEqual(value, 'Amb_Temp_Avg')

    def test_column_primary_key(self):
        column = Column.objects.get(id=1)
        primary_key = column.asset.pk
        self.assertEqual(primary_key, 1)
