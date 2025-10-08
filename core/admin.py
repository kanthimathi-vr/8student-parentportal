from django.contrib import admin
from .models import Subject, Teacher, Student, Mark, AttendanceRecord

# Custom Inline for Marks (to view/edit marks directly from the Student page)
class MarkInline(admin.TabularInline):
    model = Mark
    extra = 5 # Pre-populate 5 extra slots for easy marks entry
    fields = ('subject', 'exam_type', 'score', 'date_recorded')

# Custom Inline for Attendance
class AttendanceInline(admin.TabularInline):
    model = AttendanceRecord
    extra = 1
    fields = ('date', 'status')


# Customize Student Model Admin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_number', 'class_teacher', 'parent_email')
    list_filter = ('class_teacher',)
    search_fields = ('name', 'roll_number', 'parent_email')
    
    # Include Marks and Attendance inlines on the student page
    inlines = [MarkInline, AttendanceInline]
    
    fieldsets = (
        (None, {
            'fields': ('name', 'roll_number', 'class_teacher')
        }),
        ('Parent Information', {
            'fields': ('parent_name', 'parent_email'),
            'description': 'Details needed for parent access/communication.'
        }),
    )

# Customize Teacher Model Admin
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee_id', 'email')
    search_fields = ('name', 'employee_id')
    
    # Show students supervised by the teacher
    # Note: Students are accessible via the 'students' related_name on the Teacher model instance

# Register the remaining models
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'exam_type', 'score', 'date_recorded')
    list_filter = ('exam_type', 'subject')
    search_fields = ('student__name', 'subject__name')
    date_hierarchy = 'date_recorded'

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('student__name',)
