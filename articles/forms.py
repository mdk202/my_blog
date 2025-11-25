from django import forms

from articles.models import Comment


class CommentsForm(forms.ModelForm):
    text_comment = forms.CharField(label='Ваш комментарий*',
                                   max_length=500,
                                   widget=forms.Textarea(
                                       attrs={'class': 'form-control',
                                              'placeholder': 'Введите текст комментария',
                                              'rows': '5'}))

    class Meta:
        model = Comment
        fields = ('text_comment',)