from django.forms import ClearableFileInput
from django.utils.translation import gettext_lazy as _

class DropzoneClearableFileInput(ClearableFileInput):
    template_name = 'admin/widgets/dropzone_clearable_file_input.html'
    clear_checkbox_label = _("Elimina")