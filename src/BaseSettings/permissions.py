from rolepermissions.permissions import register_object_checker
from .roles import SystemAdmin

@register_object_checker()
def access_clinic(role, user, clinic):
    if role == SystemAdmin:
        return True

    if user.clinic == clinic:
        return True
    return False



# Create your views here.
def check_user_is_admin(user):
    try:
        return user.is_staff
    except Exception as e:
        return True
