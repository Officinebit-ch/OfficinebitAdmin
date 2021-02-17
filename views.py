from django.apps import apps
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.utils.translation import get_language
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from sorl.thumbnail import get_thumbnail

from .forms import DropzoneImageUploadForm, CKEditorImageUploadForm
from .models import CkEditorImage

class BaseCustomAdminMixin(object):
    admin_site = None

    def get_context_data(self, **kwargs):
        app_list = self.admin_site.get_app_list(self.request)
        context = {
            **self.admin_site.each_context(self.request),
            'title': self.admin_site.index_title,
            'app_list': app_list
        }
        return context


class DropzoneUploadSingle(View):
    form_class = DropzoneImageUploadForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            split_model = form.cleaned_data['model'].split(".")
            model = apps.get_model(split_model[0], split_model[1])
            instance = model.objects.get(pk=form.cleaned_data['object_id'])
            setattr(instance, form.cleaned_data['field_name'], form.cleaned_data['file'])
            instance.save()
            return JsonResponse({"esito": "success"})
        else:
            return JsonResponse({"esito": "error", "errors": str(form.errors)})


class DropzoneUploadMultiple(View):
    form_class = DropzoneImageUploadForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            split_model = form.cleaned_data['model'].split(".")
            model = apps.get_model(split_model[0], split_model[1])
            instance = model(
                related_id=form.cleaned_data['object_id']
            )
            setattr(instance, form.cleaned_data['field_name'], form.cleaned_data['file'])
            instance.save()

            try:
                lang = get_language()
                if not instance.has_translation(lang):
                    instance.create_translation(lang)
            except Exception as e:
                pass

            return JsonResponse({"esito": "success"})
        else:
            return JsonResponse({"esito": "error", "errors": str(form.errors)})



class CkeditorImageUpload(View):
    form_class = CKEditorImageUploadForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            instance = CkEditorImage()
            instance.image = form.cleaned_data['upload']
            instance.save()

            im_600 = get_thumbnail(instance.image, '600', crop='center', quality=100)
            im_800 = get_thumbnail(instance.image, '800', crop='center', quality=100)
            im_1024 = get_thumbnail(instance.image, '1024', crop='center', quality=100)
            im_1920 = get_thumbnail(instance.image, '1920', crop='center', quality=100)

            return JsonResponse({
                "urls": {
                    "default": "{}".format(instance.image.url),
                    "600": "{}".format(im_600.url),
                    "800": "{}".format(im_800.url),
                    "1024": "{}".format(im_1024.url),
                    "1920": "{}".format(im_1920.url),
                }
            })
        else:
            return JsonResponse({
                "error": {
                    "message": _("The image upload failed.")
                }
            })

