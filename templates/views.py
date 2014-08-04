# from rest_framework import viewsets
# from rest_framework.response import Response
# from rest_framework import filters
from templates.serializer import *
from invt.views import ImageListViewSet

class TemplateViewSet(ImageListViewSet):

    base = API_BASE
    uri = URI

    model = Template
    serializer_class = TemplateSerializer
    filter_backends = []

    def pre_save(self, obj):
        obj.author = self.request.user

    # def get_serializer_class(self):
    #     request = self.request
    #     if request.method == 'GET':
    #         if request.is_mobile:
    #             return SimpleImageSerializer
    #         else:
    #             return ImageDetailSerializer
    #     else:
    #         return ImageSerializer
    #
    # def retrieve(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     serializer = ImageDetailSerializer(self.object)
    #     return Response(serializer.data)