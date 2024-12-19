from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication routes
    path('', auth_views.LoginView.as_view(template_name='resume/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('signup/', views.signup, name='signup'),

    # Dashboard and Resume routes
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-resume/', views.create_resume, name='create_resume'),
    path('view-resumes/', views.view_resumes, name='view_resumes'),
    path('resume/<int:resume_id>/details/', views.resume_details, name='resume_details'),
    path('resume/<int:resume_id>/pdf/', views.generate_pdf, name='download_pdf'),
    path('edit-resume/<int:resume_id>/', views.edit_resume, name='edit_resume'),

   
    path('education/<int:education_id>/edit/', views.edit_education, name='edit_education'),
    path('education/<int:education_id>/delete/', views.delete_education, name='delete_education'),

  
    path('work-experience/<int:work_experience_id>/edit/', views.edit_work_experience, name='edit_work_experience'),
    path('work-experience/<int:work_experience_id>/delete/', views.delete_work_experience, name='delete_work_experience'),

    
    path('edit-skill/<int:skill_id>/', views.edit_skill, name='edit_skill'),
    path('delete-skill/<int:skill_id>/', views.delete_skill, name='delete_skill'),

   
    path('hobby/<int:hobby_id>/edit/', views.edit_hobby, name='edit_hobby'),
    path('hobby/<int:hobby_id>/delete/', views.delete_hobby, name='delete_hobby'),

     
    path('language/<int:language_id>/edit/', views.edit_language, name='edit_language'),
    path('language/<int:language_id>/delete/', views.delete_language, name='delete_language'),
]










# from django.urls import path
# from django.contrib.auth import views as auth_views
# from . import views

# urlpatterns = [
#     path('', auth_views.LoginView.as_view(template_name='resume/login.html'), name='login'),
#     path('logout/', views.custom_logout, name='logout'),
#     path('signup/', views.signup, name='signup'),
#     path('dashboard/', views.dashboard, name='dashboard'),
#     path('resume/<int:resume_id>/', views.resume_view, name='resume_view'),
#     path('resume/<int:resume_id>/pdf/', views.generate_pdf, name='download_pdf'),
#     path('edit-resume/<int:resume_id>/', views.edit_resume, name='edit_resume'),
    

#     path('education/<int:education_id>/edit/', views.edit_education, name='edit_education'),
#     path('education/<int:education_id>/delete/', views.delete_education, name='delete_education'),

#     path('work-experience/<int:work_experience_id>/edit/', views.edit_work_experience, name='edit_work_experience'),
#     path('work-experience/<int:work_experience_id>/delete/', views.delete_work_experience, name='delete_work_experience'),

#     path('edit-skill/<int:skill_id>/', views.edit_skill, name='edit_skill'),
#     path('delete-skill/<int:skill_id>/', views.delete_skill, name='delete_skill'),

#     path('hobby/<int:hobby_id>/edit/', views.edit_hobby, name='edit_hobby'),
#     path('hobby/<int:hobby_id>/delete/', views.delete_hobby, name='delete_hobby'),

#     path('language/<int:language_id>/edit/', views.edit_language, name='edit_language'),
#     path('language/<int:language_id>/delete/', views.delete_language, name='delete_language'),
# ]
