from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from profiles import views

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', views.registration_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.ProfileList.as_view(), name='list'),
    path('<int:pk>', views.ProfileDetail.as_view(), name="detail"),
    path(
        '<int:pk>/<str:action>', views.FollowUnfollowView.as_view(),
        name="relation"
    )
]
