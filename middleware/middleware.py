import os
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin


class AdminLocaleMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.path.startswith('/admin'):
            translation.activate(os.environ.get('FALLBACK_LANGUAGE', "it"))
            request.LANGUAGE_CODE = translation.get_language()