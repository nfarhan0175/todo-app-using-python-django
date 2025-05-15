from django.urls import path
from .views import taskList,customLogin,register
from .views import  taskDetail,taskCreate,taskUpdate,taskDelete
from django.contrib.auth.views import LogoutView 


urlpatterns = [
    path('taskList/', taskList.as_view(), name='taskList'),
    path('taskCreate/', taskCreate.as_view(), name='taskCreate'),
    path('taskDetail/', taskDetail.as_view(), name='taskDetail'),
    path('taskUpdate/<int:pk>', taskUpdate.as_view(), name='taskUpdate'),
    path('taskDelete/<int:pk>', taskDelete.as_view(), name='taskDelete'),
    path('login/',customLogin.as_view(), name='login'),
    path('register/',register.as_view(), name='register'),
    path('logout/',LogoutView.as_view(next_page = 'login'), name='logout'),
]
