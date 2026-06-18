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
    'menu_in_stock':    {'ru': 'В наличии', 'uz': 'Mavjud', 'en': 'In stock'},
    'menu_stop':        {'ru': 'Стоп', 'uz': 'Toʻxtatilgan', 'en': 'Stop'},
    'menu_from':        {'ru': 'от', 'uz': 'dan', 'en': 'from'},
    'menu_som':         {'ru': 'сум', 'uz': 'soʻm', 'en': 'soʻm'},
    'menu_edit':        {'ru': 'Редактировать', 'uz': 'Tahrirlash', 'en': 'Edit'},
    'menu_delete':      {'ru': 'Удалить', 'uz': 'Oʻchirish', 'en': 'Delete'},
    'menu_save':        {'ru': 'Сохранить', 'uz': 'Saqlash', 'en': 'Save'},
    'menu_cancel':      {'ru': 'Отмена', 'uz': 'Bekor qilish', 'en': 'Cancel'},
    'menu_back':        {'ru': '← К меню', 'uz': '← Menyuga', 'en': '← Back to menu'},

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

    # сообщения / ошибки
    'msg_code_sent':    {'ru': 'Код отправлен', 'uz': 'Kod yuborildi', 'en': 'Code sent'},
    'err_required':     {'ru': 'Заполните название и телефон', 'uz': 'Nom va telefonni toʻldiring', 'en': 'Fill in name and phone'},
    'err_invalid_code': {'ru': 'Неверный или просроченный код', 'uz': 'Kod notoʻgʻri yoki muddati oʻtgan', 'en': 'Invalid or expired code'},
    'err_no_user':      {'ru': 'Заведение с таким номером не найдено', 'uz': 'Bu raqam topilmadi', 'en': 'No account with this number'},
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
