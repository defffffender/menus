"""Заполняет БД демо-данными для ручного тестирования.

    python manage.py seed_demo

Идемпотентна: каждый запуск пересоздаёт демо-заведение и его сотрудников
(по маркер-телефонам), остальное (например, ваш суперпользователь) не трогает.
"""
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from PIL import Image, ImageDraw, ImageFont

from apps.accounts.models import User
from apps.menu.models import Category, Dish, DishVariant
from apps.orders.models import Order, OrderItem
from apps.restaurants.models import Membership, Restaurant
from apps.restaurants.utils import unique_slug

OWNER_PHONE = '+998901112233'
STAFF = [
    ('+998901112201', 'Дилшод Менеджеров', Membership.Role.MANAGER),
    ('+998901112202', 'Азиз Официантов', Membership.Role.WAITER),
    ('+998901112203', 'Шеф Поваров', Membership.Role.KITCHEN),
]
DEMO_PHONES = [OWNER_PHONE] + [p for p, _, _ in STAFF]

BRAND = (199, 91, 57)
COLORS = [(199, 91, 57), (224, 160, 77), (62, 92, 74), (138, 110, 74), (160, 80, 60)]


def make_photo(text, color, fname):
    img = Image.new('RGB', (600, 450), color)
    draw = ImageDraw.Draw(img)
    ch = (text or '?').strip()[:1].upper()
    try:
        font = ImageFont.truetype('arial.ttf', 200)
    except OSError:
        font = ImageFont.load_default()
    box = draw.textbbox((0, 0), ch, font=font)
    w, h = box[2] - box[0], box[3] - box[1]
    draw.text(((600 - w) / 2 - box[0], (450 - h) / 2 - box[1]), ch, fill=(255, 255, 255), font=font)
    buf = BytesIO()
    img.save(buf, 'PNG')
    return ContentFile(buf.getvalue(), name=fname)


# категория: (ru, uz, en, [блюда])
# блюдо: (ru, uz, en, desc_ru, weight, spiciness, prep, [(вариант_ru, вариант_uz, вариант_en, цена)])
MENU = [
    ('Салаты', 'Salatlar', 'Salads', [
        ('Ачичук', 'Achichuk', 'Achichuk', 'Помидоры, лук, перец', '200 г', 1, 5,
         [('', '', '', 18000)]),
        ('Цезарь с курицей', 'Tovuqli Sezar', 'Caesar with chicken', 'Курица, пармезан, соус', '250 г', 0, 10,
         [('', '', '', 38000)]),
    ]),
    ('Горячее', 'Issiq taomlar', 'Hot dishes', [
        ('Плов', 'Osh', 'Plov', 'Узбекский плов с говядиной', '300 г', 0, 20,
         [('Обычная', 'Oddiy', 'Regular', 38000), ('Большая', 'Katta', 'Large', 52000)]),
        ('Лагман', 'Lagʻmon', 'Lagman', 'Тянутая лапша с мясом и овощами', '350 г', 1, 15,
         [('', '', '', 34000)]),
        ('Шашлык из баранины', 'Qoʻy shashlik', 'Lamb skewers', 'Маринованная баранина', '1 шт', 2, 18,
         [('1 шампур', '1 six', '1 skewer', 28000), ('Сет 5 шт', '5 dona set', 'Set of 5', 130000)]),
    ]),
    ('Напитки', 'Ichimliklar', 'Drinks', [
        ('Чёрный чай', 'Qora choy', 'Black tea', 'Чайник свежезаваренного чая', '1 л', 0, 3,
         [('Чайник', 'Choynak', 'Pot', 8000)]),
        ('Айран', 'Ayron', 'Ayran', 'Кисломолочный напиток', '0.3 л', 0, 2,
         [('', '', '', 9000)]),
    ]),
]

TABLES = ['Стол 1', 'Стол 2', 'Стол 3', 'Стол 4', 'Топчан 1', 'Топчан 2']


