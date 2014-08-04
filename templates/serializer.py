
from rest_framework import serializers
from templates.models import *

class TemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Template
        fields = ('id', 'title', 'desc', 'uri', 'style', 'image')
        read_only_fields = ('array',)


