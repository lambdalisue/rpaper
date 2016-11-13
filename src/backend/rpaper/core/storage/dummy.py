from io import BytesIO
from PIL import Image
from django.core.files.base import File
from django.core.files.storage import Storage


def create_dummy_image(name='test.png', ext='png',
                       size=(50, 50), color=(256, 0, 0)):
    file_obj = BytesIO()
    image = Image.new("RGBA", size=size, color=color)
    image.save(file_obj, ext)
    file_obj.seek(0)
    return File(file_obj, name=name)


class DummyStorage(Storage):
    _dummy_content = None

    def _open(self, name, mode='rb'):
        if self._dummy_content is None:
            self._dummy_content = create_dummy_image(name)
        return self._dummy_content

    def _save(self, name, content):
        self._dummy_content = content

    def delete(self):
        self._dummy_content = None

    def exists(self, name):
        if self._dummy_content and self._dummy_content.name == name:
            return True
        return False

    def size(self):
        return 250

    def url(self):
        return '/dummy/content'
