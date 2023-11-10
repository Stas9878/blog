from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, required=True, label='Ваше имя:', widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'Имя'}))
    email = forms.EmailField(required=True, label='Ваша почта:', widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'Ваш Email'}))
    to = forms.EmailField(required=True, label='Кому:', widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'Email получателя'}))
    comments = forms.CharField(required=False, label='Текст сообщения:',
                               widget=forms.Textarea(attrs={"class": "form-control mb-1", 'placeholder': 'Текст'}))

class CommentForm(forms.ModelForm):

    body = forms.CharField(required=True,
                           widget=SummernoteWidget(attrs={"class": "form-control", 'summernote': {'width': '100%', 'height': '300px'}}),
                           label='Текст')
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

class SearchForm(forms.Form):
    query = forms.CharField(label='Слово',
                            widget=forms.TextInput(attrs={
                                "class": "form-control mb-1", 'placeholder': 'Введите текст...'}
                            ))

