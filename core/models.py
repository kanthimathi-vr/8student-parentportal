from django.db import models
from django.utils import timezone

# 1. Course/Subject Model
class Subject(models.Model):
    """Represents a course or subject taught in the school (e.g., Math, Science)."""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Subjects (Courses)"

# 2. Teacher Model (Class Teacher)
class Teacher(models.Model):
    """Represents a Class Teacher who is linked to a group of students."""
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"Teacher: {self.name} ({self.employee_id})"

# 3. Student Model
class Student(models.Model):
    """Represents a student, linked to a single Class Teacher."""
    name = models.CharField(max_length=100)
    roll_number = models.IntegerField(unique=True)
    
    # 1:N Relationship (One Teacher can have many Students)
    class_teacher = models.ForeignKey(
        Teacher, 
        on_delete=models.SET_NULL, # If teacher is deleted, students remain but are unassigned.
        null=True, 
        blank=True,
        related_name='students'
    )
    
    # For simulating Parent Login (Parent Email)
    parent_name = models.CharField(max_length=100, blank=True, default='N/A')
    parent_email = models.EmailField(unique=True, blank=True, null=True)

    def __str__(self):
        return f"Student: {self.name} (Roll: {self.roll_number})"

# 4. Mark Entry Model
class Mark(models.Model):
    """
    Manages marks for a student in a specific subject. 
    This is the core 'Marks entry' component.
    """
    EXAM_CHOICES = [
        ('midterm', 'Midterm Exam'),
        ('final', 'Final Exam'),
        ('quiz', 'Quiz'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    
    exam_type = models.CharField(max_length=50, choices=EXAM_CHOICES, default='midterm')
    score = models.IntegerField() # The mark out of 100
    date_recorded = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.student.name}'s {self.score} in {self.subject.name} ({self.get_exam_type_display()})"
    
    class Meta:
        unique_together = ('student', 'subject', 'exam_type') # Ensure a student only gets one mark per subject per exam type
        ordering = ['student__name', 'subject__name']

# 5. Simple Attendance Model
class AttendanceRecord(models.Model):
    """Simple model for tracking daily attendance."""
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    
    def __str__(self):
        return f"{self.student.name} - {self.date}: {self.get_status_display()}"
    
    class Meta:
        unique_together = ('student', 'date')
        ordering = ['date', 'student__name']