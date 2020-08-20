from django.urls import path, include
from hotplace.views import *

app_name = 'hotplace'

urlpatterns=[
    path('',HotplaceLV.as_view(),name='index'),
    path('<int:pk>/',HotplaceDV.as_view(),name='detail'),

    #태그
    # Example :/hotplace/tag
    path('tag',TagCloudTV.as_view(),name='tag_cloud'),
    # Example :/hotplace/tag/tagname/
    path('tag/<str:tag>',TaggedObjectLV.as_view(),name='tagged_object_list'),

    #Archive
    path('archive/',HotplaceAV.as_view(),name='hotplace_archive'),
    path('archive/<int:year>/',HotplaceYAV.as_view(),name='hotplace_year_archive'),
    path('archive/<int:year>/<str:month>/',HotplaceMAV.as_view(),name='hotplace_month_archive'),

    # 추가 삭제
    # hotplace/add
    path('add/',HotplaceCreateView.as_view(),name='add'),
    # hotplace/99/update
    path('<int:pk>/update/',HotplaceUpdateView.as_view(),name="update"),
    # hotplace/99/delete
    path('<int:pk>/delete/',HotplaceDeleteView.as_view(),name='delete'),

    #다운로드
    path('download/<int:id>',download,name="download"),



]