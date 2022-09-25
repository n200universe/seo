
from django.urls import include, path
from .views import CategoryList, PostList, PostDetail,PostByCategory, ItemViewSet

    
urlpatterns = [
    # path('<slug:slug>/', ItemViewSet.as_view({'get': 'slug'}), name='detailcreate'),
    path('<int:pk>/', PostDetail.as_view(), name='detailcreate'),

    path('', PostList.as_view(), name='listcreate'),
    path('category', CategoryList.as_view(), name='category'),

    path('category/<int:pk>', PostByCategory.as_view())
]

