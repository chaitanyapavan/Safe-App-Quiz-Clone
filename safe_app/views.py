from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
import openpyxl, xlrd
from pyexcel_ods import get_data

# Create your views here.
from .models import Course, Quiz, Blank, TrueFalse, MultipleChoice, Student

def welcome(request):
	return render(request, 'safe_app/welcome.html', {'show':False})

def course(request):
	loginId = request.POST['loginId']
	password = request.POST['password']
	user = authenticate(request, username=loginId, password=password)
	if user is None:
		login(request, user)
		return render(request, 'safe_app/welcome.html', {'show':True})
	return render(request,'safe_app/course.html', {'courses': user.course_set.all()})

def addcourse(request):
	if not request.user.is_authenticated:
		return redirect('welcome')
	course_code = request.POST['course_code']
	user = request.user
	new_course = Course(instructor=user,course_code=course_code)
	new_course.save()
	return render(request,'safe_app/course.html', {'courses': user.course_set.all()})

def removeCourse(request, courseId):
	if not request.user.is_authenticated:
		return redirect('welcome')
	Course.objects.filter(id= courseId).delete()
	user = request.user
	return render(request,'safe_app/course.html', {'courses': user.course_set.all()})

def quiz(request, courseId):
	if not request.user.is_authenticated:
		return redirect('welcome')
	course = Course.objects.get(id=courseId)
	running = course.quiz_set.filter(status='running')
	halted = course.quiz_set.filter(status='halted')
	return render(request,'safe_app/quiz.html', {'running':running, 'halted':halted, 'course':course})

def addquiz(request, courseId):
	if not request.user.is_authenticated:
		return redirect('welcome')
	quiz_code  = request.POST['quiz_code']
	course = Course.objects.get(id=courseId)
	quiz = Quiz(course=course, quiz_code=quiz_code, status='halted')
	quiz.save()
	return redirect('safe_app:quiz',courseId = course.id)

def removeQuiz(request, quizId):
	if not request.user.is_authenticated:
		return redirect('welcome')
	quiz = Quiz.objects.get(id= quizId)
	course  = quiz.course	
	Quiz.objects.filter(id= quizId).delete()
	return redirect('safe_app:quiz',courseId = course.id)

def changeQuizState(request, quizId):
	if not request.user.is_authenticated:
		return redirect('welcome')
	quiz = Quiz.objects.get(id= quizId)
	if quiz.status == 'running':
		quiz.status = 'halted'
	elif quiz.status == 'halted':
		quiz.status = 'running'
	quiz.save()
	course  = quiz.course	
	return redirect('safe_app:quiz',courseId = course.id)	

def questions(request, quizId, show1=False, show2=False):
	if not request.user.is_authenticated:
		return redirect('welcome')
	quiz = Quiz.objects.get(id=quizId)
	q_multiple = quiz.multiplechoice_set.all()
	q_blank = quiz.blank_set.all()
	q_truefalse = quiz.truefalse_set.all()
	questions = []
	for i in q_multiple:
		questions.append([i.question_number, i.id, i.text[:100]])
	for i in q_blank:
		questions.append([i.question_number, i.id, i.text[:100]])
	for i in q_truefalse:
		questions.append([i.question_number, i.id, i.text[:100]])
	questions.sort(key = lambda x: x[0])	
	return render(request, 'safe_app/questions.html', {'questions': questions, 'quiz':quiz, 'show1':show1, 'show2':show2})

def addBlank(request, quizId):
	if not request.user.is_authenticated:
		return redirect('welcome')
	quiz = Quiz.objects.get(id=quizId)
	blank = Blank(text = request.POST['question'], question_number = quiz.number_of_questions, quiz=quiz)
	blank.save()
	quiz.number_of_questions = quiz.number_of_questions + 1
	quiz.save()
	return redirect('safe_app:questions', quizId = quiz.id)

def addTrueFalse(request, quizId):
	if not request.user.is_authenticated:
		return redirect('welcome')
	quiz = Quiz.objects.get(id=quizId)
	blank = TrueFalse(text = request.POST['question'], question_number = quiz.number_of_questions, quiz=quiz)
	blank.save()
	quiz.number_of_questions = quiz.number_of_questions + 1
	quiz.save()
	return redirect('safe_app:questions', quizId = quiz.id)

def addMultipleChoice(request, quizId):
	if not request.user.is_authenticated:
		return redirect('welcome')
	quiz = Quiz.objects.get(id=quizId)
	blank = MultipleChoice(text = request.POST['question'],question_number = quiz.number_of_questions,quiz=quiz,option1=
		request.POST['option1'],option2=request.POST['option2'],option3=request.POST['option3'],option4=request.POST['option4'])
	blank.save()
	quiz.number_of_questions = quiz.number_of_questions + 1
	quiz.save()
	return redirect('safe_app:questions', quizId = quiz.id)

def showStudent(request, quizId):
	if not request.user.is_authenticated:
		return redirect('welcome')
	quiz = Quiz.objects.get(id=quizId)
	return render(request, 'safe_app/students.html', {'students': quiz.student_set.all(), 'quiz':quiz})

