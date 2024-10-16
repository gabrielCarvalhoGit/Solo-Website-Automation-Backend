from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login')
def solo_website(request):
    return render(request, 'solo/solo_website.html')