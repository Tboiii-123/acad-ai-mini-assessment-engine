
from  django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('auth/register/', views.register_view, name='register'),
    #Return access token ad refresh token
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('exam_list/',views.exam_list , name='exam_list')   ,
    path('exam_detail/<int:pk>/',views.exam_detail , name='exam_detail'),
    path('submit_exam/<int:exam_id>/',views.submit_exam , name='submit_exam'),
    path('view_submission/',views.view_submission , name='view_submit'),
    
    
       
     
    ]

    