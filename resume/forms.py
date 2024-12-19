from django import forms
from .models import Resume, Education, WorkExperience, Skill, Language, Hobby
from django.forms.widgets import DateInput


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['full_name', 'email', 'phone', 'address']

class EducationForm(forms.ModelForm):
    start_date = forms.DateField(widget=DateInput(attrs={'type': 'date', 'format': 'dd-mm-yyyy'}))
    end_date = forms.DateField(widget=DateInput(attrs={'type': 'date', 'format': 'dd-mm-yyyy'}))

    class Meta:
        model = Education
        fields = ['degree', 'institution', 'start_date', 'end_date', 'description']

class WorkExperienceForm(forms.ModelForm):
    start_date = forms.DateField(widget=DateInput(attrs={'type': 'date', 'format': 'dd-mm-yyyy'}))
    end_date = forms.DateField(widget=DateInput(attrs={'type': 'date', 'format': 'dd-mm-yyyy'}))

    class Meta:
        model = WorkExperience
        fields = ['job_title', 'company', 'start_date', 'end_date', 'description']

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill_name', 'proficiency']

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ['language_name', 'proficiency']


class HobbyForm(forms.ModelForm):
    class Meta:
        model = Hobby
        fields = ['hobby_name']

