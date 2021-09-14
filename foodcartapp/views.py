import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Order, OrderedProduct, Product


@api_view(["GET"])
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


@api_view(["GET"])
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


@api_view(["POST"])
def register_order(request):
    data = request.data
    try:
        validate_order_data(data)
    except ValueError as e:
        print(e)
        return Response(
            {"message": str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE
        )

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


def validate_order_data(data):
    if not isinstance(data, dict):
        raise ValueError(f"Request data is not json-like")

    for key in ["products", "firstname", "lastname", "phonenumber", "address"]:
        if key not in data.keys():
            raise ValueError(f"There is no {key} key")
        if not data[key]:
            raise ValueError(f"{key} value is falsy")

    if not isinstance(data["products"], list):
        raise ValueError("Products is not list")

    for product in data["products"]:
        validate_order_product(product)

    if not isinstance(data["firstname"], str):
        raise ValueError("firstname is not string")
    if not isinstance(data["lastname"], str):
        raise ValueError("lastname is not string")
    if not isinstance(data["phonenumber"], str):
        raise ValueError("phonenumber is not string")
    if not isinstance(data["address"], str):
        raise ValueError("address is not string")

    return data


def validate_order_product(data):
    for key in data.keys():
        if key not in ["product", "quantity"]:
            raise ValueError(f"wrong {key} key")

    if not isinstance(data["product"], int):
        raise ValueError("product is not integer")
    if not isinstance(data["quantity"], int):
        raise ValueError("quantity is not integer")
