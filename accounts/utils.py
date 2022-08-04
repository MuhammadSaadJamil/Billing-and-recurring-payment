from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


def to_base64(data):
    """
    Encode data to base 64
    :param data:
    :return:
    """
    return urlsafe_base64_encode(force_bytes(data))


def decode_base64(base64):
    """
    Decode base 64 data
    :param base64:
    :return:
    """
    return force_str(urlsafe_base64_decode(base64))


class TokenGenerator(PasswordResetTokenGenerator):
    """
    Token generator for account activation link
    """

    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()
