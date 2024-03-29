from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Sum
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from geocache.models import Place

from .utils import get_distance, get_place


class Restaurant(models.Model):
    name = models.CharField("название", max_length=50)
    address = models.CharField(
        "адрес",
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        "контактный телефон",
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = "ресторан"
        verbose_name_plural = "рестораны"

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = RestaurantMenuItem.objects.filter(
            availability=True,
        ).values_list("product")
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField("название", max_length=50)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField("название", max_length=50)
    category = models.ForeignKey(
        ProductCategory,
        verbose_name="категория",
        related_name="products",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        "цена",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    image = models.ImageField("картинка")
    special_status = models.BooleanField(
        "спец.предложение",
        default=False,
        db_index=True,
    )
    description = models.TextField(
        "описание",
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name="menu_items",
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="menu_items",
        verbose_name="продукт",
    )
    availability = models.BooleanField(
        "в продаже",
        default=True,
        db_index=True,
    )

    class Meta:
        verbose_name = "пункт меню ресторана"
        verbose_name_plural = "пункты меню ресторана"
        unique_together = [["restaurant", "product"]]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrderQuerySet(models.QuerySet):
    def with_price(self):
        return self.annotate(price=Sum("items__total_price"))

    def with_available_restaurants(self):
        places = list(Place.objects.all())

        for order in self:
            products = [item.product for item in order.items.all()]
            restaurants_list = []
            for product in products:
                restaurants_list.append(
                    {item.restaurant for item in product.menu_items.all()},
                )
            intersection = restaurants_list[0].intersection(*restaurants_list[1:])
            results = []

            for restaurant in intersection:
                order_place_qs = list(
                    filter(lambda x: x.address == order.address, places)
                )

                restaurant_place_qs = list(
                    filter(
                        lambda x: x.address == restaurant.address,
                        places,
                    )
                )

                if order_place_qs:
                    order_place = order_place_qs[0]
                else:
                    order_place = get_place(order.address)

                if restaurant_place_qs:
                    restaurant_place = restaurant_place_qs[0]
                else:
                    restaurant_place = get_place(restaurant.address)

                distance = get_distance(order_place, restaurant_place)

                results.append({"name": restaurant.name, "dist": distance})

            order.available_in = sorted(results, key=lambda x: x["dist"])
        return self


class Order(models.Model):
    objects = OrderQuerySet.as_manager()
    STATUS_CHOICES = [
        ("Handled", "Обработано"),
        ("Unhandled", "Необработано"),
    ]
    PAYMENT_CHOICES = [
        ("CASH", "Наличными"),
        ("CARD", "Электронно"),
    ]

    firstname = models.CharField("Имя", max_length=30)
    lastname = models.CharField("Фамилия", max_length=50)
    phonenumber = PhoneNumberField("Номер телефона", max_length=32)
    address = models.CharField("Адрес доставки", max_length=100)
    is_processed = models.CharField(
        "Статус заказа",
        choices=STATUS_CHOICES,
        default="Unhandled",
        max_length=30,
    )
    payment = models.CharField(
        "Вид оплаты",
        choices=PAYMENT_CHOICES,
        default="CARD",
        max_length=30,
    )
    comment = models.TextField("Комментарий к заказу", blank=True, default="")
    restaurant = models.ForeignKey(
        Restaurant,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Ресторан отгрузки",
    )

    created_at = models.DateTimeField("Дата создания", default=timezone.now)
    called_at = models.DateTimeField("Дата звонка", null=True, blank=True)
    delivered_at = models.DateTimeField("Дата доставки", null=True, blank=True)

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "заказы"

    def __str__(self):
        return f"Order - {self.phonenumber}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name="Заказ",
        related_name="items",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.DO_NOTHING,
        verbose_name="Товар",
        related_name="order_items",
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Количество",
    )
    product_price = models.DecimalField(
        "Цена товара",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.1)],
    )
    total_price = models.DecimalField(
        "Общая цена",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.1)],
    )

    class Meta:
        verbose_name = "позиция"
        verbose_name_plural = "позиции"

    def __str__(self):
        return f"OrderItem {self.id}"
