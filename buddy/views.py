from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django import forms
from .groupme_util import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, Row, Column


from django.conf import settings

from .models import User, Course, StudyGroup, StudyRequest


def index(request):
    course_data = Course.objects.all()
    context = {'course_data': course_data}
    return render(request, 'studybuddy/index.html', context)

def profile(request):

    return render(request, 'buddy/profile.html')


class StudyRequestsView(generic.ListView):
    model = StudyRequest
    context_object_name = 'studyrequest_list'
    queryset = StudyRequest.objects.all()
    template_name = 'buddy/requestSB.html'

                        
def courses(request):
    course_data = Course.objects.all()
    subjects = set()
    for course in Course.objects.all():
        subjects.add(course.subject)
    subjects = list(subjects)
    context = {'course_data': course_data, 'subject_list' : subjects}

    return render(request, 'buddy/courses.html', context)

def users(request):
    users_data = User.objects.all()
    context = {'users_data': users_data}
    return render(request, 'buddy/users.html', context)


def student(request, id):
    other_user = User.objects.get(id=id)
    return render(request, 'buddy/student.html', {"other_user":other_user})


class UserUpdate(UpdateView):
    model = User
    fields = ['major', 'year', 'description', 'first', 'second', 'third', 'image']
    template_name_suffix = '_update_form'

    def get_form(self, *args, **kwargs):
        form = super().get_form()
        form.helper = FormHelper()
        form.helper.layout = Layout(
            Row(Column('major', css_class='col-md-4'),
                Column('year', css_class='col-md-4')),
            Field('description', rows='3', css_class='input-xlarge col-md-6'),
            Row(Column('first', css_class='col-md-2'),
                Column('second', css_class='col-md-2'),
                Column('third', css_class='col-md-2')),
            Row(Column('image', css_class='col-md-8')),
            ButtonHolder(
                Submit('submit', 'Update Personal Information', css_class='button white')
                         )
        )
        return form

    def get_success_url(self):
        return reverse('profile')

class CourseChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{} {}".format(obj.subject, obj.catalog_number)

class StudyRequestForm(forms.ModelForm):

    class Meta:
        model = StudyRequest
        fields = ['title', 'description', 'assignment', 'sizeOfGroup', 'course']
        exclude = ['users']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column('title', css_class='col-md-6')),
            Field('description', rows='3', css_class='input-xlarge col-md-6'),
            Row( Column('assignment', css_class='col-md-2'),
                Column('sizeOfGroup', css_class='col-md-2'),
                Column('course', css_class='col-md-2')),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
                         )
        )

    title = forms.CharField()
    description = forms.CharField()
    assignment = forms.CharField()
    sizeOfGroup = forms.IntegerField()
    course = CourseChoiceField(label="Course?", queryset=Course.objects.all())


    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)
        form.instance.users.add(form.instance.user)
        return super().form_valid(form)


class StudyRequestCreate(LoginRequiredMixin, CreateView):
    template_name = "buddy/studyrequest_create_form.html"
    form_class = StudyRequestForm


    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)
        form.instance.users.add(form.instance.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('requestSB')

class StudyRequestCreate2(LoginRequiredMixin, CreateView):
    template_name = "buddy/studyrequest_create_form.html"
    form_class = StudyRequestForm


    def form_valid(self, form):
        form.instance.user = self.request.user
        super().form_valid(form)
        form.instance.users.add(form.instance.user)
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('profile')


def addcourse(request, pk):
    user = get_object_or_404(User, pk=pk)
    try:
        subject_param = request.POST['subject'].upper()
        selected_course = Course.objects.get(
            subject=subject_param,
            catalog_number=request.POST['catalog_number'])
    except (KeyError, Course.DoesNotExist):
        return render(request, 'buddy/profile.html',
                      {'courseadd_error_message' : "Sorry, that course doesn't exist"})
    else:
        if selected_course in user.courses.all():
            return render(request, 'buddy/profile.html',
                          {'courseadd_error_message': "Sorry, you're already in that course"})
        else:
            user.courses.add(selected_course)
            user.save()
            return HttpResponseRedirect(reverse('profile'))

def removecourse(request, pk):
    user = get_object_or_404(User, pk=pk)
    try:
        selected_course = Course.objects.get(pk=request.POST['course'])
    except (KeyError, Course.DoesNotExist):
        return render(request, 'buddy/profile.html',
                      {'courseremove_error_message' : "Sorry, that course doesn't exist"})
    else:
        user.courses.remove(selected_course)
        user.save()
        return HttpResponseRedirect(reverse('profile'))

class StudyGroupForm(forms.ModelForm):

    class Meta:
        model = StudyGroup
        fields = ['sizeOfGroup', 'course', 'name']


    name = forms.CharField()
    sizeOfGroup = forms.IntegerField()
    course = CourseChoiceField(label="Course?", queryset=Course.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column('name', css_class='col-md-6')),
            Row( Column('sizeOfGroup', css_class='col-md-2'),
                Column('course', css_class='col-md-2'),),
            ButtonHolder(
                Submit('submit', 'Update', css_class='button white')
                         )
        )

    def form_valid(self, form):
        if form.instance.current_size > form.instance.sizeOfGroup:
            return render('profile',
                          {'groupsize_error_message': "You can't make the max size of a group low than the number of current members"})
        else:
            studyrequest = form.instance.studyrequest
            studyrequest.sizeOfGroup = form.instance.sizeOfGroup
            studyrequest.save()
            super().form_valid(form)

