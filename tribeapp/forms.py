from django import forms
from .models import Table
import datetime

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import re

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class TableForm(forms.ModelForm):
    # Define choices for tablename and tablenumber
    TABLENAMES = [
        ('TableA', 'TableA'),
        ('TableB', 'TableB'),
        ('TableC', 'TableC'),
        ('TableD', 'TableD'),
    ]
    
    # TABLENUMBERS = [
    #     (1, 1),
    #     (2, 2),
    #     (3, 3),
    #     (4, 4),
    # ]


    tablename = forms.ChoiceField(choices=TABLENAMES, widget=forms.Select)
    # tablenumber = forms.ChoiceField(choices=TABLENUMBERS, widget=forms.Select)

    start_timing = forms.CharField(label="Start Time", max_length=5, 
                                  widget=forms.TextInput(attrs={'placeholder': 'HH:MM', 'pattern': '([01]?[0-9]|2[0-3]):[0-5][0-9]', 'title': 'Enter time in HH:MM format'}))
    end_time = forms.CharField(label="End Time", max_length=5, 
                                widget=forms.TextInput(attrs={'placeholder': 'HH:MM', 'pattern': '([01]?[0-9]|2[0-3]):[0-5][0-9]', 'title': 'Enter time in HH:MM format'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # Date picker

    class Meta:
        model = Table
        fields = ['tablename', 'tablestatus', 'start_timing', 'end_time', 'date','amount','extra_allowances']


