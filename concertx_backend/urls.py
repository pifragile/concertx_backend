from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.auth.models import User
from .models import Concert
from rest_framework import routers, serializers, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from datetime import datetime, timedelta
from pytz import timezone


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class ConcertSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    accepted_by = UserSerializer(many=True, read_only=True)
    canceled_by = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Concert
        fields = ('id', 'location', 'date', 'confirmed', 'owner', 'accepted_by', 'canceled_by')


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user


class ConcertIsInFutureOrReadOnly(BasePermission):
    message = 'Cannot modify concerts that are more than 12 hours in the past.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS and view.action not in ['cancel', 'accept']:
            return True
        return datetime.now(timezone('Europe/Zurich')) - obj.date < timedelta(days=1)


@permission_classes((IsAuthenticated, IsOwnerOrReadOnly, ConcertIsInFutureOrReadOnly))
class ConcertViewSet(viewsets.ModelViewSet):
    queryset = Concert.objects.all()
    serializer_class = ConcertSerializer

    @action(detail=True, methods=['get'])
    def accept(self, request, pk=None):
        concert = self.get_object()
        concert.accepted_by.add(request.user)
        concert.canceled_by.remove(request.user)
        return Response(ConcertSerializer(concert).data)

    @action(detail=True, methods=['get'])
    def cancel(self, request, pk=None):
        concert = self.get_object()
        concert.accepted_by.remove(request.user)
        concert.canceled_by.add(request.user)
        return Response(ConcertSerializer(concert).data)

    def perform_create(self, serializer):
        print(serializer.validated_data)
        user = self.request.user
        serializer.save(owner=user, accepted_by=[user])


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'concerts', ConcertViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^', include(router.urls)),
    re_path(r'^api-auth/', include('rest_framework.urls')),
    re_path(r'^auth/', include('rest_auth.urls'))
]