class StudyGroupUpdate(UpdateView):
    model = StudyGroup
    template_name_suffix = '_update_form'
    form_class = StudyGroupForm

    def form_valid(self, form):
        if form.instance.current_size > form.instance.sizeOfGroup:
            return render(self.request, template_name='buddy/studygroup_update_form.html', context={'groupID' : form.instance.groupID,'groupsize_error_message': "You can't make the max size of a group lower than the number of current members"})
        else:
            studyrequest = form.instance.studyrequest
            studyrequest.sizeOfGroup = form.instance.sizeOfGroup
            studyrequest.save()
            return super().form_valid(form)

    def get_success_url(self):
        studygroup = self.get_object()
        return reverse('group', kwargs={"groupID": studygroup.groupID})

def groups(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_groups = StudyGroup.objects.filter(users__id=user.id)
    context = {'user_groups': user_groups}
    return render(request, 'buddy/groups.html', context)

def group(request, groupID):
    group = get_object_or_404(StudyGroup, pk=groupID)
    context = {'group': group}
    return render(request, 'buddy/group.html', context)

def createnewstudygroup(request, studyrequest_id, user_id):
    current_user = get_object_or_404(User, id=user_id)
    studyrequest= get_object_or_404(StudyRequest, id=studyrequest_id)
    course = get_object_or_404(Course, id=studyrequest.course.id)
    studyrequest.users.add(current_user)
    studyrequest.save()

    # If a StudyGroup already exists
    if len(studyrequest.studygroup_set.all()) == 1:
        studygroup = studyrequest.studygroup_set.all()[0]
        studygroup.users.add(current_user)
        studygroup.current_size += 1
        studygroup.save()
        studyrequest.current_size += 1
        studyrequest.save()

    # If a StudyGroup has not yet been created
    else:
        groupme_name, groupme_id, groupme_shareurl = creategroupme(studyrequest.title)
        studygroup = StudyGroup(name=groupme_name, course=course, groupme_id=groupme_id, groupme_shareurl=groupme_shareurl, studyrequest=studyrequest)
        studygroup.save()
        for user in studyrequest.users.all():
            studygroup.users.add(user)
        studygroup.users.add(current_user)
        studyrequest.studygroup_id = studygroup.groupID
        studyrequest.current_size += 1
        studygroup.current_size = studyrequest.current_size
        studygroup.sizeOfGroup = studyrequest.sizeOfGroup
        studygroup.save()
        studyrequest.save()


    return HttpResponseRedirect(reverse('requestSB'))

def leavegroup(request, groupID, user_id):
    user = get_object_or_404(User, id=user_id)
    studygroup = get_object_or_404(StudyGroup, groupID=groupID)

    studyrequest = studygroup.studyrequest
    studygroup.users.remove(user)
    studyrequest.users.remove(user)
    update_size(studygroup, studyrequest)


    user_groups = StudyGroup.objects.filter(users__id=user.id)
    context = {'user_groups': user_groups}
    return render(request, 'buddy/groups.html', context)


def changehiddenstatus(request, groupID, status):
    studygroup = get_object_or_404(StudyGroup, groupID=groupID)
    studyrequest = studygroup.studyrequest
    if status == 1:
        status = True
    else:
        status = False
    studygroup.hidden = status
    studyrequest.hidden = status
    studygroup.save()
    studyrequest.save()

    context = {'group': studygroup}
    return render(request, 'buddy/group.html', context)

def course(request, id):
    course = get_object_or_404(Course, pk=id)
    context = {'course': course}
    return render(request, 'buddy/course.html', context)

def update_size(studygroup, studyrequest):
    studygroup.current_size = len(studygroup.users.all())
    studyrequest.current_size = len(studygroup.users.all())
    studygroup.save()
    studyrequest.save()





                        