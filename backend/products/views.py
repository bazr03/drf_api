from cgitb import reset
from rest_framework import generics, mixins


from .models import Product
from .serializer import ProductSerializer
#from ..api.permissions import IsStaffEditorPermission
#from api.authentication import TokenAuthentication
from api.mixins import (StaffEditorPermissionMixin, 
                        UserQuerySetMixin)

'''
los serializers para acceder al request necesitan usar self.context.get('request')
las views usan self.request
'''

class ProductListCreateApiView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.ListCreateAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # authentication_classes = [
    #     authentication.SessionAuthentication,
    #     TokenAuthentication
    #     ]
    #permission_classes = [permissions.IsAuthenticated] # solo puedes este endpoint si estas autenticado
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly] # puedes leer (list) pero no usar POST
    #permission_classes = [permissions.DjangoModelPermissions] 

    #permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission] 

    def perform_create(self, serializer): # solo se ejecuta en CreateAPIview o ListCreateAPIView
        # serializer.save(user=self.request.user)
        # print(serializer.validated_data)
        # email = serializer.validated_data.pop('email')
        # print(email)

        # esto se puede hacer en el ProductSerializer, es preferible
        title = serializer.validated_data.get('title')
        content =serializer.validated_data.get('content') or None

        if content is None:
            content = title


        serializer.save(user=self.request.user,content=content)
        # send a signal

    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset(*args, **kwargs)
    #     request = self.request
    #     user = request.user
    #     if not user.is_authenticated:
    #         return Product.objects.none()

    #     #print(request.user)
    #     return qs.filter(user=user)
        


product_list_create_view = ProductListCreateApiView.as_view()


class ProductDetailApiView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.RetrieveAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]
    # lookup_field = 'pk'


product_detail_view = ProductDetailApiView.as_view()


class ProductUpdateApiView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.UpdateAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    #permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]

    def perform_update(self, serializer):
        instance = serializer.save()

        if not instance.content:
            instance.content = instance.title


product_update_view = ProductUpdateApiView.as_view()


class ProductDeleteApiView(
    StaffEditorPermissionMixin,
    generics.DestroyAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    #permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]

    def perform_destroy(self, instance):
        # instance mods
        super().perform_destroy(instance)


product_delete_view = ProductDeleteApiView.as_view()



class ProductMixView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        pk = kwargs.get('pk')

        if pk is not None:
            return self.retrieve(request, *args, **kwargs)

        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer): 
        title   = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None

        if content is None:
            content = 'this is a single view doing cool stuff'
        serializer.save(content=content)
        # send a signal

product_mixin_view = ProductMixView.as_view()


# class ProductListApiView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     # lookup_field = 'pk'


# product_listl_view = ProductListApiView.as_view()