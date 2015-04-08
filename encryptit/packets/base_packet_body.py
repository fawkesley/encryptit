from abc import ABCMeta, abstractproperty, abstractmethod

from ..compat import abstractclassmethod


class BasePacketBody(object):
    __metaclass__ = ABCMeta

    @abstractclassmethod
    def from_stream(self, f, body_start, body_length):
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
