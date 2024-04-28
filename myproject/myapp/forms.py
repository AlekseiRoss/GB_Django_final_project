from django import forms
from .models import *


class AddRecipeForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['category'].empty_label = '-'

    title = forms.CharField(
        max_length=100, label="Заголовок",
        widget=forms.TextInput(attrs={'class': 'form-textinput'}))
    description = forms.CharField(
        label="Описание",
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-textarea'}))
    cooking_steps = forms.CharField(
        label="Шаги приготовления",
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-textarea'}))
    preparation_time = forms.DurationField(
        label="Время приготовления",
        widget=forms.TextInput(attrs={'placeholder': 'HH:MM:SS',
                                      'class': 'form-input'}))
    image = forms.ImageField(label="Изображение")
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), label="Категория", to_field_name='pk')
    is_published = forms.BooleanField(label="Опубликовано", required=False)

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'cooking_steps', 'preparation_time',
                  'image', 'category', 'is_published']

