from django.core.management import BaseCommand
from models.models import CategoryLabel, LabelID

class Command(BaseCommand):
    help = 'Initalize category labels with associated label IDs'
    
    def handle(self, *args, **kwargs):
        # Define the caregory labels for MS COCO
        category_labels = {
            'Animals': [15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
            'Vehicles': [2, 3, 4, 5, 6, 7, 8, 9],
            'Sports and Recreation': [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
            'Food and Drinks': [47, 48, 49, 50, 51, 52, 53, 54, 55, 56],
            'Furniture': [57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 76, 77, 78, 79, 80],
            'People': [0, 1]
        }
        
        for category_name, label_ids in category_labels.items():
            category_label = CategoryLabel.objects.create(label_name=category_name)
            for label_id in label_ids:
                label_instance, created = LabelID.objects.get_or_create(label_id=label_id)
                category_label.label_ids.add(label_instance)
            
            category_label.save()
            
        self.stdout.write(self.style.SUCCESS('Successfully added category labels'))