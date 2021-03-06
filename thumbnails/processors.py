import io

from django.core.files.base import ContentFile

from da_vinci import images


def resize(image, **kwargs):
    image.resize(width=kwargs['width'], height=kwargs['height'])
    return image


def rotate(image, **kwargs):
    image.rotate(degrees=kwargs['degrees'])
    return image


def flip(image, **kwargs):
    image.flip(direction=kwargs['direction'])
    return image


def crop(image, **kwargs):
    params = {
        'width': kwargs['width'],
        'height': kwargs['height']
    }
    if kwargs.get('center'):
        params['center'] = kwargs['center']
    image.crop(**params)
    return image


def process(file, size):
    """
    Process an image through its defined processors
    params :file: filename or file-like object
    params :size: string for size defined in settings
    return a ContentFile
    """
    from . import conf
    # open image in piccaso
    raw_image = images.from_file(file)

    # run through all processors, if defined
    size_dict = conf.SIZES[size]
    for processor in size_dict.get('processors'):
        raw_image = processor(raw_image, **size_dict)

    # write to Content File
    image_io = io.BytesIO()
    raw_image.save(file=image_io)
    image_file = ContentFile(image_io.getvalue())

    return image_file
