from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib import messages
from .models import Resume, Education, WorkExperience, Skill, Language, Hobby
from .forms import ResumeForm, EducationForm, WorkExperienceForm, SkillForm, LanguageForm, HobbyForm
from xhtml2pdf import pisa

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserCreationForm()
    return render(request, 'resume/signup.html', {'form': form})

@login_required
def dashboard(request):
    user_resumes = Resume.objects.filter(user=request.user)
    resume_form = ResumeForm()

    if request.method == 'POST' and 'save_resume' in request.POST:
        resume_form = ResumeForm(request.POST)
        if resume_form.is_valid():
            resume = resume_form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect('dashboard')

    return render(request, 'resume/dashboard.html', {
        'resume_form': resume_form,
        'user_resumes': user_resumes,
    })

@login_required
def create_resume(request):
    # Fetch the resumes associated with the logged-in user
    user_resumes = Resume.objects.filter(user=request.user)

    # Initialize all forms
    resume_form = ResumeForm()
    education_form = EducationForm()
    work_experience_form = WorkExperienceForm()
    skill_form = SkillForm()
    language_form = LanguageForm()
    hobby_form = HobbyForm()

    # Handle POST requests for each specific action
    if request.method == 'POST':
        if 'save_resume' in request.POST:
            resume_form = ResumeForm(request.POST)
            if resume_form.is_valid():
                resume = resume_form.save(commit=False)
                resume.user = request.user
                resume.save()
                return redirect('dashboard')

        elif 'add_education' in request.POST:
            education_form = EducationForm(request.POST)
            if education_form.is_valid():
                education = education_form.save(commit=False)
                education.resume = user_resumes.first()  # Assumes one resume per user
                education.save()
                return redirect('create_resume')

        elif 'add_work_experience' in request.POST:
            work_experience_form = WorkExperienceForm(request.POST)
            if work_experience_form.is_valid():
                work_experience = work_experience_form.save(commit=False)
                work_experience.resume = user_resumes.first()
                work_experience.save()
                return redirect('create_resume')

        elif 'add_skill' in request.POST:
            skill_form = SkillForm(request.POST)
            if skill_form.is_valid():
                skill = skill_form.save(commit=False)
                skill.resume = user_resumes.first()
                skill.save()
                return redirect('create_resume')

        elif 'add_language' in request.POST:
            language_form = LanguageForm(request.POST)
            if language_form.is_valid():
                language = language_form.save(commit=False)
                language.resume = user_resumes.first()
                language.save()
                return redirect('create_resume')

        elif 'add_hobby' in request.POST:
            hobby_form = HobbyForm(request.POST)
            if hobby_form.is_valid():
                hobby = hobby_form.save(commit=False)
                hobby.resume = user_resumes.first()
                hobby.save()
                return redirect('create_resume')

    # Context for rendering the template
    context = {
        'resume_form': resume_form,
        'education_form': education_form,
        'work_experience_form': work_experience_form,
        'skill_form': skill_form,
        'language_form': language_form,
        'hobby_form': hobby_form,
        'user_resumes': user_resumes,
    }
    return render(request, 'resume/create_resume.html', context)


@login_required
def view_resumes(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'resume/view_resumes.html', {'resumes': resumes})

