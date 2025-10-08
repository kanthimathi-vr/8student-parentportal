from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Student, Mark, AttendanceRecord
from django.db.models import Prefetch

def home_view(request):
    """
    Landing page with a simple form for parent email submission.
    """
    if request.method == 'POST':
        # Get the email from the submitted form data
        parent_email = request.POST.get('parent_email', '').strip()
        if parent_email:
            # Redirect to the specific parent dashboard URL
            return redirect(reverse('parent_dashboard', args=[parent_email]))
        
    return render(request, 'core/home.html')

def parent_dashboard_view(request, parent_email):
    """
    Simulates the parent dashboard view.
    It fetches a student, their marks, and attendance using the parent's email.
    """
    # Defensive check against empty/None email
    if not parent_email:
        # Redirect to home if the email is missing
        return redirect('home')
        
    try:
        # Fetch the student linked to this parent email (case-insensitive)
        student = Student.objects.get(parent_email__iexact=parent_email)
    except Student.DoesNotExist:
        # If no student is found, display an error message
        context = {
            'error_message': f"No student found linked to the email: {parent_email}. Please check the email address.",
            'parent_email_attempted': parent_email
        }
        return render(request, 'core/parent_dashboard.html', context)


    # Fetch all marks for the student
    marks = Mark.objects.filter(student=student).order_by('subject__name', 'date_recorded')

    # Fetch attendance records for the last 30 days
    from datetime import date, timedelta
    thirty_days_ago = date.today() - timedelta(days=30)
    
    attendance_records = AttendanceRecord.objects.filter(
        student=student,
        date__gte=thirty_days_ago
    ).order_by('-date')

    context = {
        'student': student,
        'marks': marks,
        'attendance_records': attendance_records,
        'parent_email': parent_email,
    }
    
    return render(request, 'core/parent_dashboard.html', context)

