#import json
from django.http import JsonResponse

from products.models import Product

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
def api_home(requste, *args, **kwargs):
    model_data = Product.objects.order_by("?").first()
    data = {}

    if model_data:
        data['id'] = model_data.id
        data['title'] = model_data.title
        data['content'] = model_data.content
        data['price'] = model_data.price

    return JsonResponse(data)