def addStudent(request, quizId):
	if not request.user.is_authenticated:
		return redirect('welcome')
	quiz = Quiz.objects.get(id=quizId)
	student  = Student(quiz=quiz, loginId=request.POST['loginId'], password=request.POST['password'])
	student.save()
	return redirect('safe_app:questions', quizId = quiz.id)

def StudentFile(request, quizId, check):
	if not request.user.is_authenticated:
		return redirect('welcome')
	quiz = Quiz.objects.get(id=quizId)
	file_type = request.POST['file_type']
	file= request.FILES['file_name']
	if file_type=='.xlsx':
		try:
			wb = openpyxl.load_workbook(file)
		except:
			return questions(request, quizId, show1=True)
		if check:
			Student.objects.all().delete()
		for sheet in wb:
			x = tuple(sheet.rows)[1:]
			print(x)
			for row in x:
				if len(row)>=2:
					student = Student(quiz=quiz, loginId=row[0].value, password=row[1].value)
					student.save()
			return redirect('safe_app:questions', quizId = quiz.id)
	if file_type=='.csv':
		try:
			file_data = file.read().decode("utf-8")
		except:
			return questions(request, quizId, show1=True)
		if check:
			Student.objects.all().delete()		
		lines = file_data.split("\n")[1:]
		for line in lines:
			fields = line.split(",")
			if len(fields) >= 2:
				student = Student(quiz=quiz, loginId=fields[0], password=fields[1])
				student.save()
		return redirect('safe_app:questions', quizId = quiz.id)
	if file_type=='.ods':
		try:
			file_data = get_data(file)
		except:
			return questions(request, quizId, show1=True)
		if check:
			Student.objects.all().delete()
		for sheet in file_data:
			l = file_data[sheet][1:]
			for l1 in l:
				if len(l1)>=2:
					student = Student(quiz=quiz, loginId=l1[0], password=l1[1])
					student.save()
			return redirect('safe_app:questions', quizId = quiz.id)

def newStudentFile(request, quizId):
	return StudentFile(request, quizId, True)

def addStudentFile(request, quizId):
	return StudentFile(request, quizId, False)

def question(request, questionNumber):
	if not request.user.is_authenticated:
		return redirect('welcome')
	q = Blank.objects.filter(question_number= questionNumber)
	if len(q)==1:
		quiz = q[0].quiz
		return render(request, 'safe_app/question.html', {'question':q[0],'show': False,'text':q[0].text})
	q = MultipleChoice.objects.filter(question_number= questionNumber)
	if len(q)==1:
		quiz = q[0].quiz
		return render(request, 'safe_app/question.html', {'question':q[0],'show': True,'text':q[0].text,
			'option1':q[0].option1, 'option2':q[0].option2, 'option3':q[0].option3, 'option4':q[0].option4})
	q = TrueFalse.objects.filter(question_number= questionNumber)
	if len(q)==1:
		quiz = q[0].quiz
		return render(request, 'safe_app/question.html', {'question':q[0], 'show': False,'text':q[0].text})

def removeQuestion(request, questionNumber):
	if not request.user.is_authenticated:
		return redirect('welcome')
	q = Blank.objects.filter(question_number= questionNumber)
	if len(q)==1:
		quiz = q[0].quiz
		Blank.objects.filter(id=q[0].id).delete()
		return redirect('safe_app:questions', quizId = quiz.id)
	q = MultipleChoice.objects.filter(question_number= questionNumber)
	if len(q)==1:
		quiz = q[0].quiz
		MultipleChoice.objects.filter(id=q[0].id).delete()
		return redirect('safe_app:questions', quizId = quiz.id)
	q = TrueFalse.objects.filter(question_number= questionNumber)
	if len(q)==1:
		quiz = q[0].quiz
		TrueFalse.objects.filter(id=q[0].id).delete()
		return redirect('safe_app:questions', quizId = quiz.id)

def saveQuestion(request, questionNumber):
	if not request.user.is_authenticated:
		return redirect('welcome')
	q = Blank.objects.filter(question_number= questionNumber)
	if len(q)==1:
		quiz = q[0].quiz
		q[0].text = request.POST['text']
		q[0].save()
		return redirect('safe_app:questions', quizId = quiz.id)
	q = MultipleChoice.objects.filter(question_number= questionNumber)
	if len(q)==1:
		quiz = q[0].quiz
		q[0].text = request.POST['text']
		q[0].option1 = request.POST['option1']
		q[0].option2 = request.POST['option2']
		q[0].option3 = request.POST['option3']
		q[0].option4 = request.POST['option4']
		q[0].save()
		return redirect('safe_app:questions', quizId = quiz.id)
	q = TrueFalse.objects.filter(question_number= questionNumber)
	if len(q)==1:
		quiz = q[0].quiz
		q[0].text = request.POST['text']
		q[0].save()
		return redirect('safe_app:questions', quizId = quiz.id)







