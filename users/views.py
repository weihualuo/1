
from invt.views import ListViewSet
from users.models import *
from users.serializer import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.utils import IntegrityError

class UserViewSet(ListViewSet):
    model = EndUser
    serializer_class = UserSerializer
    permission_classes = ()

class AuthView(APIView):

    #Override default permissions
    permission_classes = ()

    def post(self, request, id):
        ret = {}
        status = 404
        if hasattr(self, id):
            ret, status = getattr(self, id)(request)
        return Response(ret, status=status)

    def login(self, request):
        username = request.DATA.get('username')
        password = request.DATA.get('password')
        #print "name is", username, "password is", password
        ret = {}
        status = 403
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                ret['user'] = UserSerializer(user).data
                ret['csrf'] = csrf(request)['csrf_token']
                status = 200
            else:
                ret['error'] = 'inactive'
        else:
            ret['error'] = 'invalid'
        return ret, status

    def logout(self, request):
        logout(request)
        return {'user': None}, 200

    def register(self, request):
        username = request.DATA.get('username')
        password = request.DATA.get('password')
        email = request.DATA.get('email')
        #print "name is", username, "password is", password, 'email is', email
        ret = {}
        status = 400
        if username and password and email:
            try:
                User.objects.create_user(username, email, password)
                user = authenticate(username=username, password=password)
                login(request, user)
                ret['user'] = UserSerializer(user).data
                ret['csrf'] = csrf(request)['csrf_token']
                status = 201
            except IntegrityError:
                status = 409
                ret['error'] = 'exist'
            except:
                ret['error'] = 'unknown'
        else:
            ret['error'] = 'invalid'
        return ret, status

    def update(self, request):

        ret = {}
        status = 401
        user = request.user
        if user.is_anonymous():
            ret['error'] = 'unauthorized'
            return ret, status

        su = UserSerializer(user, data=request.DATA, partial=True)

        def saveProfile(user, data):
            if hasattr(user, 'profile'):
                sp = CreateProfileSerializer(user.profile, data=data, partial=True)
            else:
                data['user'] = user.pk
                sp = CreateProfileSerializer(data=data)
            if sp.is_valid():
                sp.save()
                return sp.object, None
            else:
                return None, sp.errors

        if su.is_valid():
            su.save()
            profile = request.DATA.get('profile')
            if profile:
                userprofile, errors = saveProfile(user, profile)
                if userprofile:
                    user.profile = userprofile
                else:
                    ret['error'] = errors
                    print "invalid profile"

            ret['user'] = UserSerializer(user).data
            status = 200

        else:
            status = 400
            ret['error'] = su.errors
        return ret, status


