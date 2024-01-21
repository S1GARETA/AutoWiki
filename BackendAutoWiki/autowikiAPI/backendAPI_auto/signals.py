from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Auto, Instruction, Section


@receiver(post_save, sender=Auto)
def create_instruction_and_sections(sender, instance, created, **kwargs):

    if created:
        # Create Instruction
        instruction = Instruction.objects.create(
            name=f"Инструкция для {instance.car_brand} {instance.car_model} {instance.generation}",
            car=instance
        )

        # Create Sections
        electronics_section = Section.objects.create(name="Электроника", instruction=instruction)
        body_section = Section.objects.create(name="Кузов", instruction=instruction)
        engine_section = Section.objects.create(name="Двигатель", instruction=instruction)

        # You can add more sections as needed
