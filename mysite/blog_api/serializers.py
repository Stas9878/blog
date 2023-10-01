from rest_framework import serializers
from blog.models import Post

class PostSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())#автоматическая подстановка юзера
    class Meta:
        fields = (
            'id','author','title','body','created'
        )
        model = Post
