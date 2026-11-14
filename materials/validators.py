from rest_framework.serializers import ValidationError

class UrlValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = dict(value).get(self.field)
        if not url:
            return
        if 'youtube.com' not in url:
            raise ValidationError("Ссылка на ресурс не соответствует правилам")

