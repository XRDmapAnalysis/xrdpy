try:
    from ._version import version as __version__
except ImportError:
    __version__ = "d0.0.0"

from .XRD import general_fns, xrd, plottings

__all__ = ['general_fns', 'xrd', 'plottings']
