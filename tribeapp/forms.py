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

    TIME_CHOICES = [('AM', 'AM'), ('PM', 'PM')]


    tablename = forms.ChoiceField(choices=TABLENAMES, widget=forms.Select)
    # tablenumber = forms.ChoiceField(choices=TABLENUMBERS, widget=forms.Select)

    # start_timing = forms.CharField(label="Start Time", max_length=5, 
    #                               widget=forms.TextInput(attrs={'placeholder': 'HH:MM', 'pattern': '([01]?[0-9]|2[0-3]):[0-5][0-9]', 'title': 'Enter time in HH:MM format'}))
    # end_time = forms.CharField(label="End Time", max_length=5, 
    #                             widget=forms.TextInput(attrs={'placeholder': 'HH:MM', 'pattern': '([01]?[0-9]|2[0-3]):[0-5][0-9]', 'title': 'Enter time in HH:MM format'}))
    start_timing = forms.CharField(
        label="Start Time",
        max_length=5,
        widget=forms.TextInput(attrs={
            'placeholder': 'HH:MM', 
            'pattern': '([01]?[0-9]|2[0-3]):[0-5][0-9]', 
            'title': 'Enter time in HH:MM format'
        })
    )
    start_am_pm = forms.ChoiceField(
        choices=TIME_CHOICES, 
        label="Start Time AM/PM", 
        widget=forms.Select()
    )

    end_time = forms.CharField(
        label="End Time",
        max_length=5,
        widget=forms.TextInput(attrs={
            'placeholder': 'HH:MM', 
            'pattern': '([01]?[0-9]|2[0-3]):[0-5][0-9]', 
            'title': 'Enter time in HH:MM format'
        })
    )

    end_am_pm = forms.ChoiceField(
        choices=TIME_CHOICES, 
        label="End Time AM/PM", 
        widget=forms.Select()
    )


    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))  # Date picker

    class Meta:
        model = Table
        fields = ['tablename', 'tablestatus', 'start_timing', 'end_time', 'date','amount','extra_allowances']


class BookingForm(forms.Form):
    TABLENAMES = [
        ('None', 'None'),
        ('TableA', 'TableA'),
        ('TableB', 'TableB'),
        ('TableC', 'TableC'),
        ('TableD', 'TableD'),
    ]
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label="Start Date"
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        }),
        label="End Date"
    )
    table = forms.ChoiceField(
        choices=TABLENAMES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

