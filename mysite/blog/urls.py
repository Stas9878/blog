from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',post_detail, name='post_detail'),
    path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
    path('<int:post_id>/share/', post_share, name='post_share'),
    path('<int:post_id>/comment/', post_comment, name='post_comment'),
    path('search/', post_search, name='post_search'),
    
]
