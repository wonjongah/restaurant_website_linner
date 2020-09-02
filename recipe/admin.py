from django.contrib import admin
from recipe.models import RecipeContent, YoutubeContent

# Register your models here.

@admin.register(RecipeContent)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('Rec_conName','Rec_conModify', 'Rec_conContent','tag_list')
    list_filter = ('Rec_conModify',)
    search_fields = ('Rec_conName','Rec_conContent')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('Rec_conTags')

    def tag_list(self,obj):
        return ','.join(o.name for o in obj.tags.all())
