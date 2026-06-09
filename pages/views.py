from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages

# Create your views here.
def contacts(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data.get('message')
            agree = form.cleaned_data['agree']
            
            print(name, email, message, agree)
            # flash message - видаляються після першого відображення
            
            messages.success(request, "Повідомлення успішно надіслано!")
            return redirect('contacts')  #  post-redirect-get pattern  PRG
        
        else:
            
            return render(request, 'pages/contacts.html', {'form': form})
    
    form = ContactForm()
    return render(request, 'pages/contacts.html', {'form': form})

