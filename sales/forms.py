from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import StudentProfile, BookAd, InterestingTitle, Title, Wishlist

'''
New User form
'''
class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']

        if not email.endswith('@studenti.unibg.it'):
            raise forms.ValidationError('An email from UniBG is required')
        return email

'''
User info update
'''
class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['username', 'email']

'''
StudentProfile creation form
'''
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['name', 'surname', 'major']

'''
Title creation form
'''
class TitleForm(forms.ModelForm):
    class Meta:
        model = Title
        fields = ['isbn', 'name']

'''
BookAd creation form
'''
class BookAdForm(forms.ModelForm):
    class Meta:
        model = BookAd
        fields = ['title', 'seller', 'description', 'price', 'quality_class']



