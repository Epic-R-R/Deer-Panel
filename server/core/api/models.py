from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
class ServerUsers(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, null=True, blank=True)
    mobile = models.CharField(max_length=255, null=True, blank=True)
    multiuser = models.IntegerField()
    start_date = models.CharField(max_length=255, null=True, blank=True)
    end_date = models.CharField(max_length=255, null=True, blank=True)
    date_one_connect = models.CharField(max_length=255, null=True, blank=True)
    customer_user = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    traffic = models.IntegerField()
    referral = models.CharField(max_length=255, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class Traffic(models.Model):
    username = models.ForeignKey(
        "ServerUsers",
        on_delete=models.CASCADE,
        db_column="username",
        to_field="username",
        related_name="traffic_entries",
    )
    download = models.CharField(max_length=255, default=0)
    upload = models.CharField(max_length=255, default=0)
    total = models.CharField(max_length=255, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username.username

    class Meta:
        unique_together = (("username",),)


class Settings(models.Model):
    ssh_port = models.CharField(max_length=255, null=True, blank=True)
    tls_port = models.CharField(max_length=255, null=True, blank=True)
    t_token = models.CharField(max_length=255, null=True, blank=True)
    t_id = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=255, null=True, blank=True)
    multiuser = models.CharField(max_length=255, null=True, blank=True)
    status_multiuser = models.CharField(max_length=255, null=True, blank=True)
    home_url = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Ensure only one instance can be created
        if Settings.objects.exists() and not self.pk:
            raise ValidationError(
                "There is already a settings instance, you can only update it."
            )

    def save(self, *args, **kwargs):
        self.pk = 1
        super(Settings, self).save(*args, **kwargs)

    @staticmethod
    def load():
        if Settings.objects.exists():
            return Settings.objects.get(pk=1)
        else:
            # Set default values when first created
            obj = Settings(
                ssh_port="22",
                tls_port="444",
            )
            obj.save()
            return obj

    def __str__(self):
        return "Settings Instance"
