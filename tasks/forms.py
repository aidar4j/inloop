from django import forms
from tinymce.widgets import TinyMCE
from tasks.models import TASK_CATEGORIES
import datetime


class UserEditorForm(forms.Form):
    content = forms.CharField(
        label='',
        widget=TinyMCE(attrs={
            'cols': 100,
            'rows': 20
        }))


class ExerciseSubmissionForm(forms.Form):
    # TODO: Add validators for file size, ending and header
    exercise_title = forms.CharField(max_length=100,
                                     widget=forms.TextInput(attrs={
                                         'class': 'form-control'
                                     }))
    exercise_description = forms.CharField(
        label='',
        widget=TinyMCE(attrs={
            'cols': 100,
            'rows': 20
        }))
    exercise_pub_date = forms.DateTimeField(initial=datetime.datetime.now())
    exercise_dead_date = forms.DateTimeField()
    exercise_category = forms.ChoiceField(
        choices=TASK_CATEGORIES
    )
    unittest_files = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control',
        'multiple': '1'
    }))
    exercise_files = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control',
        'multiple': '1'
    }))
