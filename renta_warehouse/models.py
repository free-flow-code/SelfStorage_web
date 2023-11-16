from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле email обязательно для заполнения')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    username = models.CharField(null=True, blank=True, max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name='Клиент')
    phone_number = PhoneNumberField(verbose_name='Мобильный номер')
    address = models.CharField(verbose_name='Адрес', max_length=200)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.user.username


class WareHouse(models.Model):
    address = models.CharField(verbose_name='Адрес', max_length=200)
    temperature = models.FloatField(verbose_name='Температура')
    height = models.FloatField(verbose_name='Высота')

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return self.address

    def total_boxes(self):
        return self.boxes.count()

    def free_boxes(self):
        occupied_boxes = self.boxes.filter(orders__isnull=False).count()
        return self.total_boxes() - occupied_boxes

    free_boxes.short_description = 'Свободно боксов'
    total_boxes.short_description = 'Всего боксов'


class Box(models.Model):
    number = models.IntegerField(unique=True, verbose_name='Номер бокса')
    warehouse = models.ForeignKey(WareHouse, on_delete=models.CASCADE,  verbose_name='Склад', related_name='boxes')
    floor = models.IntegerField(verbose_name='Этаж')
    length = models.FloatField(verbose_name='Длина')
    width = models.FloatField(verbose_name='Ширина')
    height = models.FloatField(verbose_name='Высота')

    class Meta:
        verbose_name = 'Бокс'
        verbose_name_plural = 'Боксы'

    def __str__(self):
        return f'№ {self.number}'

    def square(self):
        return self.width * self.length

    square.short_description = 'Площадь бокса'


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE,  verbose_name='Клиент', related_name='orders')
    box = models.ForeignKey(Box, on_delete=models.CASCADE,  verbose_name='Бокс на складе', related_name='orders')
    start_rent_date = models.DateTimeField(verbose_name='Дата начала аренды', db_index=True)
    end_rent_date = models.DateTimeField(verbose_name='Дата окончания аренды', db_index=True)
    warehouse_delivery = models.BooleanField(default=False, verbose_name='Доставка на склад')
    from_warehouse_delivery = models.BooleanField(default=False, verbose_name='Доставка со склада')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'ID заказа {self.id}'