@login_required
def resume_details(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    skills = resume.skills.all()
    languages = resume.languages.all()
    hobbies = resume.hobbies.all()
    return render(
        request, 
        'resume/resume_details.html', 
        {
            'resume': resume,
            'skills': skills,
            'languages': languages,
            'hobbies': hobbies
        }
    )


@login_required
def generate_pdf(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    education = Education.objects.filter(resume=resume)
    work_experience = WorkExperience.objects.filter(resume=resume)
    skills = Skill.objects.filter(resume=resume)
    hobbies = Hobby.objects.filter(resume=resume)
    languages = Language.objects.filter(resume=resume)

    html_content = render_to_string('resume/pdf_template.html', {
        'resume': resume,
        'education': education,
        'work_experience': work_experience,
        'skills': skills,
        'hobbies': hobbies,
        'languages': languages,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{resume.full_name}_Resume.pdf"'
    pisa_status = pisa.CreatePDF(html_content, dest=response)

    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)
    return response

def custom_logout(request):
    logout(request)
    return redirect('login')

@login_required
def edit_resume(request, resume_id):
    # Fetch the resume to be edited, associated with the logged-in user
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)

    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            messages.success(request, "Resume updated successfully!")
            # Redirect to the resume details page with the resume_id
            return redirect('resume_details', resume_id=resume.id)
    else:
        form = ResumeForm(instance=resume)

    return render(request, 'resume/edit_resume.html', {'form': form})
@login_required
def edit_item(request, item_id, model, form_class, template_name):
    item = get_object_or_404(model, id=item_id, resume__user=request.user)
    resume_id = item.resume.id
    if request.method == 'POST':
        form = form_class(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('resume_details', resume_id=resume_id)
    else:
        form = form_class(instance=item)
    return render(request, template_name, {'form': form})

@login_required
def delete_item(request, item_id, model):
    item = get_object_or_404(model, id=item_id, resume__in=Resume.objects.filter(user=request.user))
    item.delete()
    resume_id = item.resume.id
    return redirect('resume_details', resume_id=resume_id)

@login_required
def edit_education(request, education_id):
    return edit_item(request, education_id, Education, EducationForm, 'resume/edit_education.html')

@login_required
def delete_education(request, education_id):
    return delete_item(request, education_id, Education)

@login_required
def edit_work_experience(request, work_experience_id):
    return edit_item(request, work_experience_id, WorkExperience, WorkExperienceForm, 'resume/edit_work_experience.html')

@login_required
def delete_work_experience(request, work_experience_id):
    return delete_item(request, work_experience_id, WorkExperience)

@login_required
def edit_skill(request, skill_id):
    return edit_item(request, skill_id, Skill, SkillForm, 'resume/edit_skill.html')

@login_required
def delete_skill(request, skill_id):
    return delete_item(request, skill_id, Skill)

@login_required
def edit_hobby(request, hobby_id):
    return edit_item(request, hobby_id, Hobby, HobbyForm, 'resume/edit_hobby.html')

@login_required
def delete_hobby(request, hobby_id):
    return delete_item(request, hobby_id, Hobby)

@login_required
def edit_language(request, language_id):
    return edit_item(request, language_id, Language, LanguageForm, 'resume/edit_language.html')

@login_required
def delete_language(request, language_id):
    return delete_item(request, language_id, Language)












# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse
# from django.template.loader import render_to_string
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import logout
# from django.contrib import messages
# from .models import Resume, Education, WorkExperience, Skill, Language, Hobby
# from .forms import ResumeForm, EducationForm, WorkExperienceForm, SkillForm, LanguageForm, HobbyForm
# from xhtml2pdf import pisa

# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Account created successfully! Please log in.")
#             return redirect('login')  # Redirect to login after signup
#         else:
#             for error in form.errors.values():
#                 messages.error(request, error)
#     else:
#         form = UserCreationForm()  # Empty form for GET request
#     return render(request, 'resume/signup.html', {'form': form})

# @login_required
# def dashboard(request):
#     user_resumes = Resume.objects.filter(user=request.user)

#     resume_form = ResumeForm()
#     education_form = EducationForm()
#     work_experience_form = WorkExperienceForm()
#     skill_form = SkillForm()
#     language_form = LanguageForm()
#     hobby_form = HobbyForm()

#     if request.method == 'POST':
#         if 'save_resume' in request.POST:
#             resume_form = ResumeForm(request.POST)
#             if resume_form.is_valid():
#                 resume = resume_form.save(commit=False)
#                 resume.user = request.user
#                 resume.save()
#                 return redirect('dashboard')

#         elif 'add_education' in request.POST:
#             education_form = EducationForm(request.POST)
#             if education_form.is_valid():
#                 education = education_form.save(commit=False)
#                 education.resume = Resume.objects.get(user=request.user)  # Assumes a single resume per user
#                 education.save()
#                 return redirect('dashboard')

#         elif 'add_work_experience' in request.POST:
#             work_experience_form = WorkExperienceForm(request.POST)
#             if work_experience_form.is_valid():
#                 work_experience = work_experience_form.save(commit=False)
#                 work_experience.resume = Resume.objects.get(user=request.user)
#                 work_experience.save()
#                 return redirect('dashboard')

#         elif 'add_skill' in request.POST:
#             skill_form = SkillForm(request.POST)
#             if skill_form.is_valid():
#                 skill = skill_form.save(commit=False)
#                 skill.resume = Resume.objects.get(user=request.user)
#                 skill.save()
#                 return redirect('dashboard')

#         elif 'add_language' in request.POST:
#             language_form = LanguageForm(request.POST)
#             if language_form.is_valid():
#                 language = language_form.save(commit=False)
#                 language.resume = Resume.objects.get(user=request.user)
#                 language.save()
#                 return redirect('dashboard')

#         elif 'add_hobby' in request.POST:
#             hobby_form = HobbyForm(request.POST)
#             if hobby_form.is_valid():
#                 hobby = hobby_form.save(commit=False)
#                 hobby.resume = Resume.objects.get(user=request.user)
#                 hobby.save()
#                 return redirect('dashboard')

#     context = {
#         'resume_form': resume_form,
#         'education_form': education_form,
#         'work_experience_form': work_experience_form,
#         'skill_form': skill_form,
#         'language_form': language_form,
#         'hobby_form': hobby_form,
#         'user_resumes': user_resumes,
#     }
#     return render(request, 'resume/dashboard.html', context)

# @login_required
# def resume_view(request, resume_id):
#     # Fetch resume data for the logged-in user
#     resume = get_object_or_404(Resume, id=resume_id, user=request.user)
#     education = Education.objects.filter(resume=resume)
#     work_experience = WorkExperience.objects.filter(resume=resume)
#     skills = Skill.objects.filter(resume=resume)

#     return render(request, 'resume/resume.html', {
#         'resume': resume,
#         'education': education,
#         'work_experience': work_experience,
#         'skills': skills,
#     })

# @login_required
# def generate_pdf(request, resume_id):
#     resume = get_object_or_404(Resume, id=resume_id, user=request.user)
#     education = Education.objects.filter(resume=resume)
#     work_experience = WorkExperience.objects.filter(resume=resume)
#     skills = Skill.objects.filter(resume=resume)
#     hobbies = Hobby.objects.filter(resume=resume)
#     languages = Language.objects.filter(resume=resume)

#     html_content = render_to_string('resume/pdf_template.html', {
#         'resume': resume,
#         'education': education,
#         'work_experience': work_experience,
#         'skills': skills,
#         'hobbies': hobbies,
#         'languages': languages,
#     })

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="{resume.full_name}_Resume.pdf"'
#     pisa_status = pisa.CreatePDF(html_content, dest=response)

#     if pisa_status.err:
#         return HttpResponse("Error generating PDF", status=500)
#     return response

# def custom_logout(request):
#     logout(request)
#     return redirect('login')

# @login_required
# def edit_resume(request, resume_id):
#     resume = get_object_or_404(Resume, id=resume_id, user=request.user)
#     if request.method == 'POST':
#         form = ResumeForm(request.POST, instance=resume)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Resume updated successfully!")
#             return redirect('dashboard')
#     else:
#         form = ResumeForm(instance=resume)
#     return render(request, 'resume/edit_resume.html', {'form': form})


# # Reusable function for editing
# @login_required
# def edit_item(request, item_id, model, form_class, template_name, redirect_url='dashboard'):
#     item = get_object_or_404(model, id=item_id, resume__user=request.user)
#     if request.method == 'POST':
#         form = form_class(request.POST, instance=item)
#         if form.is_valid():
#             form.save()
#             return redirect(redirect_url)
#     else:
#         form = form_class(instance=item)
#     return render(request, template_name, {'form': form})

# # Reusable function for deleting
# @login_required
# def delete_item(request, item_id, model, redirect_url='dashboard'):
#     item = get_object_or_404(model, id=item_id,resume__in=Resume.objects.filter(user=request.user))
#     return redirect(redirect_url)

# # Edit and Delete Views


# @login_required
# def edit_education(request, education_id):
#     return edit_item(request, education_id, Education, EducationForm, 'resume/edit_education.html')

# @login_required
# def delete_education(request, education_id):
#     return delete_item(request, education_id, Education)

# @login_required
# def edit_work_experience(request, work_experience_id):
#     return edit_item(request, work_experience_id, WorkExperience, WorkExperienceForm, 'resume/edit_work_experience.html')

# @login_required
# def delete_work_experience(request, work_experience_id):
#     return delete_item(request, work_experience_id, WorkExperience)

# @login_required
# def edit_skill(request, skill_id):
#     return edit_item(request, skill_id, Skill, SkillForm, 'resume/edit_skill.html')

# @login_required
# def delete_skill(request, skill_id):
#     return delete_item(request, skill_id, Skill)

# @login_required
# def edit_hobby(request, hobby_id):
#     return edit_item(request, hobby_id, Hobby, HobbyForm, 'resume/edit_hobby.html')

# @login_required
# def delete_hobby(request, hobby_id):
#     return delete_item(request, hobby_id, Hobby)

# @login_required
# def edit_language(request, language_id):
#     return edit_item(request, language_id, Language, LanguageForm, 'resume/edit_language.html')

# @login_required
# def delete_language(request, language_id):
#     return delete_item(request, language_id, Language)
