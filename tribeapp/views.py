
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import Table
from django.contrib.auth import logout

# Create your views here.

def website_page(request):
    return render(request, 'website.html')

# def home(request):
#     return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('/bookingpageview')  
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})

    form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': True})
                return redirect('/index')  # Adjust as necessary
            else:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'errors': {'non_field_errors': ['Invalid username or password.']}})
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})

    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@csrf_exempt
def destroyevent(request, module_id):
    module = Table.objects.get(id=module_id)
    module.delete()
    print("-----------------done-----------")
    return HttpResponse()


# @csrf_exempt
def add_amount(request):
    if request.method == 'POST':
        table_id = request.POST.get('id')
        add_amount = int(request.POST.get('add_amount', 0))
        table = get_object_or_404(Table, id=table_id)
        
        # Update the amount
        table.extra_allowances += add_amount
        table.save()
        
        return JsonResponse({'success': True, 'new_amount': table.amount,'table_id':table_id})
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def logout_view(request):
    logout(request)
    return redirect('index')

