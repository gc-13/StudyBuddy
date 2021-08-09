from django.contrib import admin
from .models import User, Course, StudyGroup, StudyRequest



class CourseInline(admin.TabularInline):
    model = Course.user_set.through
    extra = 1
    # fields = ['subject', 'catalog_number', 'class_title']
    # list_display = ('subject', 'catalog_number', 'class_title')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('subject', 'catalog_number', 'class_title')
    fieldsets = [
        (None, {'fields' : ['subject', 'catalog_number', 'class_title','instructor']})
    ]

class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    fieldsets = [
        ("Personal Information", {'fields': ['username', 'first_name', 'last_name', 'email']}),
        ("School Information", {'fields': ['major', 'description', 'courses']}),
        ("Staff", {'fields': ['is_superuser', 'is_staff', 'user_permissions']})
    ]
    inlines = [CourseInline]

class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'course')
    fieldsets = [
        (None, {"fields" : ['name', 'users, course'],}),
        ("Groupme Information" , {"fields" : ['groupme_id', 'groupme_shareurl']})
    ]

class StudyRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    fieldsets = [
        (None , {'fields': ['users', 'course', 'title', 'description', 'assignment']}),
        ('Group Information:', {'fields': ['current_size', 'sizeOfGroup']})
    ]

admin.site.register(User, UserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(StudyGroup, StudyGroupAdmin)
admin.site.register(StudyRequest, StudyRequestAdmin)
