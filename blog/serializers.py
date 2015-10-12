from rest_framework import routers, serializers, viewsets
from blog.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post

 # ViewSets define the view behavior.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

 # Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)