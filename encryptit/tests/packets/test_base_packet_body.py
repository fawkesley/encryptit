from nose.tools import assert_raises

from encryptit.packets import BasePacketBody


def test_that_a_good_concrete_class_can_be_instantiated():
    GoodConcretePacketBody()


def test_that_a_bad_concrete_class_can_be_instantiated():
    assert_raises(TypeError, BadConcretePacketBody)


class GoodConcretePacketBody(BasePacketBody):
    @classmethod
    def from_stream(cls):
        pass

    @property
    def raw(self):
        pass

    @property
    def decoded(self):
        pass

    def serialize(self):
        pass


class BadConcretePacketBody(BasePacketBody):
    pass  # Missing abstract methods
