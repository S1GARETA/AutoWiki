import json

from rest_framework import serializers
from .models import Auto, Section, SubSection


class AutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auto
        fields = ('car_brand', 'car_model', 'generation', 'slug')

class SubSectionSerializer(serializers.ModelSerializer):
    section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())

    class Meta:
        model = SubSection
        fields = ('id', 'title', 'content', 'section')

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('name', 'slug')