try:
    import assert_is_instance
except ImportError:
    def assert_is_instance(obj, cls, msg=None):
        assert isinstance(obj, cls), msg
