from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.html import format_html

from core.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    email = models.EmailField(db_index=True, unique=True, verbose_name='Email')
    name = models.CharField(max_length=100, verbose_name='Имя')

    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_superuser = models.BooleanField(default=False, verbose_name='Суперпользователь')
    is_staff = models.BooleanField(default=False, verbose_name='Доступ в админку')

    objects = UserManager()

    class Meta:
        verbose_name = 'пользователя'
        verbose_name_plural = '1. Пользователи'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        if not self.auth_tokens.exists():
            self.auth_tokens.create()
        return result


class Organization(models.Model):
    owner = models.ForeignKey('core.User', related_name='organizations', on_delete=models.CASCADE, verbose_name='Владелец')

    name = models.CharField(max_length=100, verbose_name='Название')
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    class Meta:
        verbose_name = 'организацию'
        verbose_name_plural = '2. Организации'

    def __str__(self):
        return self.name


class WorkPlace(models.Model):
    organization = models.ForeignKey('core.Organization', related_name='work_places', on_delete=models.CASCADE, verbose_name='Организация')
    name = models.CharField(max_length=150, verbose_name='Название')

    class Meta:
        verbose_name = 'рабочее место'
        verbose_name_plural = '3. Рабочие места'

    def __str__(self):
        return f'{self.organization} - {self.name}'


class Post(models.Model):
    organization = models.ForeignKey('core.Organization', related_name='posts', on_delete=models.CASCADE, verbose_name='Организация')
    work_place = models.ForeignKey('core.WorkPlace', related_name='posts', null=True, blank=True, on_delete=models.CASCADE, verbose_name='Рабочее место')

    name = models.CharField(max_length=150, verbose_name='Название')

    class Meta:
        verbose_name = 'должность'
        verbose_name_plural = '4. Должность'

    def __str__(self):
        return f'{self.organization} - {self.name}'


class Person(models.Model):
    STATUS_CHOICES = (
        ('Работает', 'Работает'),
        ('Не работает', 'Не работает'),
        ('В отпуске', 'В отпуске'),
    )

    organization = models.ForeignKey('core.Organization', related_name='persons', on_delete=models.CASCADE, verbose_name='Организация')
    work_place = models.ForeignKey('core.WorkPlace', related_name='persons', on_delete=models.CASCADE, verbose_name='Рабочее место')
    post = models.ForeignKey('core.Post', related_name='persons', on_delete=models.CASCADE, verbose_name='Должность')

    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=150, blank=True, verbose_name='Отчество')

    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')

    birth_date = models.DateField(verbose_name='Дата рождения')

    status = models.CharField(max_length=150, choices=STATUS_CHOICES, verbose_name='Статус в организации')

    comment = models.TextField(blank=True, verbose_name='Комментарий')

    class Meta:
        verbose_name = 'сотрудника'
        verbose_name_plural = '5. Сотрудники'

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'.strip()


class WorkTime(models.Model):
    organization = models.ForeignKey('core.Organization', related_name='work_times', on_delete=models.CASCADE, verbose_name='Организация')
    person = models.ForeignKey(Person, related_name='work_times', on_delete=models.CASCADE)
    start_from = models.DateTimeField(verbose_name='Дата/время начала работы')
    ended_at = models.DateTimeField(verbose_name='Дата/время окончания работы')

    class Meta:
        verbose_name = 'рабочее время'
        verbose_name_plural = '6. Рабочее время'

    def __str__(self):
        return f'{self.person}: {self.start_from} - {self.ended_at})'
