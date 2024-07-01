from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.core import validators
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit


User = get_user_model()


class Category(models.Model):
    """Модель категории."""

    name = models.CharField("Название", max_length=200)
    slug = models.SlugField("Slug-имя", max_length=50, unique=True)
    image = models.ImageField(
        upload_to="category/images/", null=True, default=None
    )

    class Meta:
        ordering = ("id",)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.name, self.slug}"


class Subcategory(models.Model):
    """Модель подкатегории."""

    name = models.CharField("Название", max_length=200)
    slug = models.SlugField("Slug-имя", max_length=50, unique=True)
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name="subcategories",
        verbose_name="Категория",
    )
    image = models.ImageField(
        upload_to="subcategory/images/", null=True, default=None
    )

    class Meta:
        ordering = ("id",)
        verbose_name = ("Подкатегория",)
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return f"{self.name, self.slug, self.category}"


class Product(models.Model):
    """Модель продукта."""

    name = models.CharField("Название", max_length=200)
    slug = models.SlugField("Slug-имя", max_length=50, unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
    )
    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Подкатегория",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Цена",
    )
    image = models.ImageField(upload_to="products")
    image_thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFit(100, 50)],
        format="JPEG",
        options={"quality": 60},
    )
    image_medium = ImageSpecField(
        source="image",
        processors=[ResizeToFit(300, 200)],
        format="JPEG",
        options={"quality": 70},
    )
    image_large = ImageSpecField(
        source="image",
        processors=[ResizeToFit(600, 400)],
        format="JPEG",
        options={"quality": 80},
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name}, {self.slug}, {self.subcategory}, {self.price}"


class ShoppingCart(models.Model):
    """Модель корзины."""

    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name="carts",
        verbose_name="Пользователь",
    )

    class Meta:
        ordering = ["user"]
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Корзина пользователя {self.user}"


class CartProduct(models.Model):
    """Модель для вывода количества продукта в корзине."""

    cart = models.ForeignKey(
        ShoppingCart,
        on_delete=models.CASCADE,
        related_name="cart_products",
        verbose_name="Корзина",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_products",
        verbose_name="Продукт",
    )
    amount = models.PositiveIntegerField(
        verbose_name="Количество",
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5000)],
    )

    class Meta:
        ordering = ["cart"]
        verbose_name = "Корзина-товар"
        verbose_name_plural = "Корзина-товары"
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"], name="unique_cart_product"
            )
        ]

    def __str__(self):
        return f"{self.product.name}: {self.amount}"

    @property
    def total_price(self):
        return self.product.price * self.amount
