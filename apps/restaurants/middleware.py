from django.shortcuts import render


class SubscriptionBlocked(Exception):
    """Поднимается, когда доступ к заведению закрыт из-за подписки владельца.

    Ловится SubscriptionMiddleware и превращается в страницу «подписка истекла».
    """

    def __init__(self, restaurant):
        self.restaurant = restaurant
        super().__init__('subscription blocked')


class SubscriptionMiddleware:
    """Показывает экран блокировки вместо кабинета, если подписка не активна."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, SubscriptionBlocked):
            restaurant = exception.restaurant
            ctx = {
                'restaurant': restaurant,
                'status': restaurant.owner.subscription_status if restaurant.owner_id else 'suspended',
            }
            # HTMX-запрос: уводим на полную перезагрузку, чтобы показать экран
            if request.headers.get('HX-Request'):
                resp = render(request, 'cabinet/subscription_blocked.html', ctx, status=402)
                resp['HX-Redirect'] = request.path
                return resp
            return render(request, 'cabinet/subscription_blocked.html', ctx, status=402)
        return None
