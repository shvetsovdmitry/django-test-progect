from django import forms
from django.contrib import messages
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, formset_factory

from django_countries.widgets import CountrySelectWidget

from .models import user_registrated
from .models import AdvUser, Article, Tag


# Registration form.
class ARegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Пароль (повторно)', widget=forms.PasswordInput, help_text='Введите тот же самый пароль еще раз для проверки.')
    
    # Check the passwords.
    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        if password1:
            password_validation.validate_password(password1)
        else:
            raise forms.ValidationError("Error")
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError('Введенные пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    # If everything OK.
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registrated.send(ARegisterUserForm, instance=user)
        return user

    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'send_messages', 'country', 'city', )
        widgets = {'country': CountrySelectWidget()}

    

class ChangeUserInfoForm(forms.ModelForm):
    
    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'first_name', 'last_name', 'send_messages', 'account_image', 'fb_url', 'tw_url', 'vk_url', 'ok_url')


class ArticleForm(forms.ModelForm):
    
    class Meta:
        model = Article
        fields = ('category', 'title', 'image', 'image_url', 'card_text', 'content', 'tags', 'author')
        widgets = {'author': forms.HiddenInput}
        
        
ArticleFormSet = formset_factory(ArticleForm)


class DeleteArticleForm(forms.Form):
    
    class Meta:
        # model = AdvUser
        fields = ('username', )