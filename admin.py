from django.contrib.admin import ModelAdmin
from django.db.models import TextField
from django.forms import Textarea
from django.urls import reverse, path
from .models import CkEditorImage
from .views import DropzoneUploadSingle, DropzoneUploadMultiple, CkeditorImageUpload
from django.db import models
from .widgets import DropzoneClearableFileInput
from django.contrib import admin

#admin.site.index_template = "admin/index_site.html"

class OfficinebitAdminSite(admin.AdminSite):

    def get_urls(self):
        urls = super(OfficinebitAdminSite, self).get_urls()
        custom_urls = [
            path('dropzone/single_upload/', self.admin_view(DropzoneUploadSingle.as_view()), name="dropzone-singleupload"),
            path('dropzone/multiple_upload/', self.admin_view(DropzoneUploadMultiple.as_view()), name="dropzone-multipleupload"),
            path('ckeditor/image_upload/', self.admin_view(CkeditorImageUpload.as_view()), name="ckeditor-image-upload")
        ]
        return urls + custom_urls


officinebit_admin_site = OfficinebitAdminSite(name="offadmin")
#officinebit_admin_site.register(CkEditorImage, admin.ModelAdmin)


class AdminDropzoneTabularInline(admin.TabularInline):
    extra = 0
    max_num = 0

    dropzone_form_single_url = None
    acceptedFiles = 'application/pdf'
    maxFilesize = 2  # MB
    acceptedImages = 'image/png, image/jpeg, image/gif'
    maxImagesize = 2  # MB

    dropzone_top = True
    dropzone_form_multiple_url = None
    top_field_name = "image"
    top_acceptedFiles = 'image/png, image/jpeg, image/gif'
    top_maxFilesize = 2 # MB
    top_maxFiles = 10


    def __init__(self, parent_model, admin_site):
        super().__init__(parent_model, admin_site)
        self.dropzone_form_multiple_url = reverse("offadmin:dropzone-multipleupload")
        self.dropzone_form_single_url = reverse("offadmin:dropzone-singleupload")

    formfield_overrides = {
        models.ImageField: {'widget': DropzoneClearableFileInput},
        models.FileField: {'widget': DropzoneClearableFileInput},
        TextField: {'widget': Textarea(attrs={'class': 'custom_ckeditor'})}
    }

class AdminDropzone(admin.ModelAdmin):
    dropzone_form_url = None
    maxFilesize = 2  # MB
    acceptedFiles = 'application/pdf'
    maxImagesize = 2  # MB
    acceptedImages = 'image/png, image/jpeg, image/gif'

    formfield_overrides = {
        models.ImageField: {'widget': DropzoneClearableFileInput},
        models.FileField: {'widget': DropzoneClearableFileInput},
        TextField: {'widget': Textarea(attrs={'class': 'custom_ckeditor'})}
    }

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if not self.dropzone_form_url:
            self.dropzone_form_url = reverse("offadmin:dropzone-singleupload")
        extra_context['dropzone'] = {
            "url": self.dropzone_form_url,
            "maxFilesize": self.maxFilesize,
            "maxImagesize": self.maxImagesize,
            "acceptedFiles": self.acceptedFiles,
            "acceptedImages": self.acceptedImages
        }
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )


class CKEditor5(ModelAdmin):
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={'class': 'custom_ckeditor'})}
    }
