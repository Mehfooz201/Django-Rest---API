from django.urls import path, include
from home.views import home, person, login, PersonAPI, PersonViewSet, RegisterAPI, LoginApi
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'people', PersonViewSet, basename='user')
urlpatterns = router.urls


urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAPI.as_view()),
    path('login/', LoginApi.as_view()),
    path('person/', person),
    path('login/', login),
    path('persons/', PersonAPI.as_view()),
    path('login/', login),
]
