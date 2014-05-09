from django.contrib import admin
from models import *

class DatasetAdmin(admin.ModelAdmin):
    list_display = ('name', 'identifier')

admin.site.register(Dataset, DatasetAdmin)

class RenderBlockAdmin(admin.ModelAdmin):
    list_display = ('source', 'identifier', 'state', 'dataset', 'modified')
    list_filter = ('dataset', 'state')
    search_fields = ('source',)

admin.site.register(RenderBlock, RenderBlockAdmin)
