from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from tribeapp.models import Table
from tribeapp.forms import TableForm
from datetime import datetime
from django.db.models import Q


class MainPageView(TemplateView):
    def get(self, request, *args, **kwargs):
        form = TableForm()
        tables = Table.objects.all()
        return render(request,'index.html',{"tables":tables,"form":form})
    def post(self, request):
        # objects = Table.objects.all()
        # form = TableForm(request.POST)
        # tablename = request.POST.get('tablename')
        # start_timing = request.POST.get('start_timing')
        # end_time = request.POST.get('end_time')
        # date = request.POST.get('date')
        
        # # Convert string inputs to datetime objects
        # start_timing = datetime.strptime(start_timing, '%H:%M').time() if start_timing else None
        # end_time = datetime.strptime(end_time, '%H:%M').time() if end_time else None
        # date = datetime.strptime(date, '%Y-%m-%d').date() if date else None


        objects = Table.objects.all()
        form = TableForm(request.POST)
        tablename = request.POST.get('tablename')
        start_timing = request.POST.get('start_timing')
        start_am_pm = request.POST.get('start_am_pm')
        end_time = request.POST.get('end_time')
        end_am_pm = request.POST.get('end_am_pm')
        date = request.POST.get('date')

        # Convert the time with AM/PM to 24-hour format
        start_time_str = f"{start_timing} {start_am_pm}"
        end_time_str = f"{end_time} {end_am_pm}"
        start_timing = datetime.strptime(start_time_str, '%I:%M %p').time() if start_time_str else None
        end_time = datetime.strptime(end_time_str, '%I:%M %p').time() if end_time_str else None
        date = datetime.strptime(date, '%Y-%m-%d').date() if date else None

        # Check for overlapping bookings
        query = Table.objects.filter(
            tablename=tablename,
            date=date
        ).filter(
            Q(start_timing__lt=end_time, end_time__gt=start_timing)
        ).exists()

        if query:
            message = "Table Already booked"
            return render(request, 'index.html', {"objects": objects, "form": form, "message": message, "message_class": "alert-danger"})
        else:
            if form.is_valid():
                form.save()
                message = "Your Table is successfully booked"
                return render(request, 'index.html', {"objects": objects, "form": form, "message": message, "message_class": "alert-success"})
            
        return render(request,'index.html',{"objects":objects,"form":form})


class bookingpageview(TemplateView):
    def get(self, request, *args, **kwargs):
        
        tables = Table.objects.all().order_by('-update_time')
        return render(request,'booking.html',{"tables":tables})

