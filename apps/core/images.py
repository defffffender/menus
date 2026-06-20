"""Обработка загружаемых картинок: лимит размера + даунскейл.

Зачем: оригиналы с телефона бывают по 5–10 МБ — это и риск (заполнение диска),
и тормоза у гостя на мобильном. Ужимаем по большей стороне и пережимаем.
"""
from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile

MAX_UPLOAD_MB = 5


def validate_image_size(f, max_mb=MAX_UPLOAD_MB):
    """Отклонить слишком большой файл (вызывать в clean_* формы)."""
    if f is not None and getattr(f, 'size', 0) and f.size > max_mb * 1024 * 1024:
        raise ValidationError(f'Файл больше {max_mb} МБ — загрузите меньше.')


def downscale_field(field, max_px=1100, quality=82):
    """Ужать картинку в поле до max_px по большей стороне (заменяет файл на месте).

    Вызывать только при загрузке нового файла. Молча выходит, если Pillow нет
    или файл не открыть — картинка уже прошла валидацию ImageField.
    """
    if not field:
        return
    try:
        from PIL import Image, ImageOps
    except Exception:
        return
    try:
        field.open()
        img = Image.open(field)
        img = ImageOps.exif_transpose(img)  # учесть поворот из EXIF
        img.load()
    except Exception:
        return

    if max(img.size) <= max_px:
        return  # уже компактная — не пережимаем

    img.thumbnail((max_px, max_px))
    has_alpha = img.mode in ('RGBA', 'LA', 'P')
    buf = BytesIO()
    if has_alpha:
        img.save(buf, format='PNG', optimize=True)
        ext = 'png'
    else:
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img.save(buf, format='JPEG', quality=quality, optimize=True, progressive=True)
        ext = 'jpg'

    base = field.name.rsplit('/', 1)[-1].rsplit('.', 1)[0]
    field.save(f'{base}.{ext}', ContentFile(buf.getvalue()), save=False)
