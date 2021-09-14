import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Order, OrderedProduct, Product

@api_view(['GET'])
def banners_list_api(request):
    # FIXME move data to db?
    return Response(
        [
            {
                "title": "Burger",
                "src": static("burger.jpg"),
                "text": "Tasty Burger at your door step",
            },
            {
                "title": "Spices",
                "src": static("food.jpg"),
                "text": "All Cuisines",
            },
            {
                "title": "New York",
                "src": static("tasty.jpg"),
                "text": "Food is incomplete without a tasty dessert",
            },
        ],        
    )

@api_view(['GET'])
def product_list_api(request):
    products = Product.objects.select_related("category").available()

    dumped_products = []
    for product in products:
        dumped_product = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "special_status": product.special_status,
            "description": product.description,
            "category": {
                "id": product.category.id,
                "name": product.category.name,
            },
            "image": product.image.url,
            "restaurant": {
                "id": product.id,
                "name": product.name,
            },
        }
        dumped_products.append(dumped_product)
    
    return Response(
        dumped_products,
    )


@api_view(['POST'])
def register_order(request):
    data = request.data
    print(data)

    order = Order.objects.create(
        firstname=data["firstname"],
        lastname=data["lastname"],
        phonenumber=data["phonenumber"],
        address=data["address"],
    )
    try:
        for product_data in data["products"]:
            product = get_object_or_404(Product, id=product_data["product"])
            ordered_product = OrderedProduct.objects.create(
                order=order, product=product, quantity=product_data["quantity"]
            )
    except:
        order.delete()

    return Response({"Message": "order created"})
