from django.contrib import admin
from .models import (
    User,
    Question,
    Exam,
    Submission,
    SubmissionAnswer
)
# Register your models here.

admin.site.register(User)
admin.site.register(Question)
admin.site.register(Exam)
admin.site.register(Submission)
admin.site.register(SubmissionAnswer)

