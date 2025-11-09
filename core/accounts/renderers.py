# accounts/renderers.py

from rest_framework.renderers import JSONRenderer

def get_default_renderer():
    """
    Returns the default renderer instance.
    For now, we just return JSONRenderer from DRF.
    """
    return JSONRenderer()
