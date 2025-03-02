from django.contrib.admin import register
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.contrib.import_export.forms import (ExportForm, ImportForm, SelectableFieldsExportForm)
from django.db import models
from .models import Contact

@register(Contact)
class ContactAdmin(ModelAdmin):
    formfield_overrides = {models.TextField: {"widget": WysiwygWidget}}
    list_display = ('name', 'email', 'message', 'file_path', 'created_at')
    search_fields = ('name', 'email', 'message')
    list_filter = ('name','created_at')
    import_form_class = ImportForm
    export_form_class = ExportForm
    selectable_export_form_class = SelectableFieldsExportForm