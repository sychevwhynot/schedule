from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    
    def get_by_natural_key(self, username):
        return self.get(username=username)
    
    
class CustomUsers(AbstractBaseUser):
    email = models.EmailField('Email', unique=True)
    username = models.CharField('Имя пользователя', max_length=50, unique=True, default='default_username')
    first_name = models.CharField('Имя', max_length=50, blank=True)
    last_name = models.CharField('Фамилия', max_length=50, blank=True)
    superlast_name = models.CharField('Отчество', max_length=50, blank=True)
    is_staff = models.BooleanField('Администратор', default=False)
    is_superuser = models.BooleanField('Суперпользователь', default=False)
    is_active = models.BooleanField('Активный', default=True)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = CustomManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def get_full_name(self):
        return f"{self.last_name} {self.first_name} {self.superlast_name}"
    
    def __str__(self):
        return self.get_full_name()
    
    def has_perm(self, perm, obj=None):
        # Ваша реализация проверки прав доступа
        return True

    def has_module_perms(self, app_label):
        # Ваша реализация проверки прав доступа к модулю
        return self.is_staff

