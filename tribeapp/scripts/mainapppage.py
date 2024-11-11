from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from tribeapp.models import Table
from tribeapp.forms import TableForm,BookingForm
from datetime import date, datetime
from django.db.models import Q
import csv
import io
from pprint import pprint

class MainPageView(TemplateView):
    def get(self, request, *args, **kwargs):
        form = TableForm()
        tables = Table.objects.all()
        return render(request,'index.html',{"tables":tables,"form":form})
    def post(self, request):
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
        start_timing_24 = datetime.strptime(start_time_str, '%I:%M %p').time() if start_time_str else None
        end_time_24 = datetime.strptime(end_time_str, '%I:%M %p').time() if end_time_str else None

        print(start_timing_24,'==========',end_time_24)

        date = datetime.strptime(date, '%Y-%m-%d').date() if date else None

        # Check for overlapping bookings
        query = Table.objects.filter(
            tablename=tablename,
            date=date
        ).filter(
            Q(start_timing__lt=end_time_24, end_time__gt=start_timing_24)
        ).exists()

        if query:
            message = "Table Already booked"
            return render(request, 'index.html', {"objects": objects, "form": form, "message": message, "message_class": "alert-danger"})
        else:
            if form.is_valid():
                # Set the 24-hour formatted times in the form's cleaned_data
                table_instance = form.save(commit=False)
                table_instance.start_timing = start_timing_24
                table_instance.end_time = end_time_24
                table_instance.date = date
                
                # Save the instance to the database
                table_instance.save()
                message = "Your Table is successfully booked"
                return render(request, 'index.html', {"objects": objects, "form": form, "message": message, "message_class": "alert-success"})
            
        return render(request,'index.html',{"objects":objects,"form":form})



class bookingpageview(TemplateView):
    def get(self, request, *args, **kwargs):
        
        tables = Table.objects.all().order_by('-update_time')
        return render(request,'booking.html',{"tables":tables})
    

class export_data(TemplateView):
    def get(self,request,*args,**kwargs):
        form = BookingForm()
        return render(request,'export_data.html',{'form':form})

    def post(self, request, *args, **kwargs):
        form = BookingForm(request.POST)
        
        if form.is_valid():
            table = form.cleaned_data.get("table")
            start_date = form.cleaned_data.get("start_date")
            end_date = form.cleaned_data.get("end_date")
            print("Cleaned Data:", table, start_date, end_date)
            print("Cleaned Data:", type(table), type(start_date), end_date)
            if table == 'None' and end_date != None:
                print("111111111111111111111")
                return self.get_st_ed(request, start_date, end_date)
            
            
            elif table == 'None' and end_date == None:
                print("22222222222222")
                return self.get_st(request, start_date)
                
            else:
                print("3333333333333333")
                return self.get_st_ed_table(request,table,start_date, end_date)
        else:
            print("Form Errors:", form.errors)

        
        print("------------------------")
        return render(request, 'export_data.html', {'form': form})
    
    def get_st(self,request, start_date):
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = date.today().strftime("%Y-%m-%d") 

        query = Table.objects.filter(Q(date__lte=end_date_str, date__gte=start_date_str)).values()
        
        # Process query and add final_amount column
        query_list = [
            {
                **{key: value for key, value in record.items() if key not in ['id', 'created_time', 'update_time']},
                'final_amount': record['amount'] + record['extra_allowances']
            }
            for record in query
        ]
        
        # Create an in-memory CSV file
        csv_file_name = f"{start_date_str}_to_{end_date_str}.csv"
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{csv_file_name}"'
        
        # Write to the in-memory file
        csv_buffer = io.StringIO()
        if query_list:
            writer = csv.DictWriter(csv_buffer, fieldnames=query_list[0].keys())
            writer.writeheader()
            writer.writerows(query_list)
        
        response.write(csv_buffer.getvalue())
        csv_buffer.close()
        
        print(f"CSV file '{csv_file_name}' prepared for download.")
        return response
    
    def get_st_ed(self, request, start_date, end_date):
        print("get_st_ed", start_date, end_date)
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        
        # Filter query for records within the date range
        query = Table.objects.filter(Q(date__lte=end_date_str, date__gte=start_date_str)).values()
        
        # Process query and add final_amount column
        query_list = [
            {
                **{key: value for key, value in record.items() if key not in ['id', 'created_time', 'update_time']},
                'final_amount': record['amount'] + record['extra_allowances']
            }
            for record in query
        ]
        
        # Create an in-memory CSV file
        csv_file_name = f"{start_date_str}_to_{end_date_str}.csv"
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{csv_file_name}"'
        
        # Write to the in-memory file
        csv_buffer = io.StringIO()
        if query_list:
            writer = csv.DictWriter(csv_buffer, fieldnames=query_list[0].keys())
            writer.writeheader()
            writer.writerows(query_list)
        
        response.write(csv_buffer.getvalue())
        csv_buffer.close()
        
        print(f"CSV file '{csv_file_name}' prepared for download.")
        return response
    
    def get_st_ed_table(self,request,table, start_date, end_date):
        print("get_st_ed_table",table, start_date, end_date)
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        
        # Filter query for records within the date range
        query = Table.objects.filter(Q(date__lte=end_date_str, date__gte=start_date_str)).values()

        query = Table.objects.filter(tablename=table).filter(Q(date__lte=end_date_str, date__gte=start_date_str)).values()
        
        query_list = [
            {key: value for key, value in record.items() if key not in ['id', 'created_time', 'update_time']}
            for record in query
        ]

        pprint(query_list)
        
        # Create an in-memory CSV file
        csv_file_name = f"{table}-{start_date_str}_to_{end_date_str}.csv"
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{csv_file_name}"'
        
        # Write to the in-memory file
        csv_buffer = io.StringIO()
        if query_list:
            writer = csv.DictWriter(csv_buffer, fieldnames=query_list[0].keys())
            writer.writeheader()
            writer.writerows(query_list)
        
        # Set CSV buffer content to the response
        response.write(csv_buffer.getvalue())
        csv_buffer.close()
        
        print(f"CSV file '{csv_file_name}' prepared for download.")
        return response

