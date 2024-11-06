from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Table(models.Model):
    tablename = models.CharField(max_length=100)
    # tablenumber = models.IntegerField()
    tablestatus = models.CharField(max_length=20, choices=[('occupied', 'Occupied'), ('reserved', 'Reserved')])
    start_timing = models.TimeField(null=True, blank=True,help_text="Enter an Time between 00:00 and 23:59")
    end_time = models.TimeField(null=True, blank=True,help_text="Enter an Time between 00:00 and 23:59")
    date = models.DateField()
    amount = models.PositiveIntegerField(default=100,validators=[MinValueValidator(50), MaxValueValidator(1000)],help_text="Enter an amount between 50 and 1000")
    extra_allowances = models.PositiveIntegerField(verbose_name="Extra Charges",default=0,blank=True,null=True,validators=[MinValueValidator(0), MaxValueValidator(1000)],) 
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True) 
    def total_amount(self):
        # Handle case where extra_allowances could be null
        extra = self.extra_allowances if self.extra_allowances is not None else 0
        return self.amount + extra

    def __str__(self):
        return f"{self.tablename} - Table  ({self.tablestatus})"
