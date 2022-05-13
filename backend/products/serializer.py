
from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Product
from .validators import validate_title_no_hello, unique_product_title
from api.serializers import UserPublicSerializer

'''
los serializers para acceder al request necesitan usar self.context.get('request')
las views usan self.request
'''


class ProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk',
        read_only=True
        )
    title = serializers.CharField(read_only=True)

'''
ModelSerializer user por default, pero se usa generalmente cuando aplicaremos los métodos
create, update, etc
Serializer es más general y se recomienda cuando son datos públicos generales
'''
class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source='user',read_only=True)
    # my_user_data = serializers.SerializerMethodField(read_only=True)
    # my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    # related_products = ProductInlineSerializer(source='user.product_set.all', read_only=True, many=True)
    # HyperlinkIdenityField solo funciona con ModelSerializer
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk'
        )
    # agregamos write_only xk email no forma parte del 
    # modelo Product
    # email = serializers.EmailField(write_only=True)

    title = serializers.CharField(validators=[validate_title_no_hello, unique_product_title])

    class Meta:
        model = Product
        fields = [
            "owner",
            "url",
            "edit_url",
            "pk",
            "title", 
            "content", 
            "price", 
            "sale_price", 
            #"my_discount",
            #"related_products"
            ]

    # def get_my_user_data(self, obj):
    #     return {
    #         "username": obj.user.username
    #     }

    # def create(self, validated_data):
    #     '''
    #     desde la vista que esa este serializer (ProductSerializer), cuando se llama serializer.save(), si no es una instancia se llama al metodo create, si es una instancia entonces se llama al metodo update
    #     '''
    #     #return Product.objects.create(**validated_data) # esto es lo que se hace por default
    #     # email = validated_data.pop('email')
    #     obj = super().create(validated_data)
    #     # aqui podriamos enviar un email al correo brindado
    #     # print(email, obj)
    #     return obj

    # def update(self, instance, validated_data):
    #     # este es el default
    #     email = validated_data.pop('email')
    #     # aqui tambien podiramos enviar un email con cada actualización
    #     # instance.title = validated_data.get('title')
    #     return super().update(instance, validated_data)

    # def validate_title(self, value):
    #     request = self.context.get('request')
    #     user = request.user
    #     qs = Product.objects.filter(user=user,title__iexact=value)
    #     if qs.exists():
    #         raise serializers.ValidationError(f'{value} is already a product name!')

    #     return value

    def get_edit_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("product-edit", kwargs={"pk": obj.pk },request=request)


    # def get_my_discount(self, obj):
    #     if not hasattr(obj, 'id'):
    #         return None

    #     if not isinstance(obj, Product):
    #         return None

    #     return obj.get_discount()
