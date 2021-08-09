from django.db import models
from django import forms
from django.core.exceptions import ValidationError
import requests, json
import uuid
# Create your models here.

from django.contrib.auth.models import AbstractUser


class Course(models.Model):
    subject = models.CharField(max_length=4, verbose_name="Subject")
    catalog_number = models.CharField(max_length=4, verbose_name="Catalog Number")
    class_title = models.CharField(max_length=100, verbose_name="Class Title")
    instructor = models.CharField(max_length=40)


   
class User(AbstractUser):
    MAJOR_CHOICES = (("AE", "Aerospace Engineering"), ("BME", "Biomedical Engineering"), ("CE", "Civil Engineering"), ("CPE", "Computer Engineering"), ("CS", "Computer Science"), ("EE", "Electrical Engineering"), ("ES", "Engineering Science"), ("ME", "Mechanical Engineering"), ("MSE", "Materials Science and Engineering"), ("SE", "Systems Engineering"))
    YEAR_CHOICES = (("1", "First"), ("2", "Second"), ("3", "Third"), ("4", "Fourth"))
    major = models.CharField(max_length=60, choices=MAJOR_CHOICES, blank=True)
    description = models.CharField(max_length=140, blank=True)
    year = models.CharField(max_length=10, choices=YEAR_CHOICES, blank=True)
    courses = models.ManyToManyField(Course)
    first = models.CharField(max_length=100, blank=True, verbose_name="Study Buddy Trait 1")
    second = models.CharField(max_length=100, blank=True, verbose_name="Study Buddy Trait 2")
    third = models.CharField(max_length=100, blank=True, verbose_name="Study Buddy Trait 3")
    image = models.ImageField(upload_to='profile_image', blank=True)


DEFAULT_COURSE_ID = 20485
class StudyRequest(models.Model):
    users = models.ManyToManyField(User)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default = DEFAULT_COURSE_ID)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    assignment = models.CharField(max_length=140, blank=True)
    current_size = models.PositiveIntegerField(default=1, verbose_name="Current Size")
    sizeOfGroup = models.PositiveIntegerField(verbose_name="Max Size of Group")
    accepted = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)

class StudyGroup(models.Model):
    groupID = models.AutoField(primary_key = True)
    studyrequest = models.ForeignKey(StudyRequest, on_delete=models.CASCADE, verbose_name="Study Request")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default = DEFAULT_COURSE_ID)
    users = models.ManyToManyField(User)
    name = models.CharField(max_length = 100)
    groupme_id = models.PositiveIntegerField(blank=True, default=0)
    groupme_shareurl = models.URLField(blank=True, default="")
    current_size = models.PositiveIntegerField(default=2, verbose_name="Current Size")
    sizeOfGroup = models.PositiveIntegerField(default=2, verbose_name="Max Size of Group")
    hidden = models.BooleanField(default=False)




