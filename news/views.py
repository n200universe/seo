from django.shortcuts import render
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from .models import Category, Post
from .serializers import CategorySerializer, ItemSerializer, PostSerializer
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission, IsAdminUser, DjangoModelPermissions


# Create your views here.
class PostList(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CategoryList(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ItemViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = ItemSerializer
    lookup_field = 'slug'


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [PostUserWritePermission]
    # lookup_field = ["slug"]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# class PostByCategory(generics.ListAPIView):
#     # queryset = Post.objects.filter()
#     def get_queryset(self, *args, **kwargs):
#         print(self.request.data)

#     # project = get_object_or_404(Projects, id=kwargs.get["pk"])
#         return Post.objects.filter(id=self.request.data["pk"])

class PostByCategory(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        category = self.kwargs["pk"]
        return Post.objects.filter(category__id=category)

   
