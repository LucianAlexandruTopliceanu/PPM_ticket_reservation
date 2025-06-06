from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

CustomUser = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'phone', 'birth_date', 'is_staff', 'date_joined')
        read_only_fields = ('is_staff', 'date_joined')
        extra_kwargs = {
            'email': {
                'required': True,
                'help_text': "Indirizzo email valido"
            },
            'username': {
                'required': True,
                'help_text': "Obbligatorio. 150 caratteri o meno."
            },
            'phone': {
                'required': False,
                'allow_blank': True
            },
            'birth_date': {
                'required': False,
                'allow_null': True
            }
        }

    def validate_email(self, value):
        value = value.lower()
        if self.instance and CustomUser.objects.filter(email__iexact=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("Un utente con questa email esiste già.")
        return value

    def validate_username(self, value):
        if self.instance and CustomUser.objects.filter(username__iexact=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("Un utente con questo username esiste già.")
        return value


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8,
        max_length=128,
        help_text="La password deve contenere almeno 8 caratteri"
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Conferma la password"
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2', 'phone', 'birth_date')
        extra_kwargs = {
            'email': {'required': True},
            'username': {
                'required': True,
                'help_text': "Obbligatorio. 150 caratteri o meno. Lettere, cifre e @/./+/-/_ solo."
            },
            'phone': {
                'required': False,
                'allow_blank': True
            },
            'birth_date': {
                'required': False,
                'allow_null': True
            }
        }

    def validate_email(self, value):
        value = value.lower()  # Normalizza l'email in lowercase
        if CustomUser.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Un utente con questa email esiste già.")
        return value

    def validate_username(self, value):
        if CustomUser.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError("Un utente con questo username esiste già.")
        return value

    def validate(self, attrs):
        # Validazione password
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Le password non corrispondono."})

        try:
            validate_password(attrs['password'])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})

        # Validazione aggiuntiva per la data di nascita
        if attrs.get('birth_date'):
            from datetime import date
            if attrs['birth_date'] > date.today():
                raise serializers.ValidationError(
                    {"birth_date": "La data di nascita non può essere nel futuro."}
                )

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data.get('phone', ''),
            birth_date=validated_data.get('birth_date')
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Aggiunta claim personalizzati
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Aggiunta dati utente alla risposta
        data['user'] = CustomUserSerializer(self.user).data
        return data


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        min_length=8,
        max_length=128
    )
    new_password2 = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        help_text="Conferma la nuova password"
    )
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Le password non corrispondono."})

        try:
            validate_password(attrs['new_password'])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})

        return attrs