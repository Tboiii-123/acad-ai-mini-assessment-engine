from django.shortcuts import render, get_object_or_404

# Third-party imports
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Local app imports
from .serializers import (
    RegisterSerializer,
    ExamSerializer,
    QuestionSerializer,
    SubmissionAnswerSerializer,
    SubmitExamSerializer,
    SubmissionSerializer
)
from .models import User, Exam, Question, Submission, SubmissionAnswer
from .grading.grader import grade_text


@swagger_auto_schema(
    method='post',
    request_body=RegisterSerializer,
    
    responses={
        201: openapi.Response(
            description="Account created successfully",
            schema=RegisterSerializer
        ),
        400: "Validation error"
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "success": "Account created successfully!!",
            "data": serializer.data
        }, status=201)
    return Response({"error": serializer.errors}, status=400)


# --------------------------------------
# List all Exams
# --------------------------------------
@swagger_auto_schema(
    method='get',
     tags=['Exam List'],
    responses={
        200: openapi.Response(
            description="List of exams",
            schema=ExamSerializer(many=True)
        ),
        401: "Unauthorized"
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exam_list(request):
    exams = Exam.objects.prefetch_related('questions').all()
    serializer = ExamSerializer(exams, many=True)
    return Response(serializer.data)



@swagger_auto_schema(
    method='get',
     tags=['Exam Details'],
    responses={
        200: openapi.Response(
            description="Exam details with questions",
            schema=ExamSerializer()
        ),
        401: "Unauthorized",
        404: "Exam not found"
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exam_detail(request, pk):
    exam = get_object_or_404(Exam.objects.prefetch_related('questions'), id=pk)
    serializer = ExamSerializer(exam)
    return Response(serializer.data)



@swagger_auto_schema(
    method='post',
    request_body=SubmitExamSerializer,
     tags=['Submit Exam'],
    responses={
        200: openapi.Response(
            description="Exam submitted successfully",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'submission_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'score': openapi.Schema(type=openapi.TYPE_NUMBER)
                }
            )
        ),
        400: "Bad request / Already submitted",
        401: "Unauthorized",
        404: "Exam or question not found"
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    # Check if the student has already submitted
    if Submission.objects.filter(student=request.user, exam=exam).exists():
        return Response({"detail": "You have already submitted this exam."}, status=400)

    # Validate input
    serializer = SubmitExamSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # Create submission object
    submission = Submission.objects.create(student=request.user, exam=exam)

    total_score = 0
    submission_answers = []

    # Prepare SubmissionAnswer objects
    for item in serializer.validated_data['answers']:
        question = get_object_or_404(exam.questions, id=item['question'])

        if question.question_type == 'MCQ':
            is_correct = item['answer'].strip() == question.correct_option.strip()
            marks = question.marks if is_correct else 0
        elif question.question_type == 'TEXT':
            marks = grade_text(question, item['answer'])
        else:
            marks = 0

        submission_answer = SubmissionAnswer(
            submission=submission,
            question=question,
            answer=item['answer'],
            awarded_marks=marks
        )
        submission_answers.append(submission_answer)
        total_score += marks

    # Bulk create all answers at once
    SubmissionAnswer.objects.bulk_create(submission_answers)

    # Save total score
    submission.score = total_score
    submission.save()

    return Response({
        "submission_id": submission.id,
        "score": submission.score
    })

@swagger_auto_schema(
    method='get',
     tags=['View Submission'],
    responses={
        200: openapi.Response(
            description="List of user's submissions",
            schema=SubmissionSerializer(many=True)
        ),
        401: "Unauthorized"
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_submission(request):
    user_submissions = Submission.objects.select_related('exam').filter(student=request.user)
    serializer = SubmissionSerializer(user_submissions, many=True)
    return Response(serializer.data)
