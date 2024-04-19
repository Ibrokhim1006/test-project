from django.urls import path
from authen.views.views import UserSignUp, UserSignIn, UserProfile

urlpatterns = [
    path('register/', UserSignUp.as_view(), name="User register"),
    path('sigin-in/', UserSignIn.as_view(), name='User login'),
    path('profile/', UserProfile.as_view(), name='User profile'),

]
