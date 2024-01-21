from rest_framework import serializers
from djoser.serializers import UserCreateSerializer

from backendAPI_auto.models import Auto, Section
from backendAPI_forum.models import ForumPost
from .models import CustomUser, Favorite


# Вывод списка пользователей
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username')



# Регистрация и авторизация
class CustomUserCreateSerializer(UserCreateSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        return super().create(validated_data)

class AutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auto
        fields = ['car_brand', 'car_model', 'generation', 'slug']

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['name', 'slug']

class ForumPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForumPost
        fields = ['title', 'content', 'auto', 'section']

class FavoriteSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'item_type', 'item_id', 'item']

    def get_item(self, obj):
        if obj.item_type == 'auto':
            try:
                auto = Auto.objects.get(pk=obj.item_id)
                return {
                    'car_brand': auto.car_brand,
                    'car_model': auto.car_model,
                    'generation': auto.generation,
                    'slug': auto.slug,
                }
            except Auto.DoesNotExist:
                return None
        elif obj.item_type == 'post':
            try:
                post = ForumPost.objects.get(pk=obj.item_id)
                return {
                    'title': post.title,
                    'auto': {
                        'car_brand': post.auto.car_brand,
                        'car_model': post.auto.car_model,
                    } if post.auto else None,
                    'section': {
                        'slug': post.section.slug,
                    } if post.section else None,
                }
            except ForumPost.DoesNotExist:
                return None
        else:
            return None