from django.contrib import admin

from .models import Auto, Instruction, Section, SubSection

# Register your models here.
admin.site.register(Instruction)
admin.site.register(Section)
admin.site.register(SubSection)

@admin.register(Auto)
class AutoAdmin(admin.ModelAdmin):
    fields = ['car_brand', 'car_model', 'generation', 'slug']
    prepopulated_fields = {'slug': ('car_brand', 'car_model', 'generation',)}