from dataclasses import field

from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.db import models
import uuid

from django.db.models.signals import post_save


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    site = models.ManyToManyField('Site', default=None)
    email = models.EmailField(max_length=120, default=None, null=True, unique=True)
    name = models.CharField(max_length=240, verbose_name='User Name')
    phone = models.CharField(max_length=10, verbose_name='User Phone')
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    type = models.CharField(max_length=20, null=False, choices=(
        ('Industry', 'Industry'),
        ('Admin', 'Admin'),
        ('Staff', 'Staff')
    ))
    permissions = models.ManyToManyField(Permission, default=None)

    def __str__(self):
        return f'{self.email} since: {self.created_on}'

    @staticmethod
    def new_user_hook(sender, instance, created, **kwargs):
        if created and instance.username != 'AnonymousUser':
            profile = UserProfile.objects.create(user=instance)
            profile.user = instance
            profile.email = instance.email
            if instance.is_superuser:
                sites = Site.objects.select_related()
                profile.site.set(sites)
            profile.name = instance.username
            profile.save()

    @property
    def assigned_sites(self):
        if self.user.is_superuser:
            return Site.objects.all()
        return self.site.all()

    def save(self, *args, **kwargs):
        if not (self.user.is_staff and self.user.is_superuser):
            self.type = 'Industry'
        self.name = str(self.name).title()
        super(UserProfile, self).save(*args, **kwargs)


class River(models.Model):
    name = models.CharField(max_length=256, unique=True, verbose_name="River Name")

    def __str__(self):
        return self.name


class Industry(models.Model):
    name = models.CharField(max_length=256, unique=True, verbose_name="Industry Name")
    type = models.CharField(max_length=120)
    state = models.CharField(max_length=180, verbose_name='State', null=True)
    city = models.CharField(max_length=180, verbose_name='City', null=True)
    address = models.TextField(default=None, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, null=True, on_delete=models.SET_NULL, blank=True)

    def __str__(self):
        return self.name

class Site(models.Model):
    name = models.CharField(max_length=240, verbose_name='Site Name')
    prefix = models.CharField(max_length=120, verbose_name='Site Prefix', unique=True)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, verbose_name='Industry')
    river = models.ForeignKey(River, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='River')
    state = models.CharField(max_length=180, verbose_name='State', null=True)
    city = models.CharField(max_length=180, verbose_name='City', null=True)
    address = models.TextField(default=None, null=True, blank=True)
    longitude = models.DecimalField(decimal_places=15, max_digits=20, null=True, blank=True)
    latitude = models.DecimalField(decimal_places=15, max_digits=20, null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=(
            ('Live', 'Live'),
            ('Offline', 'Offline'),
            ('Delay', 'Delay')
        ),
        default='Offline'
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}: {self.status}'


class Readings(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(db_index=True)
    reading = models.TextField()
    class Meta:
        unique_together = (('timestamp', 'site'),)

    def __str__(self):
        return f'{self.site.industry.name}: {self.site.name}: {self.timestamp}'


class SiteInfo(models.Model):
    site = models.OneToOneField(Site, primary_key=True, on_delete=models.CASCADE)
    last_seen = models.DateTimeField(auto_now_add=True, null=True)
    reading = models.TextField()
    timestamp = models.DateTimeField(db_index=True)

    def __str__(self):
        return f'{self.site.name}: {self.reading}'


post_save.connect(UserProfile.new_user_hook, sender=User)


class ExceedanceReports(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, verbose_name="Site")
    min = models.DecimalField(max_digits=5, decimal_places=2)
    max = models.DecimalField(max_digits=5, decimal_places=2)
    parameter = models.CharField(max_length=16)
    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Parameter Value')
    timestamp = models.DateTimeField(verbose_name='reading time')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="received time")

    class Meta:
        verbose_name = "Exceedance"
        verbose_name_plural = "Exceedances"
        unique_together = ('site', 'timestamp', 'parameter')
        indexes = [
            models.Index(fields=['site', 'timestamp']),
        ]

class Parameters(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='parameters')
    name = models.CharField(max_length=120)
    min = models.FloatField(default=0)
    max = models.FloatField(default=0)
    unit = models.CharField(max_length=8, blank=True, null=True)
    class Meta:
        unique_together = ('site', 'name')

    def __str__(self):
        return f"{self.name} from {self.site}"