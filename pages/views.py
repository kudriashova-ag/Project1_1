from django.shortcuts import render
from .forms import ContactForm

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
            
        else:
            
            return render(request, 'pages/contacts.html', {'form': form})
    
    form = ContactForm()
    return render(request, 'pages/contacts.html', {'form': form})
