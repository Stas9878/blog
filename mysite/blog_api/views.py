from rest_framework import generics,filters,permissions
from blog.models import Post
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly

class StandartPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10

class PostList(generics.ListCreateAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['body', 'author__username','title']
    # ordering_fields = ['author_id', 'publish']
    ordering_fields = '__all__'
    ordering = ['body']
    pagination_class = StandartPagination
    
    # def get_queryset(self):
    #     user = self.request.user
    #     return Post.objects.filter(author=user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class UserPostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.kwargs['username']
        return Post.objects.filter(author=user)
    
#С миксинами

# from rest_framework import mixins
# from rest_framework import generics
# from blog.models import Post
# from .serializers import PostSerializer

# class PostList(mixins.ListModelMixin,
#                mixins.CreateModelMixin,
#                generics.GenericAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs) 
    

# class PostDetail(mixins.RetrieveModelMixin,
#                 mixins.UpdateModelMixin,
#                 mixins.DestroyModelMixin,
#                 generics.GenericAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def patch(self, request, *args, **kwargs):
#         return self.partial_update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
    


#без миксинов

# from django.http import Http404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# from blog.models import Post
# from .serializers import PostSerializer

# class PostList(APIView):
#     def get(self, request, format=None):
#         transformers = Post.objects.all()
#         serializer = PostSerializer(transformers, many=True)
#         return Response(serializer.data)
    
#     def post(self,request, format=None):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class PostDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Post.objects.get(pk=pk)
#         except Post.DoesNotExist:
#             raise Http404
    
#     def get(self, request, pk, format=None):
#         transformer = self.get_object(pk)
#         serializer = PostSerializer(transformer)
#         return Response(serializer.data)
    
#     def put(self, request, pk, format=None):
#         transformer = self.get_object(pk)
#         serializer = PostSerializer(transformer, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def path(self, request, pk, format=None):
#         transformer = self.get_object(pk)
#         serializer = PostSerializer(transformer, 
#                                     data=request.data,
#                                     partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, required, pk, format=None):
#         transformer = self.get_object(pk)
#         transformer.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)