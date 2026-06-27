from django import forms
from .models import Post, Comment


class MultiFileInput(forms.ClearableFileInput):
    """Allows selecting multiple files in a single FileField."""
    allow_multiple_selected = True


class MultiFileField(forms.FileField):
    """FileField that returns a list of UploadedFile objects."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultiFileInput(attrs={'multiple': True}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(d, initial) for d in data]
        return single_file_clean(data, initial)


class PostCreateForm(forms.ModelForm):
    media_files = MultiFileField(
        widget=MultiFileInput(attrs={
            'multiple': True,
            'accept': 'image/*,video/*',
            'class': 'form-control',
            'id': 'media-upload',
        }),
        required=True,
        label='Photos / Videos',
    )

    class Meta:
        model = Post
        fields = ['caption']
        widgets = {
            'caption': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Write a caption...',
                'maxlength': 2200,
            })
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control rounded-pill',
                'placeholder': 'Add a comment...',
                'autocomplete': 'off',
            })
        }
        labels = {'text': ''}
