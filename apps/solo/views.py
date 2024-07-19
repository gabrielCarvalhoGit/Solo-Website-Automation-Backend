from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def solo_website(request):
    context = {
        'is_superuser': request.user.is_superuser,
    }
    return render(request, 'solo/solo_website.html', context)