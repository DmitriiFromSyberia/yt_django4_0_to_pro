from django.contrib import admin

# Register your models here.
from .models import Product

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.forms.models import BaseInlineFormSet
from django.http import HttpResponseRedirect

# admin.site.register(Product)

admin.site.site_header = "MySite administration Bykov"
admin.site.site_title = "Title of MySite administration"
admin.site.index_title = "MyAdmin"


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "description", "image", "seller"]
    search_fields = ["name", "description"]
    list_editable = ["price", "description", "image", "seller"]
    actions = ["make_zero", "copy_selected_objects"]

    def make_zero(self, request, queryset):
        queryset.update(price=0)

    make_zero.short_description = "Make zero price"

    def copy_selected_objects(self, request, queryset):
        for obj in queryset:
            # Создайте копию объекта, исключив первичный ключ
            obj.pk = None
            obj.name = "Copy of " + obj.name
            obj.save()

        self.message_user(request, _("Selected objects were successfully copied."))

    copy_selected_objects.short_description = _("Copy selected objects")


admin.site.register(Product, ProductAdmin)
