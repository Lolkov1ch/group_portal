from django.core.exceptions import PermissionDenied
from .models import *

class AbleToUpdateMixin(object):
    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.creator != self.request.user or instance != ProfileModel.Roles.MOD or instance != ProfileModel.Roles.ADMIN:
            raise PermissionDenied('You cant change This! You have no permissions!\n Error 403')
        return super().dispatch(request, *args, **kwargs)
    

class IsAdminMixin(object):
    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance != ProfileModel.Roles.MOD or instance != ProfileModel.Roles.ADMIN:
            raise PermissionDenied('You cant change This! You have no permissions!\n Error 403')
        return super().dispatch(request, *args, **kwargs)