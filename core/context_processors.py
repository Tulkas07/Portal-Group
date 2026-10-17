from .permissions import can_manage, is_admin


def roles(request):
    """Змінні is_admin / can_manage доступні в усіх шаблонах."""
    return {"is_admin": is_admin(request.user), "can_manage": can_manage(request.user)}
