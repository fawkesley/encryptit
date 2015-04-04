import logging

from enum import Enum

from ..mixins import SerializeNameOctetValueMixin

LOG = logging.getLogger(__name__)


class PacketType(SerializeNameOctetValueMixin, Enum):
    """
    4.3. Packet Tags
    http://tools.ietf.org/html/rfc4880#section-4.3
    """

    PublicKeyEncryptedSessionKeyPacket = 1
    SignaturePacket = 2
    SymmetricKeyEncryptedSessionKeyPacket = 3
    OnePassSignaturePacket = 4
    SecretKeyPacket = 5
    PublicKeyPacket = 6
    SecretSubkeyPacket = 7
    CompressedDataPacket = 8
    SymmetricallyEncryptedDataPacket = 9
    MarkerPacket = 10
    LiteralDataPacket = 11
    TrustPacket = 12
    UserIDPacket = 13
    PublicSubkeyPacket = 14
    UserAttributePacket = 17
    SymmetricEncryptedandIntegrityProtectedDataPacket = 18
    ModificationDetectionCodePacket = 19

    def __str__(self):
        return '{} (tag {})'.format(self.name, self.value)
