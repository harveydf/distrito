# -*- coding: utf-8 -*-

from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Usuario', 'class': 'input-form'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Contraseña', 'class': 'input-form'}))