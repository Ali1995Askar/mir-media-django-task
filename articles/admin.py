from django.contrib import admin
from . import models
from conf.utils import relational_fields


# Register your models here.

@admin.register(models.Article)
class CustomArticleAdmin(admin.ModelAdmin):
    list_display = [
        relational_fields("author"),
        "title",
        "slug",
        "status",
        "pub_date",
    ]

    search_fields = ["author", "title", "slug"]
    list_filter = [
        "status",
        "pub_date",
    ]
    list_display_links = [
        "title",
        "slug",
    ]


admin.site.site_header = 'MIR Django Task'
admin.site.site_title = 'MIR Django Task'
admin.site.index_title = 'Admin'
