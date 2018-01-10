def get_or_none(classmodel, **kwargs):
    """Function get Model object from given attibutes and values.

    Args:
        classmodel: Class of Models
        kwargs: Paramters of required to filter out from model.

    Returns:
        Object - Return object of found else None from Exception.

    """
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None
