from django.urls import path, include, register_converter
from engine import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'engine'
urlpatterns = [
    path('neighbors/<str:image_id>/', views.AllNeighborsOfNode.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
