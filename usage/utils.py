from base.models import User


def get_user_by_pk(pk):
    try:
        user = User.objects.get(id=pk)
    except:
        user = None
