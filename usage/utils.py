from base.models import User


def get_user_by_pk(pk):
    try:
        user = User.objects.get(id=pk)
    except:
        user = None
    return user


def get_object_by_id(model, pk):
    try:
        data = model.objects.get(id=pk)
    except:
        data = None
    return data
