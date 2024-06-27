from django.contrib.auth import get_user_model
from django.core.validators import  MinValueValidator
from django.db import models


User = get_user_model()

ы
def get_upload_path(instance, filename):
    """Получить путь загрузки для изображения."""
    return f"{instance.__class__.__name__.lower()}/{filename}"


class Category(models.Model):
    """Category model."""

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
    """Subcategory model."""

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
    """Product model."""

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

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name}, {self.slug}, {self.subcategory}, {self.price}"

    @property
    def images(self):
        return [self.image, self.image_mid, self.image_mini]


class ShoppingCart(models.Model):
    """Shopping Cart model."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="users",
        verbose_name="Пользователь",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_shopping_cart",
        verbose_name="Товар",
    )

    class Meta:
        ordering = ["product"]
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Товар {self.product} добавлен в корзину и {self.user}"
