from django.forms import widgets

class CustomPictureImageFieldWidget(widgets.FileInput):

    def render(self, name, value, attrs=None, **kwargs):
        if value:
            attrs['src'] = value.url
        return super().render(name, value, attrs, **kwargs)