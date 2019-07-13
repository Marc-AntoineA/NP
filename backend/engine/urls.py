from django.urls import path, include, register_converter
from engine import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'engine'
urlpatterns = [
    path('neighbors/<str:picture_id>/', views.AllNeighborsOfNode.as_view()),
    path('upload/picture', views.testUploadPicture),
    path('tags', views.AllTagsView.as_view()),
    path('tags/<str:picture_id>', views.TagsView.as_view()),
    path('pictures/moins-tags', views.listPicturesLessTags),
    path('pictures/random', views.GetRandomPicture.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
