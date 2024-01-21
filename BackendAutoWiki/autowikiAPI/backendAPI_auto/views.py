from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import F
import json

from .models import Auto, Section, SubSection
from .serializer import AutoSerializer, SubSectionSerializer, SectionSerializer


# Create your views here.

class AutoAPIList(generics.ListCreateAPIView):
    queryset = Auto.objects.all()
    serializer_class = AutoSerializer

class AutoBrandsView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        car_brands = Auto.objects.values_list('car_brand', flat=True).distinct().order_by(F('car_brand').asc())

        return Response(list(car_brands))

class AutoModelsView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, car_brand):
        car_models = Auto.objects.filter(car_brand=car_brand).select_related('car_brand').values_list('car_model', flat=True).distinct().order_by(F('car_model').asc())

        return Response(list(car_models))

class AutoGenerationsView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, car_model):
        car_generations = Auto.objects.filter(car_model=car_model).values_list('generation', flat=True).distinct().order_by(F('generation').asc())

        return Response(list(car_generations))

class AutoSectionsView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        try:
            # Получите марку и модель автомобиля из тела запроса
            car_brand = request.data.get('car_brand', '')
            car_model = request.data.get('car_model', '')

            # Проверьте, что оба параметра присутствуют
            if not car_brand or not car_model:
                return Response({"error": "Параметры 'car_brand' и 'car_model' обязательны"}, status=400)

            # Получите автомобили по марке и модели
            autos = Auto.objects.filter(car_brand=car_brand, car_model=car_model)

            # Проверьте, что хотя бы один автомобиль найден
            if not autos.exists():
                return Response({"error": "Автомобили не найдены"}, status=404)

            # Возьмите первый автомобиль (можно настроить логику выбора, если их много)
            auto = autos.first()

            # Получите инструкцию для автомобиля
            instruction = auto.instruction

            # Получите все разделы для данной инструкции
            sections = Section.objects.filter(instruction=instruction)

            # Сериализуйте данные разделов
            serializer = SectionSerializer(sections, many=True)

            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

class AutoGetSlug(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            car_brand = data.get('car_brand')
            car_model = data.get('car_model')
            generation = data.get('generation')

            auto = Auto.objects.get(
                car_brand=car_brand,
                car_model=car_model,
                generation=generation
            )

            car_slug = auto.slug
            return Response({'car_slug': car_slug})
        except Auto.DoesNotExist:
            return Response({'error': 'Автомобиль не найден'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

class CarSectionsView(APIView):
    def get(self, request, car_slug, *args, **kwargs):
        auto = Auto.objects.get(slug=car_slug)

        # Данные об автомобиле
        car_data = {
            'auto_id': auto.id,
            'car_brand': auto.car_brand,
            'car_model': auto.car_model,
            'generation': auto.generation,
            'slug': auto.slug,
        }

        # Получите связанную инструкцию для автомобиля
        instruction = auto.instruction

        # Получите все разделы для данной инструкции
        sections = Section.objects.filter(instruction=instruction)
        sections_data = [{'name': section.name, 'slug': section.slug, 'id': section.id} for section in sections]

        # Получите все подразделы для каждого раздела
        subsections_data = {}
        for section in sections:
            subsections = SubSection.objects.filter(section=section)
            subsections_data[section.id] = [{'title': sub_section.title, 'content': sub_section.content} for sub_section in subsections]

        # Верните данные в формате JSON
        return Response({'car_data': car_data, 'sections': sections_data, 'subsections': subsections_data})

class SubSectionsView(APIView):

    # GET - Get SubSection
    def get(self, request, car_slug, section_slug):
        try:
            # Получите автомобиль по slug
            auto = Auto.objects.get(slug=car_slug)

            # Получите инструкцию для автомобиля
            instruction = auto.instruction

            # Получите раздел по slug и инструкции
            section = Section.objects.get(slug=section_slug, instruction=instruction)

            # Получите все подразделы для выбранного раздела
            subsections = SubSection.objects.filter(section=section)

            # Сериализуйте данные подразделов
            serializer = SubSectionSerializer(subsections, many=True)

            return Response(serializer.data)
        except Auto.DoesNotExist:
            return Response({"error": "Автомобиль не найден"}, status=404)
        except Section.DoesNotExist:
            return Response({"error": "Раздел не найден"}, status=404)

    # POST - Create SubSection
    def post(self, request, car_slug, section_slug):
        try:
            # Получите автомобиль по slug
            auto = Auto.objects.get(slug=car_slug)

            # Получите инструкцию для автомобиля
            instruction = auto.instruction

            # Получите раздел по slug и инструкции
            section = Section.objects.get(slug=section_slug, instruction=instruction)

            # Создайте подраздел
            data = {
                'title': request.data.get('title'),
                'content': request.data.get('content'),
                'section': section.id  # Используйте section.id вместо section
            }
            serializer = SubSectionSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Auto.DoesNotExist:
            return Response({"error": "Автомобиль не найден"}, status=status.HTTP_404_NOT_FOUND)
        except Section.DoesNotExist:
            return Response({"error": "Раздел не найден"}, status=status.HTTP_404_NOT_FOUND)

    # PUT - Update Subsection
    def put(self, request, car_slug, section_slug, subsection_id):
        try:
            # Получите автомобиль по slug
            auto = Auto.objects.get(slug=car_slug)

            # Получите инструкцию для автомобиля
            instruction = auto.instruction

            # Получите раздел по slug и инструкции
            section = Section.objects.get(slug=section_slug, instruction=instruction)

            # Получите подраздел по id
            subsection = SubSection.objects.get(id=subsection_id, section=section)

            data = {
                'title': request.data.get('title'),
                'content': request.data.get('content'),
                'section': section.id  # Используйте section.id вместо section
            }

            # Обновите подраздел
            serializer = SubSectionSerializer(subsection, data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Auto.DoesNotExist:
            return Response({"error": "Автомобиль не найден"}, status=status.HTTP_404_NOT_FOUND)
        except Section.DoesNotExist:
            return Response({"error": "Раздел не найден"}, status=status.HTTP_404_NOT_FOUND)
        except SubSection.DoesNotExist:
            return Response({"error": "Подраздел не найден"}, status=status.HTTP_404_NOT_FOUND)
