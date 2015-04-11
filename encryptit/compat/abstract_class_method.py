class _abstractclassmethod(classmethod):
    """
    Backport from Python 3.x. See http://stackoverflow.com/a/11218474
    """

    __isabstractmethod__ = True

    def __init__(self, callable):
        callable.__isabstractmethod__ = True
        super(abstractclassmethod, self).__init__(callable)


try:
    from abc import abstractclassmethod
except ImportError:
    abstractclassmethod = _abstractclassmethod
