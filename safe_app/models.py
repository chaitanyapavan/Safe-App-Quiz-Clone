from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Course(models.Model):
	instructor = models.ForeignKey(User, on_delete=models.CASCADE)
	course_code = models.CharField(max_length=200, default='')

class Quiz(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	quiz_code = models.CharField(max_length=200, default='')
	number_of_questions = models.IntegerField(default=0)
	status = models.CharField(max_length=10,default='')

class Blank(models.Model):
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	text = models.CharField(max_length=1000,default='')
	question_number = models.IntegerField(default=0)  ## Position of question in quiz

class TrueFalse(models.Model):
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	text = models.CharField(max_length=1000,default='')
	question_number = models.IntegerField(default=0)

class MultipleChoice(models.Model):
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	text = models.CharField(max_length=1000,default='')
	option1 = models.CharField(max_length=500, default='')
	option2 = models.CharField(max_length=500, default='')
	option3 = models.CharField(max_length=500, default='')
	option4 = models.CharField(max_length=500, default='')
	question_number = models.IntegerField(default=0)

class Student(models.Model):
	loginId = models.CharField(max_length=200, default='')
	password = models.CharField(max_length=200, default='')
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)


