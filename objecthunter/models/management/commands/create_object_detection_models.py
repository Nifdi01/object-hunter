# from django.core.management.base import BaseCommand
# from models.models import ObjectDetectionModel, CategoryLabel
# from django.conf import settings
# import os

# class Command(BaseCommand):
#     help = 'Create object detection models for corresponding categories'

#     def handle(self, *args, **kwargs):
#         category_labels = {
#             'Animals': [15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
#             'Vehicles': [2, 3, 4, 5, 6, 7, 8, 9],
#             'Sports and Recreation': [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
#             'Food and Drinks': [47, 48, 49, 50, 51, 52, 53, 54, 55, 56],
#             'Furniture': [57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 76, 77, 78, 79, 80],
#         }

#         # Create models for each category label
#         for category_name, label_ids in category_labels.items():
#             category_label, created = CategoryLabel.objects.get_or_create(label_name=category_name)
#             for label_id in label_ids:
#                 ObjectDetectionModel.objects.create(
#                     title=f"{category_name} Detector",
#                     description=f"Object detector for {category_name}",
#                     model_file=os.path.join(settings.MEDIA_URL, 'yolov8n.pt'),  # Provide the actual path to the model file
#                     category_label=category_label,
#                 )
#                 self.stdout.write(self.style.SUCCESS(f'Successfully created {category_name} Detector model'))
