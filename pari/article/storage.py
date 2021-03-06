import os
import StringIO

from django.core.files.storage import FileSystemStorage, default_storage

from mezzanine.conf import settings

from filebrowser_safe.storage import FileSystemStorageMixin
import boto
from boto.s3.key import Key
try:
    from PIL import Image, ImageFile, ImageOps
except ImportError:
    import Image
    import ImageFile
    import ImageOps


class ParallelS3Storage(FileSystemStorageMixin, FileSystemStorage):
    def _save(self, name, content):
        if is_s3_storage():
            upload_to_s3(name, in_memory_file=content)
        return super(ParallelS3Storage, self)._save(name, content)


def is_s3_storage():
    return hasattr(settings, 'S3_URL') and settings.S3_URL is not None


def get_s3_bucket():
    conn = boto.connect_s3()
    return conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)


def get_s3_key(key):
    return "/media/%s" % key


def upload_to_s3(key, file_path=None, in_memory_file=None, string_io=None):
    bucket = get_s3_bucket()
    k = Key(bucket)
    k.key = get_s3_key(key)
    if file_path:
        k.set_contents_from_filename(file_path)
    elif in_memory_file:
        k.set_contents_from_string(in_memory_file.read())
    elif string_io:
        k.set_contents_from_string(string_io.getvalue())

    k.make_public()


def key_in_s3(key):
    bucket = get_s3_bucket()
    return Key(bucket, get_s3_key(key)).exists()


def get_s3_content(key, f):
    bucket = get_s3_bucket()
    Key(bucket, get_s3_key(key)).get_file(f)


def is_file_exists(path, url):
    if is_s3_storage():
        return key_in_s3(url)
    return os.path.exists(path)


def create_thumbnail(image_url, thumb_path, thumb_url, width, height, filetype, quality=95):
    try:
        thumb_exists = is_file_exists(thumb_path, thumb_url)
    except UnicodeEncodeError:
        from mezzanine.core.exceptions import FileSystemEncodingChanged
        raise FileSystemEncodingChanged()

    if thumb_exists:
        return thumb_url

    if is_s3_storage():
        f = StringIO.StringIO()
        get_s3_content(image_url, f)
        f.seek(0)
    else:
        try:
            f = default_storage.open(image_url)
        except:
            return image_url

    try:
        image = Image.open(f)
    except:
        return image_url

    image_info = image.info
    width = int(width)
    height = int(height)

    if width == image.size[0] and height == image.size[1]:
        return image_url

    if width == 0:
        width = image.size[0] * height / image.size[1]
    elif height == 0:
        height = image.size[1] * width / image.size[0]
    if image.mode not in ("P", "L", "RGBA"):
        image = image.convert("RGBA")

    # Required for progressive jpgs.
    ImageFile.MAXBLOCK = image.size[0] * image.size[1]

    try:
        image = ImageOps.fit(image, (width, height), Image.ANTIALIAS)
        if is_s3_storage():
            thumb_f = StringIO.StringIO()
            image.save(thumb_f, filetype, quality=quality, **image_info)
            upload_to_s3(thumb_url, string_io=thumb_f)
        else:
            image = image.save(thumb_path, filetype, quality=quality, **image_info)
    except Exception:
        try:
            os.remove(thumb_path)
        except Exception:
            pass
        return image_url

    return thumb_url
