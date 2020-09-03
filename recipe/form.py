from django import forms
from .models import RecipeContent, Reply

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['Rep_content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Rep_content'].label = '댓글'
