from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer

class UseCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
         fields = ['id', 'username', 'passward', 'email', 'first_name', 'last_name']

class UserSerializer(BaseUserSerializer):
     class Meta(BaseUserSerializer.Meta):
          fields = ['id', 'username', 'email', 'first_name', 'last_name']       