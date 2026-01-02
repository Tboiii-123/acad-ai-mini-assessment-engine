from rest_framework import serializers
from .models import User, Question, Exam, Submission,SubmissionAnswer


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password')

    def create(self, validated_data):
        user = User(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)

# ---------- QUESTIONS ----------
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'options', 'marks','question_type']


# ---------- EXAMS ----------
class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'course', 'duration_minutes', 'questions']


# ---------- SUBMIT EXAM (INPUT ONLY) ----------
class SubmissionAnswerInputSerializer(serializers.Serializer):
    question = serializers.IntegerField()
    answer = serializers.CharField(max_length=1000)


class SubmitExamSerializer(serializers.Serializer):
    answers = SubmissionAnswerInputSerializer(many=True)




# ---------- VIEW SUBMISSION (OUTPUT ONLY) ----------
class SubmissionAnswerSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = SubmissionAnswer
        fields = ['question', 'answer','awarded_marks']


class SubmissionSerializer(serializers.ModelSerializer):
    exam = ExamSerializer(read_only=True)
    answers = SubmissionAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Submission
        fields = ['id', 'exam', 'score', 'submitted_at', 'answers']
