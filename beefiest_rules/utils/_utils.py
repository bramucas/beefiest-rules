def check_iterable(var, variable_name: str) -> None:
    """Raises a ValueError exception if the given variable 'var' is not a non-empty iterable type.

    Args:
        var (): variable to be checked.
        variable_name (str): name of the varibale that appear in the message of the raised exceptions.

    Raises:
        ValueError: if 'var' is None.
        ValueError: if 'var' is 'str' type or not Iterable type.
        ValueError: if len(var) == 0.
    """
    if var is None:
        raise ValueError(f'Argument "{variable_name}" must not be None')
    if not hasattr(var, '__iter__') and type(var) != str:
        raise ValueError(
            f'Argument "{variable_name}" must be (a non-str) iterable.')
    if len(var) == 0:
        raise ValueError(f'Argument "{variable_name}" can not be empty')
