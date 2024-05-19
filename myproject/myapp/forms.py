from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import *
from django.utils import timezone
from django.core.files.storage import FileSystemStorage


class AddRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'cooking_steps', 'preparation_time',
                  'image', 'category', 'is_published']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['category'].empty_label = '-'

    title = forms.CharField(
        max_length=100, label="Заголовок",
        widget=forms.TextInput(attrs={'class': 'form-textinput'}))
    description = forms.CharField(
        max_length=100,
        label="Описание",
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-textarea'}))
    cooking_steps = forms.CharField(
        max_length=200,
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

    def clean_title(self):
        title = self.cleaned_data.get('title')
        return title.strip()

    def clean_description(self):
        description = self.cleaned_data.get('description')
        return description.strip()

    def clean_cooking_steps(self):
        cooking_steps = self.cleaned_data.get('cooking_steps')
        return cooking_steps.strip()

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError("Необходимо загрузить изображение")
        return image

    def save(self, commit=True, author_id=1):
        recipe = super().save(commit=False)
        time_now = timezone.now()
        current_time_formatted = time_now.strftime('%Y%m%d%H%M%S')
        image = self.cleaned_data['image']
        fs = FileSystemStorage()
        filename = fs.save(f'recipes/images/{current_time_formatted}/'
                           f'{image.name}', image)
        recipe.image = filename
        recipe.author_id = author_id
        recipe.time_create = time_now
        recipe.time_update = time_now
        if commit:
            recipe.save()
        return recipe


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-input'}))
