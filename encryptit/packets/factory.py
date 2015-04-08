from .generic_packet_body import GenericPacketBody

PACKET_CLASSES = {
    #  PacketType.LiteralDataPacket:
    #  LiteralDataPacket,

    #  PacketType.SymmetricKeyEncryptedSessionKeyPacket:
    #  SymmetricKeyEncryptedSessionKeyPacket,

    #  PacketType.SymmetricEncryptedandIntegrityProtectedDataPacket:
    #  SymmetricEncryptedandIntegrityProtectedDataPacket,

    #  PacketType.SymmetricallyEncryptedDataPacket:
    #  SymmetricallyEncryptedDataPacket,
}


def get_packet_body_class(packet_type):
    """
    Return the class relating to the given PacketType, for example a
    SymmetricallyEncryptedDataPacket.
    """
    return PACKET_CLASSES.get(packet_type, GenericPacketBody)
