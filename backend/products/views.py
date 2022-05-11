from rest_framework import generics, mixins, permissions, authentication


from .models import Product
from .serializer import ProductSerializer
from .permissions import IsStaffEditorPermission
from api.authentication import TokenAuthentication


class ProductListCreateApiView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [
        authentication.SessionAuthentication,
        TokenAuthentication
        ]
    #permission_classes = [permissions.IsAuthenticated] # solo puedes este endpoint si estas autenticado
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly] # puedes leer (list) pero no usar POST
    #permission_classes = [permissions.DjangoModelPermissions] 
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission] 

    def perform_create(self, serializer): # solo se ejecuta en CreateAPIview o ListCreateAPIView
        # serializer.save(user=self.request.user)
        # print(serializer.validated_data)
        title = serializer.validated_data.get('title')
        content =serializer.validated_data.get('content') or None

        if content is None:
            content = title


        serializer.save(content=content)
        # send a signal


product_list_create_view = ProductListCreateApiView.as_view()


class ProductDetailApiView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk'


product_detail_view = ProductDetailApiView.as_view()


class ProductUpdateApiView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.DjangoModelPermissions] 

    def perform_update(self, serializer):
        instance = serializer.save()

        if not instance.content:
            instance.content = instance.title


product_update_view = ProductUpdateApiView.as_view()


class ProductDeleteApiView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

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