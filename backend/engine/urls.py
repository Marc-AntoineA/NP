from django.urls import path, include, register_converter
from engine import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'engine'
urlpatterns = [
    path('neighbors', views.AllGraph.as_view()),
    path('neighbors/<str:picture_id>/', views.AllNeighborsOfNode.as_view()),
    path('picture/upload', views.test_upload_picture),
    path('picture/delete/<str:picture_id>', views.delete_picture),
    path('tags', views.AllTagsView.as_view()),
    path('tags/<str:picture_id>', views.TagsView.as_view()),
    path('pictures/less-tagged/<int:nb_pictures>', views.ListPicturesLessTags.as_view()),
    path('pictures/random', views.GetRandomPicture.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
