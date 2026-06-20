"""Лёгкая мультиязычность интерфейса (ru/uz/en) без gettext-тулчейна.

Строки интерфейса (chrome) храним здесь. Контент заведений (меню, описания)
переводится через поля моделей `*_ru/_uz/_en` — это другое.
"""

LANGUAGES = (('ru', 'RU'), ('uz', 'UZ'), ('en', 'EN'))
DEFAULT_LANG = 'ru'

# ключи — валидные идентификаторы, чтобы работало {{ t.key }} в шаблонах
TR = {
    # nav / общее
    'nav_login':        {'ru': 'Войти', 'uz': 'Kirish', 'en': 'Log in'},
    'nav_start':        {'ru': 'Начать бесплатно', 'uz': 'Bepul boshlash', 'en': 'Start free'},

    # регистрация
    'reg_title':        {'ru': 'Регистрация заведения', 'uz': 'Muassasani roʻyxatdan oʻtkazish', 'en': 'Register your venue'},
    'reg_name':         {'ru': 'Название заведения', 'uz': 'Muassasa nomi', 'en': 'Venue name'},
    'reg_type':         {'ru': 'Тип заведения', 'uz': 'Muassasa turi', 'en': 'Venue type'},
    'reg_city':         {'ru': 'Город', 'uz': 'Shahar', 'en': 'City'},
    'reg_phone':        {'ru': 'Телефон', 'uz': 'Telefon', 'en': 'Phone'},
    'reg_submit':       {'ru': 'Получить код', 'uz': 'Kod olish', 'en': 'Get code'},
    'reg_have_account': {'ru': 'Уже есть аккаунт?', 'uz': 'Hisobingiz bormi?', 'en': 'Already have an account?'},

    # типы заведений
    'type_restaurant':  {'ru': 'Ресторан', 'uz': 'Restoran', 'en': 'Restaurant'},
    'type_cafe':        {'ru': 'Кафе', 'uz': 'Kafe', 'en': 'Cafe'},
    'type_chaikhana':   {'ru': 'Чайхана', 'uz': 'Choyxona', 'en': 'Chaikhana'},
    'type_fastfood':    {'ru': 'Фастфуд', 'uz': 'Fastfud', 'en': 'Fast food'},

    # подтверждение кода
    'verify_title':     {'ru': 'Введите код из SMS', 'uz': 'SMS dagi kodni kiriting', 'en': 'Enter the SMS code'},
    'verify_sent':      {'ru': 'Мы отправили код на номер', 'uz': 'Kod yuborilgan raqam', 'en': 'We sent a code to'},
    'verify_code':      {'ru': 'Код подтверждения', 'uz': 'Tasdiqlash kodi', 'en': 'Confirmation code'},
    'verify_submit':    {'ru': 'Подтвердить', 'uz': 'Tasdiqlash', 'en': 'Confirm'},
    'verify_resend':    {'ru': 'Отправить код повторно', 'uz': 'Kodni qayta yuborish', 'en': 'Resend code'},
    'verify_resend_in': {'ru': 'Повторная отправка через', 'uz': 'Qayta yuborish', 'en': 'Resend available in'},
    'verify_sec':       {'ru': 'сек', 'uz': 'son.', 'en': 'sec'},

    # вход
    'login_title':      {'ru': 'Вход', 'uz': 'Kirish', 'en': 'Log in'},
    'login_submit':     {'ru': 'Получить код', 'uz': 'Kod olish', 'en': 'Get code'},
    'login_no_account': {'ru': 'Нет аккаунта?', 'uz': 'Hisob yoʻqmi?', 'en': 'No account?'},
    'login_register':   {'ru': 'Зарегистрировать заведение', 'uz': 'Muassasani roʻyxatdan oʻtkazish', 'en': 'Register a venue'},

    # кабинет
    'cab_title':        {'ru': 'Кабинет', 'uz': 'Kabinet', 'en': 'Dashboard'},
    'cab_welcome':      {'ru': 'Добро пожаловать', 'uz': 'Xush kelibsiz', 'en': 'Welcome'},
    'cab_your_venues':  {'ru': 'Ваши заведения', 'uz': 'Sizning muassasalaringiz', 'en': 'Your venues'},
    'cab_role':         {'ru': 'Роль', 'uz': 'Rol', 'en': 'Role'},
    'cab_logout':       {'ru': 'Выйти', 'uz': 'Chiqish', 'en': 'Log out'},
    'cab_empty':        {'ru': 'У вас пока нет заведений', 'uz': 'Hozircha muassasalaringiz yoʻq', 'en': 'You have no venues yet'},

    # кабинет: навигация
    'nav_dashboard':    {'ru': 'Дашборд', 'uz': 'Boshqaruv paneli', 'en': 'Dashboard'},
    'nav_menu':         {'ru': 'Меню', 'uz': 'Menyu', 'en': 'Menu'},
    'nav_orders':       {'ru': 'Заказы', 'uz': 'Buyurtmalar', 'en': 'Orders'},
    'nav_tables':       {'ru': 'Столы', 'uz': 'Stollar', 'en': 'Tables'},
    'nav_qr':           {'ru': 'QR-коды', 'uz': 'QR-kodlar', 'en': 'QR codes'},
    'nav_analytics':    {'ru': 'Аналитика', 'uz': 'Tahlil', 'en': 'Analytics'},
    'nav_settings':     {'ru': 'Настройки', 'uz': 'Sozlamalar', 'en': 'Settings'},
    'nav_design':       {'ru': 'Дизайн меню', 'uz': 'Menyu dizayni', 'en': 'Menu design'},
    'soon':             {'ru': 'скоро', 'uz': 'tez orada', 'en': 'soon'},

    # дашборд
    'dash_title':       {'ru': 'Дашборд', 'uz': 'Boshqaruv paneli', 'en': 'Dashboard'},
    'dash_tables':      {'ru': 'Столов', 'uz': 'Stollar', 'en': 'Tables'},
    'dash_manage_menu': {'ru': 'Управлять меню', 'uz': 'Menyuni boshqarish', 'en': 'Manage menu'},

    # столы
    'tables_title':     {'ru': 'Столы', 'uz': 'Stollar', 'en': 'Tables'},
    'tables_subtitle':  {'ru': 'Добавьте столы — для каждого создаётся свой QR', 'uz': 'Stollar qoʻshing — har biriga QR yaratiladi', 'en': 'Add tables — each gets its own QR'},
    'tables_add':       {'ru': 'Добавить стол', 'uz': 'Stol qoʻshish', 'en': 'Add table'},
    'tables_save':      {'ru': 'Сохранить', 'uz': 'Saqlash', 'en': 'Save'},
    'tables_cancel':    {'ru': 'Отмена', 'uz': 'Bekor qilish', 'en': 'Cancel'},
    'tables_edit':      {'ru': 'Редактировать', 'uz': 'Tahrirlash', 'en': 'Edit'},
    'tables_delete':    {'ru': 'Удалить', 'uz': 'Oʻchirish', 'en': 'Delete'},
    'tables_name':      {'ru': 'Название/номер', 'uz': 'Nomi/raqami', 'en': 'Name/number'},
    'tables_seats':     {'ru': 'Мест', 'uz': 'Joylar', 'en': 'Seats'},
    'tables_empty':     {'ru': 'Столов пока нет', 'uz': 'Hozircha stollar yoʻq', 'en': 'No tables yet'},
    'tables_qr':        {'ru': 'QR', 'uz': 'QR', 'en': 'QR'},
    'tables_delete_confirm': {'ru': 'Удалить стол?', 'uz': 'Stol oʻchirilsinmi?', 'en': 'Delete table?'},
    'tables_assign':    {'ru': 'Официанты', 'uz': 'Ofitsiantlar', 'en': 'Waiters'},
    'tables_waiters_hint': {'ru': 'Закрепите официантов — они будут видеть и вести заказы только этого стола. Если никого не отметить, заказы стола видны всем.', 'uz': 'Ofitsiantlarni biriktiring — ular faqat shu stol buyurtmalarini koʻradi va yuritadi. Hech kim belgilanmasa, stol buyurtmalari hammaga koʻrinadi.', 'en': 'Assign waiters — they will see and handle orders for this table only. If none are selected, the table’s orders are visible to everyone.'},
    'tables_waiters_saved': {'ru': 'Официанты стола обновлены', 'uz': 'Stol ofitsiantlari yangilandi', 'en': 'Table waiters updated'},
    'tables_zone':      {'ru': 'Зона', 'uz': 'Zona', 'en': 'Zone'},
    'tables_zone_none': {'ru': '— Без зоны —', 'uz': '— Zonasiz —', 'en': '— No zone —'},

    # зоны / секции столов
    'zones_label':      {'ru': 'Зоны', 'uz': 'Zonalar', 'en': 'Zones'},
    'zones_hint':       {'ru': 'Этажи, залы, улица, терраса — сгруппируйте столы по зонам', 'uz': 'Qavatlar, zallar, koʻcha, terrassa — stollarni zonalarga ajrating', 'en': 'Floors, halls, street, terrace — group tables into zones'},
    'zone_add':         {'ru': 'Добавить зону', 'uz': 'Zona qoʻshish', 'en': 'Add zone'},
    'zone_name':        {'ru': 'Название зоны', 'uz': 'Zona nomi', 'en': 'Zone name'},
    'zone_name_ph':     {'ru': '2 этаж / Улица / VIP-зал', 'uz': '2-qavat / Koʻcha / VIP-zal', 'en': '2nd floor / Street / VIP hall'},
    'zone_none':        {'ru': 'Без зоны', 'uz': 'Zonasiz', 'en': 'No zone'},
    'zone_created':     {'ru': 'Зона создана', 'uz': 'Zona yaratildi', 'en': 'Zone created'},
    'zone_deleted':     {'ru': 'Зона удалена', 'uz': 'Zona oʻchirildi', 'en': 'Zone deleted'},
    'zone_delete_confirm': {'ru': 'Удалить зону? Столы останутся (станут без зоны).', 'uz': 'Zona oʻchirilsinmi? Stollar qoladi (zonasiz boʻladi).', 'en': 'Delete zone? Tables remain (become unzoned).'},
    'zone_empty':       {'ru': 'Зон пока нет', 'uz': 'Hozircha zonalar yoʻq', 'en': 'No zones yet'},
    'zone_rename':      {'ru': 'Переименовать', 'uz': 'Nomini oʻzgartirish', 'en': 'Rename'},

    # qr
    'qr_title':         {'ru': 'QR-коды столов', 'uz': 'Stollar QR-kodlari', 'en': 'Table QR codes'},
    'qr_subtitle':      {'ru': 'Распечатайте и поставьте на столы', 'uz': 'Chop eting va stollarga qoʻying', 'en': 'Print and place on tables'},
    'qr_print':         {'ru': 'Печать', 'uz': 'Chop etish', 'en': 'Print'},
    'qr_scan':          {'ru': 'Сканируйте, чтобы открыть меню', 'uz': 'Menyuni ochish uchun skanerlang', 'en': 'Scan to open the menu'},
    'qr_empty':         {'ru': 'Сначала добавьте столы', 'uz': 'Avval stollar qoʻshing', 'en': 'Add tables first'},

    # меню (кабинет)
    'menu_title':       {'ru': 'Меню', 'uz': 'Menyu', 'en': 'Menu'},
    'menu_subtitle':    {'ru': 'Категории, блюда, варианты и цены', 'uz': 'Kategoriyalar, taomlar, variantlar va narxlar', 'en': 'Categories, dishes, variants and prices'},
    'menu_add_dish':    {'ru': 'Добавить блюдо', 'uz': 'Taom qoʻshish', 'en': 'Add dish'},
    'menu_add_category': {'ru': 'Добавить категорию', 'uz': 'Kategoriya qoʻshish', 'en': 'Add category'},
    'menu_categories':  {'ru': 'Категории', 'uz': 'Kategoriyalar', 'en': 'Categories'},
    'menu_no_categories': {'ru': 'Сначала создайте категорию', 'uz': 'Avval kategoriya yarating', 'en': 'Create a category first'},
    'menu_no_dishes':   {'ru': 'В этой категории пока нет блюд', 'uz': 'Bu kategoriyada hozircha taom yoʻq', 'en': 'No dishes in this category yet'},
    'menu_empty':       {'ru': 'Меню пустое — добавьте категорию и блюда', 'uz': 'Menyu boʻsh — kategoriya va taom qoʻshing', 'en': 'Menu is empty — add a category and dishes'},
    'menu_search_ph':   {'ru': 'Поиск блюд…', 'uz': 'Taomlarni qidirish…', 'en': 'Search dishes…'},
    'menu_search_empty': {'ru': 'Ничего не найдено по запросу', 'uz': 'Soʻrov boʻyicha hech narsa topilmadi', 'en': 'Nothing found for'},
    'menu_in_stock':    {'ru': 'В наличии', 'uz': 'Mavjud', 'en': 'In stock'},
    'menu_stop':        {'ru': 'Стоп', 'uz': 'Toʻxtatilgan', 'en': 'Stop'},
    'menu_from':        {'ru': 'от', 'uz': 'dan', 'en': 'from'},
    'menu_som':         {'ru': 'сум', 'uz': 'soʻm', 'en': 'soʻm'},
    'menu_edit':        {'ru': 'Редактировать', 'uz': 'Tahrirlash', 'en': 'Edit'},
    'menu_delete':      {'ru': 'Удалить', 'uz': 'Oʻchirish', 'en': 'Delete'},
    'menu_save':        {'ru': 'Сохранить', 'uz': 'Saqlash', 'en': 'Save'},
    'menu_cancel':      {'ru': 'Отмена', 'uz': 'Bekor qilish', 'en': 'Cancel'},
    'menu_back':        {'ru': '← К меню', 'uz': '← Menyuga', 'en': '← Back to menu'},
    'menu_collapse':    {'ru': 'Свернуть', 'uz': 'Yigʻish', 'en': 'Collapse'},
    'menu_expand':      {'ru': 'Развернуть', 'uz': 'Yoyish', 'en': 'Expand'},
    'menu_add_dish_here': {'ru': 'Добавить блюдо', 'uz': 'Taom qoʻshish', 'en': 'Add dish'},
    'menu_cat_created': {'ru': 'Категория создана', 'uz': 'Kategoriya yaratildi', 'en': 'Category created'},
    'menu_dish_created': {'ru': 'Блюдо добавлено', 'uz': 'Taom qoʻshildi', 'en': 'Dish added'},
    'menu_saved':       {'ru': 'Сохранено', 'uz': 'Saqlandi', 'en': 'Saved'},
    'menu_deleted':     {'ru': 'Удалено', 'uz': 'Oʻchirildi', 'en': 'Deleted'},
    'menu_need_price':  {'ru': 'Укажите хотя бы одну цену', 'uz': 'Kamida bitta narx kiriting', 'en': 'Enter at least one price'},

    # форма блюда
    'dish_new':         {'ru': 'Новое блюдо', 'uz': 'Yangi taom', 'en': 'New dish'},
    'dish_edit_title':  {'ru': 'Редактировать блюдо', 'uz': 'Taomni tahrirlash', 'en': 'Edit dish'},
    'dish_photo':       {'ru': 'Фото блюда', 'uz': 'Taom surati', 'en': 'Dish photo'},
    'dish_photo_hint':  {'ru': 'Обязательно · до 5 МБ', 'uz': 'Majburiy · 5 MB gacha', 'en': 'Required · up to 5 MB'},
    'dish_name':        {'ru': 'Название', 'uz': 'Nomi', 'en': 'Name'},
    'dish_description':  {'ru': 'Описание', 'uz': 'Tavsif', 'en': 'Description'},
    'dish_category':    {'ru': 'Категория', 'uz': 'Kategoriya', 'en': 'Category'},
    'dish_weight':      {'ru': 'Вес/объём', 'uz': 'Vazn/hajm', 'en': 'Weight/volume'},
    'dish_spiciness':   {'ru': 'Острота', 'uz': 'Achchiqligi', 'en': 'Spiciness'},
    'dish_prep_time':   {'ru': 'Время (мин)', 'uz': 'Vaqt (daq)', 'en': 'Time (min)'},
    'dish_available':   {'ru': 'В наличии', 'uz': 'Mavjud', 'en': 'In stock'},
    'dish_variants':    {'ru': 'Варианты и цены', 'uz': 'Variantlar va narxlar', 'en': 'Variants and prices'},
    'dish_variants_hint': {'ru': 'Один вариант — обычное блюдо. Несколько — размеры.', 'uz': 'Bitta variant — oddiy taom. Bir nechta — oʻlchamlar.', 'en': 'One variant — a regular dish. Several — sizes.'},
    'dish_variant_name': {'ru': 'Вариант (напр. Большая)', 'uz': 'Variant (mas. Katta)', 'en': 'Variant (e.g. Large)'},
    'dish_price':       {'ru': 'Цена', 'uz': 'Narx', 'en': 'Price'},
    'dish_add_variant': {'ru': '+ Добавить вариант', 'uz': '+ Variant qoʻshish', 'en': '+ Add variant'},
    'dish_delete_confirm': {'ru': 'Удалить блюдо?', 'uz': 'Taom oʻchirilsinmi?', 'en': 'Delete dish?'},
    'cat_delete_confirm': {'ru': 'Удалить категорию со всеми блюдами?', 'uz': 'Kategoriya barcha taomlari bilan oʻchirilsinmi?', 'en': 'Delete category with all dishes?'},

    # острота (значения)
    'spicy_0':          {'ru': 'Не острое', 'uz': 'Achchiq emas', 'en': 'Not spicy'},
    'spicy_1':          {'ru': 'Слабо острое', 'uz': 'Engil achchiq', 'en': 'Mild'},
    'spicy_2':          {'ru': 'Острое', 'uz': 'Achchiq', 'en': 'Spicy'},
    'spicy_3':          {'ru': 'Очень острое', 'uz': 'Juda achchiq', 'en': 'Very spicy'},

    # публичное меню (заглушка)
    'stub_soon':        {'ru': 'Меню скоро появится', 'uz': 'Menyu tez orada', 'en': 'Menu coming soon'},
    'stub_table':       {'ru': 'Стол', 'uz': 'Stol', 'en': 'Table'},

    # публичное меню гостя
    'pub_table':        {'ru': 'Стол', 'uz': 'Stol', 'en': 'Table'},
    'pub_som':          {'ru': 'сум', 'uz': 'soʻm', 'en': 'soʻm'},
    'pub_add':          {'ru': 'Добавить', 'uz': 'Qoʻshish', 'en': 'Add'},
    'pub_stop':         {'ru': 'Нет в наличии', 'uz': 'Mavjud emas', 'en': 'Out of stock'},
    'pub_empty':        {'ru': 'Меню пока пустое', 'uz': 'Menyu hozircha boʻsh', 'en': 'The menu is empty for now'},
    'pub_cart':         {'ru': 'Корзина', 'uz': 'Savat', 'en': 'Cart'},
    'pub_your_order':   {'ru': 'Ваш заказ', 'uz': 'Buyurtmangiz', 'en': 'Your order'},
    'pub_cart_empty':   {'ru': 'Корзина пуста', 'uz': 'Savat boʻsh', 'en': 'Your cart is empty'},
    'pub_total':        {'ru': 'Итого', 'uz': 'Jami', 'en': 'Total'},
    'pub_comment':      {'ru': 'Комментарий к заказу', 'uz': 'Buyurtmaga izoh', 'en': 'Order comment'},
    'pub_comment_ph':   {'ru': 'Без лука, побыстрее…', 'uz': 'Piyozsiz, tezroq…', 'en': 'No onion, faster…'},
    'pub_send':         {'ru': 'Отправить заказ', 'uz': 'Buyurtmani yuborish', 'en': 'Send order'},
    'pub_order_error':  {'ru': 'Не удалось отправить заказ, попробуйте ещё раз', 'uz': 'Buyurtma yuborilmadi, qayta urinib koʻring', 'en': 'Could not send the order, please try again'},
    'pub_table_closed': {'ru': 'Стол закрыт. Обновите страницу или позовите официанта.', 'uz': 'Stol yopilgan. Sahifani yangilang yoki ofitsiantni chaqiring.', 'en': 'The table is closed. Refresh the page or call a waiter.'},
    'pub_checkout':     {'ru': 'Оформить', 'uz': 'Rasmiylashtirish', 'en': 'Checkout'},
    'pub_clear':        {'ru': 'Очистить', 'uz': 'Tozalash', 'en': 'Clear'},
    'pub_items':        {'ru': 'поз.', 'uz': 'ta', 'en': 'items'},

    # роли (трёхъязычно)
    'role_owner':         {'ru': 'Владелец', 'uz': 'Egasi', 'en': 'Owner'},
    'role_director':      {'ru': 'Директор', 'uz': 'Direktor', 'en': 'Director'},
    'role_administrator': {'ru': 'Управляющий', 'uz': 'Boshqaruvchi', 'en': 'Administrator'},
    'role_manager':       {'ru': 'Менеджер', 'uz': 'Menejer', 'en': 'Manager'},
    'role_waiter':        {'ru': 'Официант', 'uz': 'Ofitsiant', 'en': 'Waiter'},
    'role_kitchen':       {'ru': 'Кухня', 'uz': 'Oshxona', 'en': 'Kitchen'},

    # сотрудники
    'nav_staff':        {'ru': 'Сотрудники', 'uz': 'Xodimlar', 'en': 'Staff'},
    'staff_title':      {'ru': 'Сотрудники', 'uz': 'Xodimlar', 'en': 'Staff'},
    'staff_subtitle':   {'ru': 'Пригласите сотрудников и назначьте роли', 'uz': 'Xodimlarni taklif qiling va rol bering', 'en': 'Invite staff and assign roles'},
    'staff_invite':     {'ru': 'Пригласить сотрудника', 'uz': 'Xodim taklif qilish', 'en': 'Invite a staff member'},
    'staff_phone':      {'ru': 'Телефон (+998…)', 'uz': 'Telefon (+998…)', 'en': 'Phone (+998…)'},
    'staff_name':       {'ru': 'Имя (необязательно)', 'uz': 'Ism (ixtiyoriy)', 'en': 'Name (optional)'},
    'staff_role':       {'ru': 'Роль', 'uz': 'Rol', 'en': 'Role'},
    'staff_add':        {'ru': 'Пригласить', 'uz': 'Taklif qilish', 'en': 'Invite'},
    'staff_hint':       {'ru': 'Сотрудник войдёт по этому номеру через SMS-код.', 'uz': 'Xodim shu raqam orqali SMS-kod bilan kiradi.', 'en': 'The staff member logs in with this number via SMS code.'},
    'staff_you':        {'ru': 'это вы', 'uz': 'bu siz', 'en': 'you'},
    'staff_member':     {'ru': 'Сотрудник', 'uz': 'Xodim', 'en': 'Member'},
    'staff_change':     {'ru': 'Сменить роль', 'uz': 'Rolni almashtirish', 'en': 'Change role'},
    'staff_remove':     {'ru': 'Убрать', 'uz': 'Olib tashlash', 'en': 'Remove'},
    'staff_remove_confirm': {'ru': 'Убрать сотрудника из заведения?', 'uz': 'Xodim muassasadan olib tashlansinmi?', 'en': 'Remove this member from the venue?'},
    'staff_empty':      {'ru': 'Пока только вы', 'uz': 'Hozircha faqat siz', 'en': 'Just you so far'},
    'staff_no_assign':  {'ru': 'У вашей роли нет права приглашать сотрудников', 'uz': 'Sizning rolingizda xodim taklif qilish huquqi yoʻq', 'en': 'Your role cannot invite staff'},
    'staff_added':      {'ru': 'Сотрудник добавлен', 'uz': 'Xodim qoʻshildi', 'en': 'Member added'},
    'staff_err_phone':  {'ru': 'Введите корректный телефон', 'uz': 'Toʻgʻri telefon kiriting', 'en': 'Enter a valid phone'},
    'staff_err_role':   {'ru': 'Недопустимая роль', 'uz': 'Notoʻgʻri rol', 'en': 'Invalid role'},
    'staff_err_exists': {'ru': 'Этот сотрудник уже в заведении', 'uz': 'Bu xodim allaqachon muassasada', 'en': 'This member is already in the venue'},
    'staff_venue':      {'ru': 'Заведение', 'uz': 'Muassasa', 'en': 'Venue'},
    'staff_venues':     {'ru': 'Заведения', 'uz': 'Muassasalar', 'en': 'Venues'},
    'staff_venues_hint': {'ru': 'Отметьте, куда добавить сотрудника', 'uz': 'Xodimni qayerga qoʻshishni belgilang', 'en': 'Choose where to add the member'},
    'staff_err_venue':  {'ru': 'Нет прав привязывать сотрудников к этому заведению', 'uz': 'Bu muassasaga xodim biriktirishga ruxsat yoʻq', 'en': 'You cannot assign staff to this venue'},
    'staff_err_no_venue': {'ru': 'Выберите хотя бы одно заведение', 'uz': 'Kamida bitta muassasa tanlang', 'en': 'Select at least one venue'},
    'staff_added_n':    {'ru': 'Добавлено в заведений', 'uz': 'Muassasaga qoʻshildi', 'en': 'Added to venues'},

    # дизайн меню
    'design_title':     {'ru': 'Дизайн меню', 'uz': 'Menyu dizayni', 'en': 'Menu design'},
    'design_subtitle':  {'ru': 'Оформление гостевого меню — меняется вживую справа', 'uz': 'Mehmon menyusi koʻrinishi — oʻngda jonli oʻzgaradi', 'en': 'Guest menu look — updates live on the right'},
    'design_save':      {'ru': 'Сохранить дизайн', 'uz': 'Dizaynni saqlash', 'en': 'Save design'},
    'design_saved':     {'ru': 'Дизайн сохранён', 'uz': 'Dizayn saqlandi', 'en': 'Design saved'},
    'design_presets':   {'ru': 'Готовые темы', 'uz': 'Tayyor mavzular', 'en': 'Presets'},
    'design_colors':    {'ru': 'Цвета', 'uz': 'Ranglar', 'en': 'Colors'},
    'design_c_accent':  {'ru': 'Акцент', 'uz': 'Urgʻu', 'en': 'Accent'},
    'design_c_bg':      {'ru': 'Фон', 'uz': 'Fon', 'en': 'Background'},
    'design_c_text':    {'ru': 'Текст', 'uz': 'Matn', 'en': 'Text'},
    'design_c_card':    {'ru': 'Карточки', 'uz': 'Kartochkalar', 'en': 'Cards'},
    'design_font':      {'ru': 'Шрифт', 'uz': 'Shrift', 'en': 'Font'},
    'design_cards':     {'ru': 'Карточки блюд', 'uz': 'Taom kartochkalari', 'en': 'Dish cards'},
    'design_card_list': {'ru': 'Список', 'uz': 'Roʻyxat', 'en': 'List'},
    'design_card_grid': {'ru': 'Плитка', 'uz': 'Plitka', 'en': 'Grid'},
    'design_card_compact': {'ru': 'Компактно', 'uz': 'Ixcham', 'en': 'Compact'},
    'design_radius':    {'ru': 'Скругление углов', 'uz': 'Burchak yumaloqligi', 'en': 'Corner radius'},
    'design_show_desc': {'ru': 'Показывать описания блюд', 'uz': 'Taom tavsiflarini koʻrsatish', 'en': 'Show dish descriptions'},
    'design_header':    {'ru': 'Шапка и логотип', 'uz': 'Sarlavha va logotip', 'en': 'Header & logo'},
    'design_show_logo': {'ru': 'Логотип в шапке', 'uz': 'Sarlavhada logotip', 'en': 'Logo in header'},
    'design_no_logo':   {'ru': 'Логотип не загружен — добавьте его в Настройках', 'uz': 'Logotip yuklanmagan — Sozlamalarda qoʻshing', 'en': 'No logo uploaded — add it in Settings'},
    'design_h_left':    {'ru': 'Слева', 'uz': 'Chapda', 'en': 'Left'},
    'design_h_center':  {'ru': 'По центру', 'uz': 'Markazda', 'en': 'Center'},
    'design_cover':     {'ru': 'Обложка (баннер сверху)', 'uz': 'Muqova (yuqori banner)', 'en': 'Cover (top banner)'},
    'design_cover_remove': {'ru': 'Убрать обложку', 'uz': 'Muqovani olib tashlash', 'en': 'Remove cover'},
    'design_cover_big': {'ru': 'Обложка больше 5 МБ — загрузите меньше.', 'uz': 'Muqova 5 MB dan katta — kichikroq yuklang.', 'en': 'Cover is over 5 MB — upload a smaller one.'},
    'design_radius_none': {'ru': 'Прямые', 'uz': 'Toʻgʻri', 'en': 'Square'},
    'design_radius_sm': {'ru': 'Слегка', 'uz': 'Yengil', 'en': 'Slight'},
    'design_radius_md': {'ru': 'Средне', 'uz': 'Oʻrtacha', 'en': 'Medium'},
    'design_radius_lg': {'ru': 'Сильно', 'uz': 'Kuchli', 'en': 'Round'},
    'design_preset_classic': {'ru': 'Классика', 'uz': 'Klassika', 'en': 'Classic'},
    'design_preset_dark': {'ru': 'Тёмная', 'uz': 'Qorongʻi', 'en': 'Dark'},
    'design_preset_minimal': {'ru': 'Минимал', 'uz': 'Minimal', 'en': 'Minimal'},
    'design_preset_chaikhana': {'ru': 'Чайхана', 'uz': 'Choyxona', 'en': 'Chaikhana'},

    # тарифы / лимиты
    'plan_label':       {'ru': 'Тариф', 'uz': 'Tarif', 'en': 'Plan'},
    'plan_venues':      {'ru': 'Заведения', 'uz': 'Muassasalar', 'en': 'Venues'},
    'plan_dishes':      {'ru': 'Блюда в заведении', 'uz': 'Muassasadagi taomlar', 'en': 'Dishes in venue'},
    'plan_unlimited':   {'ru': 'без лимита', 'uz': 'cheksiz', 'en': 'unlimited'},
    'plan_limit_venues': {'ru': 'Достигнут лимит заведений по тарифу. Обновите тариф, чтобы добавить ещё.', 'uz': 'Tarif boʻyicha muassasalar limiti tugadi. Yana qoʻshish uchun tarifni yangilang.', 'en': 'You’ve reached your plan’s venue limit. Upgrade to add more.'},
    'plan_limit_dishes': {'ru': 'Достигнут лимит блюд по тарифу. Обновите тариф, чтобы добавить ещё.', 'uz': 'Tarif boʻyicha taomlar limiti tugadi. Yana qoʻshish uchun tarifni yangilang.', 'en': 'You’ve reached your plan’s dish limit. Upgrade to add more.'},
    'plan_upgrade':     {'ru': 'Сменить тариф', 'uz': 'Tarifni oʻzgartirish', 'en': 'Change plan'},

    # статусы заказа
    'st_new':           {'ru': 'Новый', 'uz': 'Yangi', 'en': 'New'},
    'st_accepted':      {'ru': 'Принят', 'uz': 'Qabul qilindi', 'en': 'Accepted'},
    'st_cooking':       {'ru': 'Готовится', 'uz': 'Tayyorlanmoqda', 'en': 'Cooking'},
    'st_served':        {'ru': 'Подан', 'uz': 'Berildi', 'en': 'Served'},
    'st_closed':        {'ru': 'Закрыт', 'uz': 'Yopildi', 'en': 'Closed'},
    'st_cancelled':     {'ru': 'Отменён', 'uz': 'Bekor qilindi', 'en': 'Cancelled'},

    # заказы (кабинет)
    'ord_title':        {'ru': 'Заказы', 'uz': 'Buyurtmalar', 'en': 'Orders'},
    'ord_subtitle':     {'ru': 'Новые заказы появляются автоматически', 'uz': 'Yangi buyurtmalar avtomatik chiqadi', 'en': 'New orders appear automatically'},
    'ord_active':       {'ru': 'активных', 'uz': 'faol', 'en': 'active'},
    'ord_closed_today': {'ru': 'закрыто сегодня', 'uz': 'bugun yopildi', 'en': 'closed today'},
    'ord_open_tables':  {'ru': 'Открытые столы', 'uz': 'Ochiq stollar', 'en': 'Open tables'},
    'ord_close_table':  {'ru': 'Закрыть стол', 'uz': 'Stolni yopish', 'en': 'Close table'},
    'ord_close_table_confirm': {'ru': 'Закрыть стол? Новые заказы по нему приниматься не будут, пока гость снова не откроет меню.', 'uz': 'Stol yopilsinmi? Mehmon menyuni qayta ochmaguncha yangi buyurtmalar qabul qilinmaydi.', 'en': 'Close this table? New orders won’t be accepted until a guest reopens the menu.'},
    'ord_empty_col':    {'ru': 'Пусто', 'uz': 'Boʻsh', 'en': 'Empty'},
    'ord_no_active':    {'ru': 'Пока нет активных заказов', 'uz': 'Hozircha faol buyurtmalar yoʻq', 'en': 'No active orders yet'},
    'ord_table':        {'ru': 'Стол', 'uz': 'Stol', 'en': 'Table'},
    'ord_no_table':     {'ru': 'Без стола', 'uz': 'Stolsiz', 'en': 'No table'},
    'ord_advance':      {'ru': 'Дальше →', 'uz': 'Keyingisi →', 'en': 'Next →'},
    'ord_close':        {'ru': 'Закрыть', 'uz': 'Yopish', 'en': 'Close'},
    'ord_cancel':       {'ru': 'Отменить', 'uz': 'Bekor qilish', 'en': 'Cancel'},
    'ord_cancel_confirm': {'ru': 'Отменить заказ?', 'uz': 'Buyurtma bekor qilinsinmi?', 'en': 'Cancel the order?'},
    'ord_som':          {'ru': 'сум', 'uz': 'soʻm', 'en': 'soʻm'},
    'ord_comment':      {'ru': 'Комментарий', 'uz': 'Izoh', 'en': 'Comment'},
    'ord_sound_on':     {'ru': '🔔 Звук вкл', 'uz': '🔔 Tovush yoq', 'en': '🔔 Sound on'},
    'ord_sound_off':    {'ru': '🔕 Звук выкл', 'uz': '🔕 Tovush oʻchiq', 'en': '🔕 Sound off'},
    'ord_new_order':    {'ru': 'Новый заказ', 'uz': 'Yangi buyurtma', 'en': 'New order'},

    # история заказов
    'nav_history':      {'ru': 'История', 'uz': 'Tarix', 'en': 'History'},
    'hist_title':       {'ru': 'История заказов', 'uz': 'Buyurtmalar tarixi', 'en': 'Order history'},
    'hist_subtitle':    {'ru': 'Закрытые и отменённые заказы', 'uz': 'Yopilgan va bekor qilingan buyurtmalar', 'en': 'Closed and cancelled orders'},
    'hist_today':       {'ru': 'Сегодня', 'uz': 'Bugun', 'en': 'Today'},
    'hist_7d':          {'ru': '7 дней', 'uz': '7 kun', 'en': '7 days'},
    'hist_30d':         {'ru': '30 дней', 'uz': '30 kun', 'en': '30 days'},
    'hist_all':         {'ru': 'Всё время', 'uz': 'Butun davr', 'en': 'All time'},
    'hist_export':      {'ru': 'Выгрузить CSV', 'uz': 'CSV yuklab olish', 'en': 'Export CSV'},
    'hist_empty':       {'ru': 'За этот период заказов нет', 'uz': 'Bu davrda buyurtmalar yoʻq', 'en': 'No orders in this period'},
    'hist_count':       {'ru': 'заказов', 'uz': 'buyurtma', 'en': 'orders'},
    'hist_revenue':     {'ru': 'выручка', 'uz': 'tushum', 'en': 'revenue'},
    'hist_items_short': {'ru': 'поз.', 'uz': 'ta', 'en': 'items'},
    'hist_prev':        {'ru': '← Назад', 'uz': '← Orqaga', 'en': '← Prev'},
    'hist_next':        {'ru': 'Вперёд →', 'uz': 'Oldinga →', 'en': 'Next →'},

    # аналитика
    'an_title':         {'ru': 'Аналитика', 'uz': 'Tahlil', 'en': 'Analytics'},
    'an_subtitle':      {'ru': 'Заказы и выручка заведения', 'uz': 'Buyurtmalar va tushum', 'en': 'Orders and revenue'},
    'an_today':         {'ru': 'Сегодня', 'uz': 'Bugun', 'en': 'Today'},
    'an_orders':        {'ru': 'Заказов', 'uz': 'Buyurtmalar', 'en': 'Orders'},
    'an_revenue':       {'ru': 'Выручка', 'uz': 'Tushum', 'en': 'Revenue'},
    'an_avg_check':     {'ru': 'Средний чек', 'uz': 'Oʻrtacha chek', 'en': 'Average check'},
    'an_active_now':    {'ru': 'Активных сейчас', 'uz': 'Hozir faol', 'en': 'Active now'},
    'an_week':          {'ru': 'За 7 дней', 'uz': '7 kun', 'en': 'Last 7 days'},
    'an_top':           {'ru': 'Топ блюд за неделю', 'uz': 'Hafta xitlari', 'en': 'Top dishes (week)'},
    'an_qty':           {'ru': 'шт', 'uz': 'dona', 'en': 'pcs'},
    'an_som':           {'ru': 'сум', 'uz': 'soʻm', 'en': 'soʻm'},
    'an_no_data':       {'ru': 'Пока нет данных — заказы появятся здесь', 'uz': 'Hozircha maʼlumot yoʻq', 'en': 'No data yet'},
    'an_note':          {'ru': 'Выручка = сумма заказов (без отменённых). Оплату сервис не считает.', 'uz': 'Tushum = buyurtmalar summasi (bekorlarsiz).', 'en': 'Revenue = sum of orders (excl. cancelled).'},
    'an_dynamics':      {'ru': 'Динамика за 7 дней', 'uz': '7 kunlik dinamika', 'en': '7-day dynamics'},
    'an_top_chart':     {'ru': 'Топ блюд (шт)', 'uz': 'Top taomlar (dona)', 'en': 'Top dishes (pcs)'},

    # настройки заведения
    'set_title':        {'ru': 'Настройки', 'uz': 'Sozlamalar', 'en': 'Settings'},
    'set_subtitle':     {'ru': 'Профиль заведения', 'uz': 'Muassasa profili', 'en': 'Venue profile'},
    'set_name':         {'ru': 'Название', 'uz': 'Nomi', 'en': 'Name'},
    'set_type':         {'ru': 'Тип', 'uz': 'Turi', 'en': 'Type'},
    'set_city':         {'ru': 'Город', 'uz': 'Shahar', 'en': 'City'},
    'set_phone':        {'ru': 'Телефон', 'uz': 'Telefon', 'en': 'Phone'},
    'set_logo':         {'ru': 'Логотип', 'uz': 'Logotip', 'en': 'Logo'},
    'set_desc':         {'ru': 'Описание', 'uz': 'Tavsif', 'en': 'Description'},
    'set_address':      {'ru': 'Адрес (slug)', 'uz': 'Manzil (slug)', 'en': 'Address (slug)'},
    'set_address_hint': {'ru': 'Не меняется — на него завязаны ссылки кабинета', 'uz': 'Oʻzgarmaydi', 'en': 'Fixed — cabinet links depend on it'},
    'set_save':         {'ru': 'Сохранить', 'uz': 'Saqlash', 'en': 'Save'},
    'set_saved':        {'ru': 'Сохранено', 'uz': 'Saqlandi', 'en': 'Saved'},
    'set_logo_current': {'ru': 'Текущий логотип', 'uz': 'Joriy logotip', 'en': 'Current logo'},

    # статус заказа (гость)
    'ost_title':        {'ru': 'Заказ принят', 'uz': 'Buyurtma qabul qilindi', 'en': 'Order placed'},
    'ost_number':       {'ru': 'Заказ', 'uz': 'Buyurtma', 'en': 'Order'},
    'ost_status':       {'ru': 'Статус', 'uz': 'Holat', 'en': 'Status'},
    'ost_total':        {'ru': 'Итого', 'uz': 'Jami', 'en': 'Total'},
    'ost_comment':      {'ru': 'Ваш комментарий', 'uz': 'Izohingiz', 'en': 'Your comment'},
    'ost_cancelled':    {'ru': 'Заказ отменён', 'uz': 'Buyurtma bekor qilindi', 'en': 'Order cancelled'},
    'ost_back_menu':    {'ru': '← Вернуться в меню', 'uz': '← Menyuga qaytish', 'en': '← Back to menu'},
    'ost_new_order':    {'ru': 'Сделать ещё заказ', 'uz': 'Yana buyurtma berish', 'en': 'Place another order'},
    'ost_som':          {'ru': 'сум', 'uz': 'soʻm', 'en': 'soʻm'},

    # добавление заведения (в кабинете)
    'venue_add':        {'ru': 'Добавить заведение', 'uz': 'Muassasa qoʻshish', 'en': 'Add venue'},
    'venue_new':        {'ru': 'Новое заведение', 'uz': 'Yangi muassasa', 'en': 'New venue'},
    'venue_create_btn': {'ru': 'Создать заведение', 'uz': 'Muassasa yaratish', 'en': 'Create venue'},
    'venue_created':    {'ru': 'Заведение создано', 'uz': 'Muassasa yaratildi', 'en': 'Venue created'},
    'venue_back':       {'ru': '← К заведениям', 'uz': '← Muassasalarga', 'en': '← Back to venues'},

    # сообщения / ошибки
    'msg_code_sent':    {'ru': 'Код отправлен', 'uz': 'Kod yuborildi', 'en': 'Code sent'},
    'err_otp_throttled': {'ru': 'Код уже отправлен. Если не пришёл — подождите минуту и попробуйте снова.', 'uz': 'Kod allaqachon yuborilgan. Kelmasa — bir daqiqa kuting va qayta urinib koʻring.', 'en': 'A code was already sent. If it didn’t arrive, wait a minute and try again.'},
    'err_required':     {'ru': 'Заполните название и телефон', 'uz': 'Nom va telefonni toʻldiring', 'en': 'Fill in name and phone'},
    'err_phone_uz':     {'ru': 'Введите номер в формате +998 XX XXX-XX-XX', 'uz': 'Raqamni +998 XX XXX-XX-XX koʻrinishida kiriting', 'en': 'Enter the number as +998 XX XXX-XX-XX'},
    'err_invalid_code': {'ru': 'Неверный код', 'uz': 'Notoʻgʻri kod', 'en': 'Invalid code'},
    'err_attempts_left': {'ru': 'осталось попыток', 'uz': 'urinish qoldi', 'en': 'attempts left'},
    'err_otp_locked':   {'ru': 'Слишком много неверных попыток. Запросите новый код.', 'uz': 'Juda koʻp notoʻgʻri urinish. Yangi kod soʻrang.', 'en': 'Too many wrong attempts. Request a new code.'},
    'err_otp_expired':  {'ru': 'Код истёк или не запрашивался. Получите новый.', 'uz': 'Kod muddati oʻtgan yoki soʻralmagan. Yangisini oling.', 'en': 'Code expired or not requested. Get a new one.'},
    'err_no_user':      {'ru': 'Заведение с таким номером не найдено', 'uz': 'Bu raqam topilmadi', 'en': 'No account with this number'},
    'reg_exists':       {'ru': 'Этот номер уже зарегистрирован. Войдите, а новое заведение добавьте в кабинете.', 'uz': 'Bu raqam allaqachon roʻyxatda. Kiring va yangi muassasani kabinetda qoʻshing.', 'en': 'This number is already registered. Log in and add a new venue from the dashboard.'},

    # ===== Лендинг (главная) =====
    # навигация
    'l_nav_features':   {'ru': 'Возможности', 'uz': 'Imkoniyatlar', 'en': 'Features'},
    'l_nav_how':        {'ru': 'Как работает', 'uz': 'Qanday ishlaydi', 'en': 'How it works'},
    'l_nav_pricing':    {'ru': 'Цены', 'uz': 'Narxlar', 'en': 'Pricing'},

    # hero
    'l_hero_badge':     {'ru': 'QR-меню для общепита Узбекистана', 'uz': 'Oʻzbekiston umumiy ovqatlanishi uchun QR-menyu', 'en': 'QR menu for Uzbekistan’s food service'},
    'l_hero_h1':        {'ru': 'Меню, которое гость открывает', 'uz': 'Mehmon ochadigan menyu —', 'en': 'A menu your guest opens'},
    'l_hero_h1_accent': {'ru': 'за один скан', 'uz': 'bitta skan bilan', 'en': 'in a single scan'},
    'l_hero_sub':       {'ru': 'Гость наводит камеру на QR на столе — и заказывает сам, на родном языке. Вы управляете меню и заказами из одного кабинета. Без приложений и регистрации гостя.', 'uz': 'Mehmon stoldagi QR-ga kamerani toʻgʻrilaydi va oʻz tilida oʻzi buyurtma beradi. Siz menyu va buyurtmalarni bitta kabinetdan boshqarasiz. Ilovasiz va mehmonni roʻyxatdan oʻtkazmasdan.', 'en': 'A guest points the camera at the QR on the table and orders by themselves, in their own language. You manage menu and orders from one dashboard. No apps, no guest sign-up.'},
    'l_hero_cta1':      {'ru': 'Подключить заведение', 'uz': 'Muassasani ulash', 'en': 'Connect your venue'},
    'l_hero_cta2':      {'ru': 'Смотреть демо', 'uz': 'Demoni koʻrish', 'en': 'Watch demo'},
    'l_stat_venues':    {'ru': 'заведений', 'uz': 'muassasa', 'en': 'venues'},
    'l_stat_langs_num': {'ru': '3 языка', 'uz': '3 til', 'en': '3 languages'},
    'l_stat_start':     {'ru': 'старт', 'uz': 'boshlash', 'en': 'to start'},

    # phone mock
    'l_mock_popular':   {'ru': 'Популярное', 'uz': 'Ommabop', 'en': 'Popular'},
    'l_mock_hot':       {'ru': 'Горячее', 'uz': 'Issiq taomlar', 'en': 'Hot'},
    'l_mock_cart':      {'ru': 'Корзина', 'uz': 'Savat', 'en': 'Cart'},
    'l_mock_scan':      {'ru': 'СКАН', 'uz': 'SKAN', 'en': 'SCAN'},
    'l_mock_table':     {'ru': 'СТОЛ', 'uz': 'STOL', 'en': 'TABLE'},

    # features
    'l_feat_kicker':    {'ru': 'Возможности', 'uz': 'Imkoniyatlar', 'en': 'Features'},
    'l_feat_h2':        {'ru': 'Всё для меню и заказов — в одном месте', 'uz': 'Menyu va buyurtmalar uchun hammasi — bir joyda', 'en': 'Everything for menu and orders — in one place'},
    'l_f1_t':           {'ru': 'QR на каждом столе', 'uz': 'Har bir stolda QR', 'en': 'QR on every table'},
    'l_f1_d':           {'ru': 'Гость сканирует код и сразу видит меню своего стола. Без приложений, без регистрации, без официанта.', 'uz': 'Mehmon kodni skanerlaydi va oʻz stolining menyusini darhol koʻradi. Ilovasiz, roʻyxatsiz, ofitsiantsiz.', 'en': 'The guest scans the code and instantly sees the menu for their table. No apps, no sign-up, no waiter.'},
    'l_f2_t':           {'ru': 'Три языка из коробки', 'uz': 'Uchta til standart', 'en': 'Three languages out of the box'},
    'l_f2_d':           {'ru': 'Русский, узбекский (латиница) и английский. Гость выбирает язык — меню переключается целиком.', 'uz': 'Rus, oʻzbek (lotin) va ingliz. Mehmon tilni tanlaydi — menyu toʻliq almashadi.', 'en': 'Russian, Uzbek (Latin) and English. The guest picks a language and the whole menu switches.'},
    'l_f3_t':           {'ru': 'Цены в сумах', 'uz': 'Narxlar soʻmda', 'en': 'Prices in soʻm'},
    'l_f3_d':           {'ru': 'Крупные читаемые числа в формате «45 000 so‘m». Скидки, стоп-листы и веса порций.', 'uz': '«45 000 so‘m» koʻrinishidagi yirik, oʻqilishi oson raqamlar. Chegirmalar, stop-listlar va porsiya vaznlari.', 'en': 'Large, readable numbers like “45 000 so‘m”. Discounts, stop-lists and portion weights.'},
    'l_f4_t':           {'ru': 'Меню без программиста', 'uz': 'Dasturchisiz menyu', 'en': 'Menu without a developer'},
    'l_f4_d':           {'ru': 'Добавляйте блюда, фото и цены сами. Перетаскивайте порядок, включайте и выключайте позиции в один клик.', 'uz': 'Taom, surat va narxlarni oʻzingiz qoʻshing. Tartibni surib oʻzgartiring, pozitsiyalarni bir bosishda yoqing va oʻchiring.', 'en': 'Add dishes, photos and prices yourself. Drag to reorder, toggle items on and off in one click.'},
    'l_f5_t':           {'ru': 'Заказы в реальном времени', 'uz': 'Real vaqtda buyurtmalar', 'en': 'Real-time orders'},
    'l_f5_d':           {'ru': 'Новые заказы прилетают на кухню мгновенно. Статусы «принят → готовится → готово → подано».', 'uz': 'Yangi buyurtmalar oshxonaga bir zumda tushadi. Holatlar: «qabul qilindi → tayyorlanmoqda → tayyor → berildi».', 'en': 'New orders reach the kitchen instantly. Statuses: “accepted → cooking → ready → served”.'},
    'l_f6_t':           {'ru': 'Аналитика продаж', 'uz': 'Sotuv tahlili', 'en': 'Sales analytics'},
    'l_f6_d':           {'ru': 'Выручка, средний чек, хиты и аутсайдеры меню. Понимайте, что заказывают и что стоит убрать.', 'uz': 'Tushum, oʻrtacha chek, menyu xitlari va autsayderlari. Nima buyurtma qilinayotganini va nimani olib tashlash kerakligini tushuning.', 'en': 'Revenue, average check, bestsellers and weak items. See what’s ordered and what to drop.'},

    # how it works
    'l_how_kicker':     {'ru': 'Как это работает', 'uz': 'Qanday ishlaydi', 'en': 'How it works'},
    'l_how_h2':         {'ru': 'Запуск за 5 минут', 'uz': '5 daqiqada ishga tushirish', 'en': 'Launch in 5 minutes'},
    'l_how1_t':         {'ru': 'Зарегистрируйте заведение', 'uz': 'Muassasani roʻyxatdan oʻtkazing', 'en': 'Register your venue'},
    'l_how1_d':         {'ru': 'Название, тип, город и телефон. Кабинет готов сразу — без договоров и оборудования.', 'uz': 'Nom, tur, shahar va telefon. Kabinet darhol tayyor — shartnoma va jihozsiz.', 'en': 'Name, type, city and phone. The dashboard is ready at once — no contracts or hardware.'},
    'l_how2_t':         {'ru': 'Добавьте меню', 'uz': 'Menyu qoʻshing', 'en': 'Add your menu'},
    'l_how2_d':         {'ru': 'Блюда, фото и цены на трёх языках. Можно импортировать готовый список одним файлом.', 'uz': 'Taom, surat va narxlar uch tilda. Tayyor roʻyxatni bitta fayl bilan import qilish mumkin.', 'en': 'Dishes, photos and prices in three languages. You can import a ready list with a single file.'},
    'l_how3_t':         {'ru': 'Распечатайте QR на столы', 'uz': 'Stollarga QR chop eting', 'en': 'Print QR for tables'},
    'l_how3_d':         {'ru': 'Скачайте готовые таблички с QR для каждого стола — и принимайте первые заказы.', 'uz': 'Har bir stol uchun tayyor QR-jadvalchalarni yuklab oling va birinchi buyurtmalarni qabul qiling.', 'en': 'Download ready QR table-tents for each table — and start taking your first orders.'},

    # pricing
    'l_price_kicker':   {'ru': 'Цены', 'uz': 'Narxlar', 'en': 'Pricing'},
    'l_price_h2':       {'ru': 'Прозрачно, в сумах, без комиссии с заказов', 'uz': 'Shaffof, soʻmda, buyurtmalardan komissiyasiz', 'en': 'Transparent, in soʻm, no fees on orders'},
    'l_per_month':      {'ru': 'so‘m / мес', 'uz': 'so‘m / oyiga', 'en': 'so‘m / mo'},
    'l_plan_start':     {'ru': 'Старт', 'uz': 'Boshlangʻich', 'en': 'Start'},
    'l_plan_start_sub': {'ru': 'Для одной точки', 'uz': 'Bitta nuqta uchun', 'en': 'For a single venue'},
    'l_plan_start_f1':  {'ru': '1 заведение', 'uz': '1 muassasa', 'en': '1 venue'},
    'l_plan_start_f2':  {'ru': 'До 30 блюд', 'uz': '30 tagacha taom', 'en': 'Up to 30 dishes'},
    'l_plan_start_f3':  {'ru': 'QR-меню, 3 языка', 'uz': 'QR-menyu, 3 til', 'en': 'QR menu, 3 languages'},
    'l_plan_start_f4':  {'ru': 'Приём заказов', 'uz': 'Buyurtma qabul qilish', 'en': 'Order taking'},
    'l_plan_start_cta': {'ru': 'Начать бесплатно', 'uz': 'Bepul boshlash', 'en': 'Start free'},
    'l_plan_popular':   {'ru': 'Популярный', 'uz': 'Ommabop', 'en': 'Popular'},
    'l_plan_pro':       {'ru': 'Бизнес', 'uz': 'Biznes', 'en': 'Business'},
    'l_plan_pro_sub':   {'ru': 'Для активной точки', 'uz': 'Faol nuqta uchun', 'en': 'For a busy venue'},
    'l_plan_pro_f1':    {'ru': 'До 3 заведений', 'uz': '3 tagacha muassasa', 'en': 'Up to 3 venues'},
    'l_plan_pro_f2':    {'ru': 'Безлимит блюд', 'uz': 'Cheksiz taom', 'en': 'Unlimited dishes'},
    'l_plan_pro_f3':    {'ru': 'Аналитика и отчёты', 'uz': 'Tahlil va hisobotlar', 'en': 'Analytics and reports'},
    'l_plan_pro_f4':    {'ru': 'Стоп-листы, акции', 'uz': 'Stop-listlar, aksiyalar', 'en': 'Stop-lists, promos'},
    'l_plan_pro_f5':    {'ru': 'Поддержка в Telegram', 'uz': 'Telegram orqali qoʻllab-quvvatlash', 'en': 'Telegram support'},
    'l_plan_pro_cta':   {'ru': 'Попробовать 14 дней', 'uz': '14 kun sinab koʻrish', 'en': 'Try 14 days'},
    'l_plan_net':       {'ru': 'Сеть', 'uz': 'Tarmoq', 'en': 'Network'},
    'l_plan_net_sub':   {'ru': 'Для сетей и франшиз', 'uz': 'Tarmoq va franshizalar uchun', 'en': 'For chains and franchises'},
    'l_plan_net_price': {'ru': 'Договорная', 'uz': 'Kelishuv asosida', 'en': 'Custom'},
    'l_plan_net_f1':    {'ru': 'Безлимит точек', 'uz': 'Cheksiz nuqtalar', 'en': 'Unlimited venues'},
    'l_plan_net_f2':    {'ru': 'Роли и права персонала', 'uz': 'Xodimlar rollari va huquqlari', 'en': 'Staff roles and permissions'},
    'l_plan_net_f3':    {'ru': 'Единое меню сети', 'uz': 'Yagona tarmoq menyusi', 'en': 'Unified network menu'},
    'l_plan_net_f4':    {'ru': 'Интеграции и API', 'uz': 'Integratsiyalar va API', 'en': 'Integrations and API'},
    'l_plan_net_cta':   {'ru': 'Связаться с нами', 'uz': 'Biz bilan bogʻlanish', 'en': 'Contact us'},

    # registration block
    'l_reg_h2':         {'ru': 'Подключите заведение', 'uz': 'Muassasani ulang', 'en': 'Connect your venue'},
    'l_reg_h2_accent':  {'ru': 'за 5 минут', 'uz': '5 daqiqada', 'en': 'in 5 minutes'},
    'l_reg_p':          {'ru': 'Заполните короткую форму — и сразу попадёте в кабинет, где можно добавить меню и получить QR-коды для столов.', 'uz': 'Qisqa shaklni toʻldiring — va darhol kabinetga oʻtasiz, u yerda menyu qoʻshib, stollar uchun QR-kodlar olishingiz mumkin.', 'en': 'Fill in a short form — and land straight in the dashboard, where you can add a menu and get QR codes for tables.'},
    'l_reg_b1_t':       {'ru': 'Бесплатный тариф навсегда', 'uz': 'Abadiy bepul tarif', 'en': 'Free plan forever'},
    'l_reg_b1_d':       {'ru': 'Карта не нужна, оборудование не нужно.', 'uz': 'Karta kerak emas, jihoz kerak emas.', 'en': 'No card needed, no hardware needed.'},
    'l_reg_b2_t':       {'ru': 'Поможем перенести меню', 'uz': 'Menyuni koʻchirishga yordam beramiz', 'en': 'We’ll help move your menu'},
    'l_reg_b2_d':       {'ru': 'Пришлите фото бумажного меню — заполним за вас.', 'uz': 'Qogʻoz menyu suratini yuboring — siz uchun toʻldiramiz.', 'en': 'Send a photo of your paper menu — we’ll fill it in for you.'},
    'l_reg_b3_t':       {'ru': 'Поддержка на русском и узбекском', 'uz': 'Rus va oʻzbek tilida qoʻllab-quvvatlash', 'en': 'Support in Russian and Uzbek'},
    'l_reg_b3_d':       {'ru': 'Отвечаем в Telegram в течение часа.', 'uz': 'Telegramda bir soat ichida javob beramiz.', 'en': 'We reply on Telegram within an hour.'},
    'l_reg_step':       {'ru': 'Шаг 1 / 2', 'uz': 'Qadam 1 / 2', 'en': 'Step 1 / 2'},
    'l_reg_agree':      {'ru': 'Соглашаюсь с условиями и политикой данных.', 'uz': 'Shartlar va maʼlumotlar siyosatiga roziman.', 'en': 'I agree to the terms and data policy.'},
    'l_reg_submit':     {'ru': 'Создать кабинет →', 'uz': 'Kabinet yaratish →', 'en': 'Create dashboard →'},
    'l_reg_city_ph':    {'ru': 'Ташкент', 'uz': 'Toshkent', 'en': 'Tashkent'},

    # footer
    'l_foot_tagline':   {'ru': 'QR-меню и приём заказов для ресторанов, кафе и чайхан Узбекистана.', 'uz': 'Oʻzbekiston restoran, kafe va choyxonalari uchun QR-menyu va buyurtma qabul qilish.', 'en': 'QR menu and order taking for restaurants, cafes and chaikhanas of Uzbekistan.'},
    'l_foot_product':   {'ru': 'Продукт', 'uz': 'Mahsulot', 'en': 'Product'},
    'l_foot_support':   {'ru': 'Поддержка', 'uz': 'Qoʻllab-quvvatlash', 'en': 'Support'},
    'l_foot_lang':      {'ru': 'Язык', 'uz': 'Til', 'en': 'Language'},
    'l_foot_demo':      {'ru': 'Демо-меню', 'uz': 'Demo menyu', 'en': 'Demo menu'},
    'l_foot_help':      {'ru': 'Помощь', 'uz': 'Yordam', 'en': 'Help'},
    'l_foot_contacts':  {'ru': 'Контакты', 'uz': 'Kontaktlar', 'en': 'Contacts'},
    'l_foot_copy':      {'ru': '© 2026 Menus. Ташкент, Узбекистан.', 'uz': '© 2026 Menus. Toshkent, Oʻzbekiston.', 'en': '© 2026 Menus. Tashkent, Uzbekistan.'},
    'l_foot_made':      {'ru': 'Сделано для общепита Узбекистана', 'uz': 'Oʻzbekiston umumiy ovqatlanishi uchun', 'en': 'Made for Uzbekistan’s food service'},
}


def t(lang, key):
    entry = TR.get(key)
    if not entry:
        return key
    return entry.get(lang) or entry.get(DEFAULT_LANG) or key


def tr(request, key):
    """Перевод по языку из сессии запроса."""
    lang = request.session.get('lang', DEFAULT_LANG)
    return t(lang, key)


def resolve_lang(request):
    lang = request.session.get('lang', DEFAULT_LANG)
    return lang if lang in dict(LANGUAGES) else DEFAULT_LANG


def normalize_lang(lang):
    return lang if lang in dict(LANGUAGES) else DEFAULT_LANG


def flat(lang):
    """Плоский словарь переводов для шаблонов: {{ t.key }}."""
    return {key: entry.get(lang) or entry.get(DEFAULT_LANG) or key for key, entry in TR.items()}


def i18n_context(lang):
    """Контекст i18n без request (для render_to_string в consumer'ах)."""
    lang = normalize_lang(lang)
    return {'LANG': lang, 'LANGUAGES': LANGUAGES, 't': flat(lang)}
