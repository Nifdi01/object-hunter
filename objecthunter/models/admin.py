from django.contrib import admin
from .models import CategoryLabel, ObjectDetectionModel

class CategoryLabelAdmin(admin.ModelAdmin):
    list_display = ('label_name', 'get_label_ids')

    def get_label_ids(self, obj):
        # This method returns a comma-separated string of label IDs associated with the CategoryLabel
        return ', '.join([str(label.label_id) for label in obj.label_ids.all()])

    # Set a user-friendly column header for get_label_ids method
    get_label_ids.short_description = 'Label IDs'

admin.site.register(CategoryLabel, CategoryLabelAdmin)

admin.site.register(ObjectDetectionModel)