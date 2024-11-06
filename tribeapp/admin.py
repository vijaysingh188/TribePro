# admin.py
from django.contrib import admin
from django import forms
from .models import Table
import datetime

class TableAdminForm(forms.ModelForm):
    # HOURS = [(datetime.time(hour=h), f"{h:02}:00") for h in range(24)]  # Dropdown list for every hour
    HOURS_MINUTES = [
        (datetime.time(hour=h, minute=m), f"{h:02}:{m:02}")
        for h in range(24)
        for m in range(60)
    ]

    start_timing = forms.ChoiceField(choices=HOURS_MINUTES, widget=forms.Select, label="Start Time")

    end_time = forms.ChoiceField(choices=HOURS_MINUTES, widget=forms.Select, label="End Time")

    class Meta:
        model = Table
        fields = '__all__'

class TableAdmin(admin.ModelAdmin):
    form = TableAdminForm
    list_display = ('tablename', 'tablestatus', 'start_timing', 'end_time', 'date','created_time','update_time')
    search_fields = ('tablename',)

admin.site.register(Table, TableAdmin)
