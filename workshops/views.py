from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Workshop, Registration

def workshop_list(request):
    # Get all upcoming workshops
    upcoming_workshops = Workshop.objects.filter(
        start_time__gte=timezone.now()
    ).order_by('start_time')
    
    context = {
        'workshops': upcoming_workshops,
    }
    return render(request, 'workshops/workshop_list.html', context)

def workshop_detail(request, pk):
    workshop = get_object_or_404(Workshop, pk=pk)
    
    # Check if user has registered any children for this workshop
    user_registrations = []
    if request.user.is_authenticated:
        user_registrations = Registration.objects.filter(
            workshop=workshop,
            parent=request.user
        )
    
    context = {
        'workshop': workshop,
        'user_registrations': user_registrations,
    }
    return render(request, 'workshops/workshop_detail.html', context)
