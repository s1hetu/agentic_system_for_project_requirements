from django.core.validators import FileExtensionValidator
from django.forms import forms, CharField, FileField, Textarea, ClearableFileInput


class GenerateContentForm(forms.Form):
    requirement_text = CharField(
        widget=Textarea(attrs={'rows': 5, 'cols': 40}),
        label="Provide your requirements here.",
        required=False
    )
    requirement_doc = FileField(label="Provide your requirements file here. ", required=False,
                                widget=ClearableFileInput(attrs={'accept': '.pdf,.docx,.txt'}),
                                validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'txt'])])


class RequirementForm(forms.Form):
    requirement_text = CharField(widget=Textarea(attrs={'rows': 5, 'cols': 40}), label="Provide your requirements "
                                                                                       "here.", required=False)
    requirement_doc = FileField(label="Provide your requirements file here ", required=False,
                                widget=ClearableFileInput(attrs={'accept': '.pdf,.docx,.txt,.md'}),
                                validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'txt', 'md'])])
    questions_doc = FileField(label="Provide your questions + answers file here ", required=False,
                              widget=ClearableFileInput(attrs={'accept': '.pdf,.docx,.txt,.md'}),
                              validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'txt', 'md'])])


class PanelForm(RequirementForm):
    panel = CharField(widget=Textarea(attrs={'rows': 3, 'cols': 40}),
        label="Provide the panel details here.",
        required=False
    )

class ModuleForm(PanelForm):
     module = CharField(widget=Textarea(attrs={'rows': 3, 'cols': 40}),
        label="Provide the module details here.",
        required=False
    )
