from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)  
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()  # Replaces summary
    # github_link = models.URLField(blank=True, null=True)
    # skills = models.TextField()  # Keep this for summary-style skills

class Education(models.Model):
    resume = models.ForeignKey(Resume, related_name='education', on_delete=models.CASCADE)
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True) 

class WorkExperience(models.Model):
    resume = models.ForeignKey(Resume, related_name='work_experience', on_delete=models.CASCADE)
    job_title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True) 

class Skill(models.Model):
    resume = models.ForeignKey(Resume, related_name='skills', on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=200)
    proficiency = models.CharField(
        max_length=50,
        choices=[('fluent', 'Fluent'), ('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')],
        default='Beginner'  # Set a default value here
    )

    def __str__(self):
        return self.skill_name
    
class Language(models.Model):
    resume = models.ForeignKey(Resume, related_name='languages', on_delete=models.CASCADE)
    language_name = models.CharField(max_length=100)
    proficiency = models.CharField(
        max_length=50,
        choices=[('fluent', 'Fluent'), ('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')],
        default='Beginner'
    )

    def __str__(self):
        return f"{self.language_name} ({self.proficiency})"
    
class Hobby(models.Model):
    resume = models.ForeignKey(Resume, related_name='hobbies', on_delete=models.CASCADE)
    hobby_name = models.CharField(max_length=200)

    def __str__(self):
        return self.hobby_name



