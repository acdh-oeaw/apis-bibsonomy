from django.contrib import admin
from .models import Reference, ZoteroEntry


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    pass


@admin.register(ZoteroEntry)
class ZoteroEntryAdmin(admin.ModelAdmin):
    pass
