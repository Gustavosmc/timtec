# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from accounts.views import CustomLoginView, ProfileEditView, RegistrationUniqueEmailView, ProfileView
from core.views import AdminCourseView, CourseView, CourseViewSet, EnrollCourseView, HomeView, UserCoursesView
from lesson.views import LessonDetailView, LessonViewSet, StudentProgressViewSet, ReceiveAnswerView
from forum.views import CourseForumView, QuestionView, QuestionCreateView, QuestionViewSet, AnswerViewSet, QuestionVoteViewSet, AnswerVoteViewSet
from course_material.views import CourseMaterialView, FileUploadView
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'course', CourseViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'student_progress', StudentProgressViewSet)
router.register(r'forum_question', QuestionViewSet)
router.register(r'forum_answer', AnswerViewSet)
router.register(r'question_vote', QuestionVoteViewSet)
router.register(r'answer_vote', AnswerVoteViewSet)


urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='home_view'),

    # Uncomment the next line to enable the admin:
    url(r'^django/admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^django/admin/', include(admin.site.urls)),

    # Privileged browsing
    url(r'^admin/course/(?P<slug>[-a-zA-Z0-9_]+)$', AdminCourseView.as_view(), name='course_intro'),

    # Public browsing
    url(r'^my-courses$', UserCoursesView.as_view(), name='user_courses'),
    url(r'^course/(?P<slug>[-a-zA-Z0-9_]+)$', CourseView.as_view(), name='course_intro'),
    url(r'^course/(?P<slug>[-a-zA-Z0-9_]+)/enroll$', EnrollCourseView.as_view(), name='enroll_course'),
    url(r'^lesson/(?P<slug>[-a-zA-Z0-9_]+)$', LessonDetailView.as_view(), name='lesson'),

    # Services
    url(r'^api/', include(router.urls)),
    url(r'^api/answer/(?P<unitId>[0-9]*)$', ReceiveAnswerView.as_view(), name='answer'),

    # Forum
    url(r'^forum/(?P<course_slug>[-a-zA-Z0-9_]+)$', CourseForumView.as_view(), name='forum'),
    url(r'^forum/question/(?P<slug>[-a-zA-Z0-9_]+)$', QuestionView.as_view(), name='forum_question'),
    url(r'^forum/question/add/(?P<course_slug>[-a-zA-Z0-9_]+)$', QuestionCreateView.as_view(), name='forum_question_create'),

    # Course Material
    url(r'^course_material/file_upload/(?P<slug>[-a-zA-Z0-9_]+)$', FileUploadView.as_view(), name='file_upload'),
    url(r'^course_material/(?P<slug>[-a-zA-Z0-9_]+)$', CourseMaterialView.as_view(), name='course_material'),

    # Authentication
    url(r'^login/', CustomLoginView.as_view(), name='timtec_login'),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='timtec_logout'),

    url(r'^profile/edit/?$', ProfileEditView.as_view(), name="profile_edit"),
    url(r'^profile/(?P<username>[-a-zA-Z0-9_]+)?$', ProfileView.as_view(), name="profile"),

    # The django-registration
    url(r'^accounts/register/$', RegistrationUniqueEmailView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),

    # The django-rosetta
    url(r'^rosetta/', include('rosetta.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
