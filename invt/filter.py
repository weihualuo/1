
from rest_framework import filters
from django.db.models import Q
from django.utils import timezone
from utils import default_int


class CreateFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):

        last = request.QUERY_PARAMS.get('last', None)
        first = request.QUERY_PARAMS.get('first', None)
        if last:
            try:
                cur = queryset.get(pk=last)
                queryset =  queryset.filter(created__lt= cur.created)
            except:
                queryset =  queryset.filter(pk__lt= last)
        elif first:
            try:
                cur = queryset.get(pk=first)
                queryset = queryset.filter(created__gt= cur.created)
            except:
                queryset = queryset.filter(pk__gt= first)
        return queryset

class AuthorFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        author = default_int(request.QUERY_PARAMS.get('author', 0))
        if author:
            queryset = queryset.filter(author=author)
        return queryset

class LocationFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        location= default_int(request.QUERY_PARAMS.get('location', 0))
        if location:
            queryset = queryset.filter(location=location)
        return queryset

class ProfileLocationFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        location= default_int(request.QUERY_PARAMS.get('location', 0))
        if location:
            queryset = queryset.filter(userprofile__location=location)
        return queryset
    
class RoomFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        room= default_int(request.QUERY_PARAMS.get('room', 0))
        if room:
            queryset = queryset.filter(room=room)
        return queryset  
    
class StyleFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        style= default_int(request.QUERY_PARAMS.get('style', 0))
        if style:
            queryset = queryset.filter(style=style)
        return queryset

class TopicFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        topic= default_int(request.QUERY_PARAMS.get('topic', 0))
        if topic:
            queryset = queryset.filter(topic=topic)
        return queryset

class SearchFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        search = request.QUERY_PARAMS.get('se')    #search
        if search:
            queryset = queryset.filter(Q(title__icontains=search) |
                                Q(desc__icontains=search) )
        return queryset
            
class MarkFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        mark = request.QUERY_PARAMS.get('mark')    #search
        if mark:
            if request.user.is_authenticated():
                queryset = queryset.filter(marks=request.user)
            else:
                queryset = queryset.none()
        return queryset

