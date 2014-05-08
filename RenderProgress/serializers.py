from rest_framework_gis import serializers as geo_serializers

from RenderProgress.models import Dataset, RenderBlock


class RenderBlockSerializer(geo_serializers.GeoFeatureModelSerializer):

    class Meta:
        model = RenderBlock
        geo_field = 'bounds'