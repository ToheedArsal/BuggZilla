from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm 
from .models import CustomUser,Project,Bug



class SignUpForm(UserCreationForm):
	class Meta:
		model=CustomUser
		fields = ('first_name','last_name','username', 'email','user_type','password1', 'password2',)

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter your username','class': 'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 '}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter your password ','class': 'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}))

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'project_description']

class BugForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = ['bug_title', 'bug_description', 'deadline', 'screenshot', 'bug_type', 'status']
