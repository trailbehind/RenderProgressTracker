from django.shortcuts import render
from django.views.generic import TemplateView

from rest_framework import viewsets

from RenderProgress.models import Dataset, RenderBlock
from RenderProgress.serializers import RenderBlockSerializer


class RenderBlockViewSet(viewsets.ModelViewSet):
    """
    API endpoint that provides geojson feature collection
    """
    serializer_class = RenderBlockSerializer
    model = RenderBlock

    def get_queryset(self):
    	return RenderBlock.objects.all()

class RenderBlockMap(TemplateView):
    template_name = "map.html"
