from django.urls import path
from .views import welcome , course, addcourse, quiz, addquiz, removeCourse, removeQuiz, changeQuizState, questions
from .views import addBlank, addTrueFalse, addMultipleChoice, addStudent, showStudent
from .views import newStudentFile, addStudentFile, saveQuestion, removeQuestion, question

app_name = 'safe_app'  ## URL Name space
urlpatterns = [
    path('welcome/', welcome, name='welcome'),
    path('course/', course, name='course'),
    path('addcourse/', addcourse, name='addcourse'),
    path('quiz/<int:courseId>/', quiz, name='quiz'),
    path('addquiz/<int:courseId>/', addquiz, name='addquiz'),
    path('removecourse/<int:courseId>/', removeCourse, name='removecourse'),
    path('removequiz/<int:quizId>/', removeQuiz, name='removequiz'),
    path('changequizstate/<int:quizId>/', changeQuizState, name='changequizstate'),
    path('questions/<int:quizId>/', questions, name='questions'),
   	path('addblank/<int:quizId>/', addBlank, name='addblank'),
    path('addtruefalse/<int:quizId>/', addTrueFalse, name='addtruefalse'),
    path('addmultiplechoice/<int:quizId>/', addMultipleChoice, name='addmultiplechoice'),
    path('showstudent/<int:quizId>/', showStudent, name='showstudent'),
    path('addstudent/<int:quizId>/', addStudent, name='addstudent'),
    path('newstudentfile/<int:quizId>/', newStudentFile, name='newstudentfile'),
    path('addstudentfile/<int:quizId>/', addStudentFile, name='addstudentfile'),
    path('question/<int:questionNumber>/', question, name='question'),
    path('removequestion/<int:questionNumber>/', removeQuestion, name='removequestion'),
    path('savequestion/<int:questionNumber>/',saveQuestion, name='savequestion'),
]