class Command(BaseCommand):
    help = 'Заполняет БД демо-данными для ручного тестирования (идемпотентно).'

    @transaction.atomic
    def handle(self, *args, **options):
        # 1) снести предыдущее демо
        Restaurant.objects.filter(owner__phone=OWNER_PHONE).delete()
        User.objects.filter(phone__in=DEMO_PHONES).delete()

        # 2) владелец + заведение
        owner = User.objects.create(phone=OWNER_PHONE, full_name='Бек Владельцев')
        owner.set_unusable_password()
        owner.save()
        rest = Restaurant.objects.create(
            owner=owner, name='Чайхана Демо', slug=unique_slug('Чайхана Демо'),
            type=Restaurant.Type.CHAIKHANA, city='Ташкент', phone=OWNER_PHONE,
            description_ru='Демо-заведение для тестирования',
            description_uz='Sinov uchun demo muassasa',
            description_en='Demo venue for testing',
        )
        Membership.objects.create(user=owner, restaurant=rest, role=Membership.Role.OWNER)

        # 3) сотрудники
        for phone, name, role in STAFF:
            u = User.objects.create(phone=phone, full_name=name)
            u.set_unusable_password()
            u.save()
            Membership.objects.create(user=u, restaurant=rest, role=role)

        # 4) меню
        dishes_flat = []
        for ci, (cru, cuz, cen, dishes) in enumerate(MENU):
            cat = Category.objects.create(
                restaurant=rest, name_ru=cru, name_uz=cuz, name_en=cen, sort_order=ci,
            )
            for di, (nru, nuz, nen, desc, weight, spicy, prep, variants) in enumerate(dishes):
                color = COLORS[(ci + di) % len(COLORS)]
                dish = Dish.objects.create(
                    category=cat, name_ru=nru, name_uz=nuz, name_en=nen,
                    description_ru=desc, weight=weight, spiciness=spicy, prep_time=prep,
                    sort_order=di, photo=make_photo(nru, color, f'demo_{ci}_{di}.png'),
                )
                for vi, (vru, vuz, ven, price) in enumerate(variants):
                    DishVariant.objects.create(
                        dish=dish, name_ru=vru, name_uz=vuz, name_en=ven,
                        price=price, sort_order=vi,
                    )
                dishes_flat.append(dish)

        # 5) столы
        tables = [
            rest.tables.create(name=name, seats=4, sort_order=i)
            for i, name in enumerate(TABLES)
        ]

        # 6) пара заказов в разных статусах
        def make_order(table, picks, status, comment=''):
            order = Order.objects.create(restaurant=rest, table=table, status=status, comment=comment)
            for dish, qty in picks:
                v = dish.variants.first()
                name = dish.name_ru + (f' · {v.name_ru}' if v.name_ru else '')
                OrderItem.objects.create(order=order, variant=v, name=name, price=v.price, quantity=qty)
            return order

        plov = next(d for d in dishes_flat if d.name_ru == 'Плов')
        lagman = next(d for d in dishes_flat if d.name_ru == 'Лагман')
        tea = next(d for d in dishes_flat if d.name_ru == 'Чёрный чай')
        shashlik = next(d for d in dishes_flat if d.name_ru.startswith('Шашлык'))

        make_order(tables[0], [(plov, 2), (tea, 1)], Order.Status.NEW, 'Без острого, пожалуйста')
        make_order(tables[2], [(lagman, 1), (shashlik, 3)], Order.Status.COOKING)
        make_order(tables[4], [(plov, 1), (tea, 2)], Order.Status.SERVED)

        # итог
        self.stdout.write(self.style.SUCCESS('Демо-данные созданы.'))
        self.stdout.write(f'  Заведение : {rest.name}  (slug: {rest.slug})')
        self.stdout.write(f'  Кабинет   : /cabinet/{rest.slug}/')
        self.stdout.write('  Вход (по SMS-коду, код печатается в консоль сервера):')
        self.stdout.write(f'    Владелец    {OWNER_PHONE}')
        for phone, name, role in STAFF:
            self.stdout.write(f'    {role:<13} {phone}  — {name}')
        first_qr = tables[0].qr_token
        self.stdout.write(f'  Меню гостя : /m/{first_qr}/   (стол «{tables[0].name}»)')
        self.stdout.write(f'  Категорий: {rest.categories.count()}, блюд: {len(dishes_flat)}, '
                          f'столов: {len(tables)}, заказов: {rest.orders.count()}')
