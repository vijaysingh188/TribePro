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
    def post(self,request):
        objects = Table.objects.all()
        form = TableForm(request.POST)
        tablename = request.POST.get('tablename')
        start_timing = request.POST.get('start_timing')
        end_time = request.POST.get('end_time')
        date = request.POST.get('date')
        print(tablename,start_timing,end_time,date)
        
        
        start_timing = datetime.strptime(start_timing, '%H:%M').time() if start_timing else None
        end_time = datetime.strptime(end_time, '%H:%M').time() if end_time else None
        date = datetime.strptime(date, '%Y-%m-%d').date() if date else None
        print(tablename,start_timing,end_time,date)
        query = Table.objects.filter(
            tablename=tablename,
            date=date
            ).filter(
                Q(start_timing__lt=end_time) & Q(end_time__gt=start_timing)
            ).values()
        if query:
            message = "Table Already booked"
            return render(request,'index.html',{"objects":objects,"form":form,"message": message})
        else:
            if form.is_valid():
                form.save()
                return redirect('bookingpageview')
        
        

        return render(request,'index.html',{"objects":objects,"form":form})

class bookingpageview(TemplateView):
    def get(self, request, *args, **kwargs):
        
        tables = Table.objects.all().order_by('-update_time')
        return render(request,'booking.html',{"tables":tables})

