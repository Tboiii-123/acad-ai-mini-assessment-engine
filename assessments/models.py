from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin



class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    # Login info

    created_at = models.DateTimeField(auto_now_add=True)

   
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    objects = UserManager()

    USERNAME_FIELD = 'email'
  

    def __str__(self):
        return self.email

 

# Create your models here.
class Exam(models.Model):
    title = models.CharField(max_length=255)
    course = models.CharField(max_length=100)
    duration_minutes = models.PositiveIntegerField()
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["course"]),
        ]

    def __str__(self):
        return self.title



    
class Question(models.Model):
    QUESTION_TYPES = (
        ('MCQ', 'Multiple Choice'),
        ('TEXT', 'Text Answer'),
    )

    exam = models.ForeignKey(Exam,related_name="questions",on_delete=models.CASCADE)
    question_type = models.CharField(max_length=10,choices=QUESTION_TYPES,default='MCQ')

    question_text = models.TextField()

    options = models.JSONField(blank=True, null=True, help_text="MCQ options e.g. {A: 'Option1', B: 'Option2'}")

    
    correct_option = models.CharField(max_length=5, blank=True, null=True,help_text="Correct option key e.g. A")

    correct_text_answer = models.TextField(blank=True, null=True, help_text="Answer for text questions")

    keywords = models.JSONField(blank=True, null=True,help_text="Keywords for grading text answers e.g. ['pythagoras', 'triangle']")



    marks = models.PositiveIntegerField(default=1)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text



class Submission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE,related_name="submissions")
    exam = models.ForeignKey( Exam,on_delete=models.CASCADE,related_name="submissions")
    score = models.FloatField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "exam")
        indexes = [
            models.Index(fields=["student", "exam"]),
        ]

    def __str__(self):
        return f"{self.student} - {self.exam}"

class SubmissionAnswer(models.Model):
    submission = models.ForeignKey( Submission,related_name="answers",on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    answer = models.TextField()
    awarded_marks = models.FloatField(default=0)

    class Meta:
        unique_together = ("submission", "question")
