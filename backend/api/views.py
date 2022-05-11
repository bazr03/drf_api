#import json
# from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.forms.models import model_to_dict
from products.models import Product
from products.serializer import ProductSerializer
'''
def api_home(request, *args, **kwargs):
    # request -> HttpRequest -> Django

    # request.body
    print(request.GET) # url query parameters
    body = request.body # byte string of JSON data
    data = {}

    # si no se envia nada de información, body sera un diccionario vacio
    try:
        data = json.loads(body) # string of JSON data -> Python Dict
    except:
        pass

    data['headers'] = dict(request.headers)
    data['params'] = dict(request.GET) # si no hay querys ?key=value en la url, esto sera un diccionario vacio
    data['content_type'] = request.content_type
    print(data)
    return JsonResponse(data)
    '''


# @api_view(["POST"])
# def api_home(request, *args, **kwargs):
#     instance = Product.objects.order_by("?").first()
#     data = {}

#     if instance:
#         # data['id'] = model_data.id
#         # data['title'] = model_data.title
#         # data['content'] = model_data.content
#         # data['price'] = model_data.price
#         # data = model_to_dict(instance, fields=['id', 'title'])
#         data = ProductSerializer(instance).data


#         # SERIALIZATION
#         # model instance (model_data)
#         # turn into a Python dict
#         # return JSON to client

#     return Response(data)

@api_view(["POST"])
def api_home(request, *args, **kwargs):
    
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        instance = serializer.save()
        print(instance)
        
        return Response(serializer.data)

