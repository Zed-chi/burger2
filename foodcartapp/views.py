from django.db import transaction
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import (IntegerField, ModelSerializer)

from .models import Order, OrderItem, Product


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
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data

    with transaction.atomic():
        order = Order.objects.create(
            firstname=data["firstname"],
            lastname=data["lastname"],
            phonenumber=data["phonenumber"],
            address=data["address"],
        )

        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product=product_data["product"],
                    quantity=product_data["quantity"],
                    product_price=product_data["product"].price,
                    total_price=product_data["product"].price
                    * product_data["quantity"],
                )
                for product_data in data["products"]
            ],
        )

        serializer = OrderSerializer(order)

        return Response(serializer.data)


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "product",
            "quantity",
        ]


class OrderSerializer(ModelSerializer):
    id = IntegerField(read_only=True)
    products = OrderItemSerializer(
        many=True, allow_empty=False, write_only=True,
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "products",
            "firstname",
            "lastname",
            "phonenumber",
            "address",
        ]
