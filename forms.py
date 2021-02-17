# In form.py
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django import forms

class ErrorListMsg(ErrorList):
    def __unicode__(self):
        return self.as_msg()
    
    def as_msg(self):
        if not self: return u''
        return mark_safe(u'\n'.join([u'<span class="red">%s</span>' % e for e in self]))


class DropzoneImageUploadForm(forms.Form):
    file = forms.FileField()
    object_id = forms.CharField()
    model = forms.CharField()
    field_name = forms.CharField()

class CKEditorImageUploadForm(forms.Form):
    upload = forms.FileField()
