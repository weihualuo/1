
from rest_framework import viewsets, generics
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.http import HttpResponse
from utils import default_int
from django.db.utils import IntegrityError
from functools import wraps

from django.http import HttpResponse
from django.views.generic import View
from invt import settings

class WithParentMixin(object):

    parents = {}

    @property
    def parentName(self):
        if not hasattr(self, '_parentName'):
            name = self.kwargs.get('name')
            if name in self.parents:
                self._parentName = name
            else:
                self._parentName = None
        return self._parentName

    @property
    def parentModel(self):
        return self.parents.get(self.parentName)

    @property
    def parent(self):
        if not hasattr(self, '_parent'):
            pk = self.kwargs.get('id')
            if not pk or not self.parentModel:
                raise Http404
            self._parent = get_object_or_404(self.parentModel, pk=pk)
        return self._parent


def fuid_required(f):
    @wraps(f)
    def wrapper(self, request, *args, **kwargs):
        import pylibmc as memcache
        #from django.utils.crypto import get_random_string
        mc = memcache.Client()
        import time
        fuid = request.DATA.get('fuid', None)
        if fuid:
            key = "fuid_" + str(request.user.pk) + '_' + str(fuid)
            if mc.get(key):
                print "exist fuid ", key
                return HttpResponse(status=409)
            else:
                print "set", key
                mc.set(key, time.time())
                return f(self, request, *args, **kwargs)
        return HttpResponse(status=403)
    return wrapper


class ListViewSet(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):

        num = default_int(request.QUERY_PARAMS.get('num'), 60)
        all = self.filter_queryset(self.get_queryset())
        total = all.count()
        first = request.QUERY_PARAMS.get('first', None)
        #Get from end of array if it is a refresh
        if first:
            start = total-num if total > num else 0
            self.object_list = all[start:]
        else:
            self.object_list = all[:num]
        serializer = self.get_serializer(self.object_list, many=True)
        ret = {}
        ret['meta'] = {'more': total-len(self.object_list)}
        ret['results'] = serializer.data
        return Response(ret)

class ImageListViewSet(ListViewSet):

    base = 'api/photos/'
    uri = 'photos'

    @fuid_required
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)

        try:
            if serializer.is_valid():
                self.pre_save(serializer.object)
                self.object = serializer.save(force_insert=True)
                self.post_save(self.object, created=True)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED,
                                headers=headers)
        except IntegrityError:
            serializer.errors['image'] = "Duplicated"
        except:
            serializer.errors['image'] = 'error'

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'])
    def thumb(self, request, pk=None):
        from utils import default_int
        import pylibmc as memcache

        seq = request.GET.get('seq')
        token = request.GET.get('token')
        result=status.HTTP_400_BAD_REQUEST

        if seq and token:
            key = self.uri+str(pk)+'-'+str(seq)
            mc = memcache.Client()
            value = mc.get(key)
            if token == value:
                mc.delete(key)
                image = get_object_or_404(self.get_queryset(), pk=pk)
                ret = image.save_thumb(default_int(seq))
                result= status.HTTP_201_CREATED if ret else status.HTTP_304_NOT_MODIFIED
        return Response(status=result)

class MetaView(generics.ListAPIView):

    def list(self, request, *args, **kwargs):
        ret = {}
        if request.user.is_authenticated():
            ret['user'] = 'user'
        # ret['room'] = RoomSerializer(Room.objects.all(), many=True).data
        ret['imgbase'] = settings.STORAGE.url('')
        return Response(ret)


class Information(View):

    class photos:
        def exist(self, name):
            ret = 'NO'
            return ret

        def thumbfail(self, *args):
            print "thumb fail"
            return 'OK'

    def get(self, request, app, item):
        ret = 'NO'
        name = request.GET.get('name')
        if hasattr(self, app):
            object = getattr(self, app)()
            if hasattr(object, item):
                ret = getattr(object, item)(name)
        return HttpResponse(ret)

class Task(View):

    def rectify(self):
        return "rectify OK"

    def landscape(self):
        return "OK"

    def post(self, request, id):
        ret = 'no'
        if hasattr(self, id):
            ret = getattr(self, id)()
        return HttpResponse(ret)







