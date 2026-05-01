# Unrelated utility functions

def is_float(number):
    try:
        float(number)
        return True
    except ValueError:
        return False