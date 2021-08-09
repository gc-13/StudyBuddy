from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('profile/studyrequestform', views.StudyRequestCreate2.as_view(), name='studyrequestform2'),
    path('requestSB/', views.StudyRequestsView.as_view(), name='requestSB'),
    path('courses/', views.courses, name='courses'),
    path('profile/addcourse/<int:user_id>/', views.addcourse, name='addcourse'),
    path('editprofile/<int:pk>/', views.UserUpdate.as_view(), name='editprofile'),
    path('editprofile/<int:pk>/addcourse/', views.addcourse, name='addcourse'),
    path('editprofile/<int:pk>/removecourse/', views.removecourse, name='removecourse'),
    path('users/', views.users, name='users'),
    path('student/<int:id>', views.student, name='student'),
    path('groups/<int:pk>/', views.groups, name='groups'),
    path('group-<int:groupID>/', views.group, name='group'),
    path('requestSB/studyrequestform', views.StudyRequestCreate.as_view(), name='studyrequestform'),
    path('requestSB/createstudygroup/<int:studyrequest_id>/<int:user_id>', views.createnewstudygroup, name='createnewstudygroup'),
    path('group-<int:groupID>/leavegroup/<int:user_id>', views.leavegroup, name="leavegroup"),
    path('group-<int:pk>/editgroup', views.StudyGroupUpdate.as_view(), name='studygroupupdate'),
    path('group-<int:groupID>/changehiddenstatus/<int:status>', views.changehiddenstatus, name='changehiddenstatus'),
    path('courses/<int:id>', views.course, name='course'),
]
