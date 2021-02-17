from django.db import models
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from pilkit.processors import ResizeToFit, ResizeToFill
from django.conf import settings
from utils.models import ContentTypeRestrictedFileField

class SEOModel(models.Model):
    seo_title = models.CharField(_("Titolo SEO"), help_text=_("Massimo 65 caratteri"), max_length=65, blank=True, null=True)
    seo_description = models.CharField(_("Descrizione SEO"), help_text=_("Massimo 160 caratteri"), max_length=160, blank=True, null=True)
    seo_kwywords = models.CharField(_("Parole chiave SEO"), help_text=_("Parole chiave separate da una virgola"), max_length=255, blank=True, null=True)
    seo_author = models.CharField(_("Autore SEO"), help_text=_("Autore"), max_length=255, blank=True, null=True)
    seo_noindex = models.BooleanField(_("NOINDEX SEO"), default=0)
    seo_nofollow = models.BooleanField(_("NOFOLLOW SEO"), default=0)

    og_type = models.CharField(_("Tipo OG"), help_text=_("Tipo OG. Es.: article, book, ..."), max_length=255, default='article')
    og_title = models.CharField(_("Titolo OG"), help_text=_("Titolo OG"), max_length=255, blank=True, null=True)
    og_description = models.CharField(_("Descrizione OG"), help_text=_("Descrizione OG"), max_length=255, blank=True, null=True)

    og_image = ContentTypeRestrictedFileField(
        upload_to="OGImage",
        content_types=settings.IMAGE_CONTENT_TYPES,
        max_upload_size=settings.IMAGE_MAX_UPLOAD_SIZE,
        null=True, blank=True, verbose_name=_('Immaigne OG'))

    def _google_preview(self):
        return mark_safe(render_to_string(template_name="admin/_google_preview.html", context={'object':self}))
    _google_preview.allow_tags = True

    class Meta:
        abstract = True


class CkEditorImage(models.Model):
    image = ContentTypeRestrictedFileField(
                upload_to="AuditImage",
                content_types=settings.IMAGE_CONTENT_TYPES,
                max_upload_size=settings.IMAGE_MAX_UPLOAD_SIZE,
                null=True, blank=True, verbose_name=_('immagine'))
    created = models.DateTimeField(_("Creato"), auto_now_add=True)
    modified = models.DateTimeField(_("Modificato"), auto_now=True)

    class Meta():
        verbose_name = _("Immagine ckeditor")
        verbose_name_plural = _("Immagini ckeditor")
