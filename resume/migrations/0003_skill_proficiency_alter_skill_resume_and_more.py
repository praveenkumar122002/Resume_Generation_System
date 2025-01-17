# Generated by Django 5.1.3 on 2024-12-09 14:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0002_rename_skills_resume_address_remove_resume_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='proficiency',
            field=models.CharField(choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], default='Beginner', max_length=50),
        ),
        migrations.AlterField(
            model_name='skill',
            name='resume',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='resume.resume'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='skill_name',
            field=models.CharField(max_length=200),
        ),
    ]
