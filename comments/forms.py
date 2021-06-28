from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('message', )
        widgets = {
            'message': forms.Textarea(attrs={'class': 'uk-textarea uk-border-rounded', 'rows': "5", 'minlength': "10"})
        }
