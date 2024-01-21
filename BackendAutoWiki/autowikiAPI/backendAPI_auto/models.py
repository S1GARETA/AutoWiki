import uuid
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models
from django.utils.text import slugify


def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r', 'ю': 'yu', 'я': 'ya'}

    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))


# Create your models here.

class Auto(models.Model):
    car_brand = models.CharField(max_length=100, verbose_name="Марка")
    car_model = models.CharField(max_length=100, verbose_name="Модель")
    generation = models.CharField(max_length=100, verbose_name="Поколение")
    slug = models.SlugField(max_length=255, unique=True, blank=True, db_index=True, verbose_name="URL")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{translit_to_eng(self.car_brand)} \
                                  {translit_to_eng(self.car_model)} \
                                  {translit_to_eng(self.generation)}")
            super().save(*args, **kwargs)

    def __str__(self):
        return self.slug

class Instruction(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название инструкции")
    car = models.OneToOneField('Auto', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название раздела инструкции")
    slug = models.SlugField(max_length=255, db_index=True, verbose_name="URL Section")
    instruction = models.ForeignKey('Instruction', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{translit_to_eng(self.name)}")
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class SubSection(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название подраздела")
    content = models.TextField(blank=True, verbose_name="Контент")
    section = models.ForeignKey('Section', on_delete=models.CASCADE)