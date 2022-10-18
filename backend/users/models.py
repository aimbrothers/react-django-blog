from django.db import models
from django.contrib.auth.models import (
  BaseUserManager, AbstractBaseUser
)


class BackendUserManager(BaseUserManager):
  def create_user(self, email, username, password=None):
    if not email:
      raise ValueError('Users must have an email address')

    if not username:
      raise ValueError('Users must have a username')
    
    user = self.model(
      email=self.normalize_email(email),
      username=username
    )

    user.set_password(password)
    user.save(using=self._db)

    return user

  def create_superuser(self, email, username, password=None):
    user = self.create_user(
      email,
      username,
      password
    )
    user.is_admin = True
    user.save(using=self._db)

    return user


class BackendUser(AbstractBaseUser):
  email = models.EmailField(
    verbose_name='email address',
    max_length=255,
    unique=True
  )
  username = models.CharField(
    max_length=255,
    unique=True
  )
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)

  objects = BackendUserManager()

  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email']

  def __str__(self):
    return self.username

  def has_perm(self, perm, obj=None):
    return True
  
  def has_module_perms(self, app_label):
    return True
  
  @property
  def is_admin(self):
    return self.is_admin