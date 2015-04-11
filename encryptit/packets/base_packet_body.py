from abc import ABCMeta, abstractproperty, abstractmethod

from six import add_metaclass

from ..compat import abstractclassmethod


@add_metaclass(ABCMeta)
class BasePacketBody(object):

    @abstractclassmethod
    def from_stream(cls, f, body_start, body_length):
        pass

    @abstractproperty
    def raw(self):
        pass

    @abstractproperty
    def decoded(self):
        pass

    @abstractmethod
    def serialize(self):
        pass
