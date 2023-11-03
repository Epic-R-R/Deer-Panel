from rest_framework import serializers
from .models import Client, Traffic, Settings
from rest_framework.validators import UniqueValidator


class UserEditSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=False)
    mobile = serializers.CharField(required=False)
    multiuser = serializers.IntegerField(required=True)
    traffic = serializers.IntegerField(required=True)
    end_date = serializers.DateField(required=False)
    type_traffic = serializers.CharField(required=True)
    status = serializers.CharField(required=True)
    desc = serializers.CharField(required=False)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=Client.objects.all())]
    )
    password = serializers.CharField(required=True)

    class Meta:
        model = Client
        fields = (
            "username",
            "password",
            "email",
            "mobile",
            "multiuser",
            "start_date",
            "end_date",
            "date_one_connect",
            "customer_user",
            "status",
            "traffic",
            "referral",
            "desc",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        instance = self.Meta.model(**validated_data)
        if password:
            instance.password = password
        instance.save()
        Traffic.objects.create(username=instance)
        return instance


class ClientTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class TrafficSerializer(serializers.ModelSerializer):
    class Meta:
        model = Traffic
        fields = "__all__"


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = "__all__"


class ActivateDeactivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["status"]  # Assuming 'status' is the field you're updating

    def update(self, instance, validated_data):
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance
