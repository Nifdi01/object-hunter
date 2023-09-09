from django.contrib import admin
from .models import CategoryLabel, ObjectDetectionModel, ModelUseCount

class CategoryLabelAdmin(admin.ModelAdmin):
    list_display = ('label_name', 'get_label_ids')

    def get_label_ids(self, obj):
        # This method returns a comma-separated string of label IDs associated with the CategoryLabel
        return ', '.join([str(label.label_id) for label in obj.label_ids.all()])

    # Set a user-friendly column header for get_label_ids method
    get_label_ids.short_description = 'Label IDs'

admin.site.register(CategoryLabel, CategoryLabelAdmin)

class ObjectDetectionModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'category_label', 'get_inference_modes')

    def get_inference_modes(self, obj):
        # Define a method to retrieve and display the inference modes as a comma-separated string
        return ', '.join([label.label_name for label in obj.classes_during_inference.all()])

    get_inference_modes.short_description = 'Inference Modes'  # Set a custom column header

# Register the admin class for ObjectDetectionModel
admin.site.register(ObjectDetectionModel, ObjectDetectionModelAdmin)


admin.site.register(ModelUseCount)