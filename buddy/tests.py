
from django.test import TestCase, Client
from django.contrib.auth.models import AbstractUser #maybe User
from buddy.models import User, Course, StudyGroup, StudyRequest
from buddy.views import update_size
from django.urls import reverse


# Create your tests here.
class TestCourseModel(TestCase):
    "tests to make sure all of the fields inputted into Course model are accurate"
    def test_subject_field(self):
        testCourse = Course(subject="CS", catalog_number="3240", class_title="advanced dev", instructor="sherriff")
        self.assertEqual(testCourse.subject,"CS")
    def test_instructor_field(self):
        testCourse = Course(subject="CS", catalog_number="3240", class_title="advanced dev", instructor="sherriff")
        self.assertEqual(testCourse.instructor,"sherriff")
    def test_catalog_field(self):
        testCourse = Course(subject="CS", catalog_number="3240", class_title="advanced dev", instructor="sherriff")
        self.assertEqual(testCourse.catalog_number,"3240")
    def test_class_title_field(self):
        testCourse = Course(subject="CS", catalog_number="3240", class_title="advanced dev", instructor="sherriff")
        self.assertEqual(testCourse.class_title,"advanced dev")

class TestUserModel(TestCase):
    "tests to make sure all of the fields inputted into User model are accurate"
    def test_many_to_many_field(self):
        
        TestUser = User( major ="computer science", description ="i need cs help!", id = 0)
        TestUser.save()
        course1 = TestUser.courses.create(subject = "CS", )
        course1.save()
        TestUser.courses.add(course1)


        self.assertEqual(TestUser.courses.all()[0], course1)
        self.assertEqual(course1.subject, "CS")

    def test_major_field(self):
        TestUser = User( major ="computer science", description ="i need cs help!", id = 0)
        TestUser.save()
        course1 = TestUser.courses.create(subject = "CS", )
        course1.save()
        TestUser.courses.add(course1)

        self.assertEqual(TestUser.major, "computer science")

    def test_description_field(self):
        TestUser = User( major ="computer science", description ="i need cs help!", id = 0)
        TestUser.save()
        course1 = TestUser.courses.create(subject = "CS", )
        course1.save()
        TestUser.courses.add(course1)

        self.assertEqual(TestUser.description, "i need cs help!")

def create_user(major, description, courses):
   return User.objects.create(major=major, description=description, course=courses)


class testMainFunction(TestCase):
    def test_add_course(self):
        """
        user's name shows up in response when account is already set up
        """
        TestUser = User( major ="computer science", description ="i need cs help!", id = 0)
        TestUser.save()
        course1 = TestUser.courses.create(subject = "CS", )
        course1.save()
        response = True
        self.assertEqual(response, True)

class testStudyRequestandStudyGroup(TestCase):

    def test_onestudygroupinrequestTrue(self):
        # pass
        TestUser = User( major ="computer science", description ="i need cs help!", id = 0)
        TestUser.save()
        course1 = TestUser.courses.create(subject = "CS", catalog_number="3240")
        course1.save()
        studyrequest = StudyRequest(course=course1, title="test", current_size=1,
                                    sizeOfGroup=3, hidden=False)
        studyrequest.save()
        studyrequest.users.add(TestUser)
        studyrequest.save()
        studygroup = StudyGroup(course=course1, studyrequest=studyrequest, name="test group", current_size=1,
                                sizeOfGroup=3, hidden=False)
        studygroup.save()
        studygroup.users.add(TestUser)
        studygroup.save()

        one_studygroup = len(studyrequest.studygroup_set.all()) == 1

        self.assertEqual(True, one_studygroup)

    def test_differentusersets(self):
        TestUser = User(username="testuser1", major ="computer science", description ="i need cs help!")
        TestUser.save()
        TestUser2 = User(username="testuser2", major ="computer science", description ="i need cs help!")
        TestUser2.save()
        course1 = TestUser.courses.create(subject = "CS", catalog_number="3240" )
        course1.save()
        studyrequest = StudyRequest(course=course1, title="test", current_size=1,
                                    sizeOfGroup=3, hidden=False)
        studyrequest.save()
        studyrequest.users.add(TestUser)
        studyrequest.save()
        studygroup = StudyGroup(course=course1, studyrequest=studyrequest, name="test group", current_size=1,
                                sizeOfGroup=3, hidden=False)
        studygroup.save()
        studygroup.users.add(TestUser)
        studygroup.users.add(TestUser2)
        studygroup.save()
        same_users = len(studygroup.users.all()) == len(studyrequest.users.all())
        for user in studygroup.users.all():
            if user not in studyrequest.users.all():
                same_users = False

        self.assertEqual(False, same_users)

    def test_sameusersinrequestandgroup(self):
        TestUser = User( major ="computer science", description ="i need cs help!", id = 0)
        TestUser.save()
        course1 = TestUser.courses.create(subject = "CS", )
        course1.save()
        studyrequest = StudyRequest(course=course1, title="test", current_size=1,
                                    sizeOfGroup=3, hidden=False)
        studyrequest.save()
        studyrequest.users.add(TestUser)
        studyrequest.save()
        studygroup = StudyGroup(course=course1, studyrequest=studyrequest, name="test group", current_size=1,
                                sizeOfGroup=3, hidden=False)
        studygroup.save()
        studygroup.users.add(TestUser)
        studygroup.save()
        same_users = len(studygroup.users.all()) == len(studyrequest.users.all())
        for user in studygroup.users.all():
            if user not in studyrequest.users.all():
                same_users = False

        self.assertTrue(same_users)

    def test_updatesize(self):
        TestUser = User(username="testuser1", major ="computer science", description ="i need cs help!")
        TestUser.save()
        TestUser2 = User(username="testuser2", major ="computer science", description ="i need cs help!")
        TestUser2.save()
        course1 = TestUser.courses.create(subject = "CS", catalog_number="3240" )
        course1.save()
        studyrequest = StudyRequest(course=course1, title="test", current_size=1,
                                    sizeOfGroup=3, hidden=False)
        studyrequest.save()
        studyrequest.users.add(TestUser)
        studyrequest.users.add(TestUser2)
        studyrequest.save()
        studygroup = StudyGroup(course=course1, studyrequest=studyrequest, name="test group", current_size=1,
                                sizeOfGroup=3, hidden=False)
        studygroup.save()
        studygroup.users.add(TestUser)
        studygroup.users.add(TestUser2)
        studygroup.save()
        update_size(studygroup, studyrequest)
        correct = len(studygroup.users.all()) == len(studyrequest.users.all()) and len(studygroup.users.all()) == studygroup.current_size
        for user in studygroup.users.all():
            if user not in studyrequest.users.all():
                correct = False

        self.assertEqual(True, correct)

