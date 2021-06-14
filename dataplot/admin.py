from django.contrib import admin
from dataplot.models import Asset, Column


class ColumnInline(admin.TabularInline):
    model = Column


class AssetAdmin(admin.ModelAdmin):
    inlines = [
        ColumnInline,
    ]


admin.site.register(Asset, AssetAdmin)
admin.site.register(Column)
