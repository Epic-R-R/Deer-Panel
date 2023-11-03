from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refreshToken": str(refresh),
        "accessToken": str(refresh.access_token),
    }
