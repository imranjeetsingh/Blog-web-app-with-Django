from rest_framework.serializers import (
        ModelSerializer,
        HyperlinkedIdentityField,
        SerializerMethodField
        )
from comments.api.serializers import CommentSerializer
from comments.models import Comment

from posts.models import Post

class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            # 'id',
            'title',
            # 'slug',
            'content',
            'publish'
        ]

class PostListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='posts-api:detail',
        lookup_field='slug'
        )
    user = SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            'url',
            'user',
            'title',
            # 'slug',
            'content',
            'publish'
        ]
    def get_user(self, obj):
        return str(obj.user.username)

class PostDetailSerializer(ModelSerializer):
    user = SerializerMethodField()
    image = SerializerMethodField()
    html = SerializerMethodField()
    comments = SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'title',
            'slug',
            'content',
            'html',
            'publish',
            'image',
            'comments',
        ]
    def get_user(self, obj):
        return str(obj.user.username)

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image
    
    def get_html(self, obj):
        return obj.get_markdown()

    def get_comments(self,obj):
        qs = Comment.objects.filter_by_instance(obj)
        print(qs)
        comments = CommentSerializer(qs,many=True).data
        return comments