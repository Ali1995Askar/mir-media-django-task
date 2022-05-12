from django.contrib import admin
from . import models


# Register your models here.

@admin.register(models.Contact)
class CustomContactAdmin(admin.ModelAdmin):
    readonly_fields = ("email", "name", "content", "created_at",)
    list_display = [
        "email",
        "name",
        "created_at",
    ]

    search_fields = ["email", "name"]
    list_filter = [
        "created_at",
    ]
    list_display_links = [
        "email",
        "name",
    ]
