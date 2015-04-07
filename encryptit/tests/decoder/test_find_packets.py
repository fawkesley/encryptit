from os.path import join as pjoin

from nose.tools import assert_equal

from ..sample_files import SAMPLE_FILES, SAMPLE_DIR

from encryptit.decoder import find_packets
from encryptit.openpgp_message import PacketLocation


EXPECTED_LOCATIONS = {
    'gpg_1.4.16_symmetric_simples2k.gpg': [
        PacketLocation(
            header_start=0,
            body_start=2,
            body_length=4),
        PacketLocation(
            header_start=6,
            body_start=8,
            body_length=59),
    ],
    'gpg_2.0.22_symmetric_simples2k.gpg': [
        PacketLocation(
            header_start=0,
            body_start=2,
            body_length=4),
        PacketLocation(
            header_start=6,
            body_start=8,
            body_length=59),
    ],
    'gpg_1.4.16_symmetric_saltedanditerateds2k.gpg': [
        PacketLocation(
            header_start=0,
            body_start=2,
            body_length=13),
        PacketLocation(
            header_start=15,
            body_start=17,
            body_length=72),
    ],
    'gpg_2.0.22_symmetric_saltedanditerated2k.gpg': [
        PacketLocation(
            header_start=0,
            body_start=2,
            body_length=13),
        PacketLocation(
            header_start=15,
            body_start=17,
            body_length=59),
    ],
    'gpg_1.4.16_asymmetric_and_symmetric_simples2k.gpg': [

        PacketLocation(
            header_start=0,
            body_start=3,
            body_length=524),

        PacketLocation(
            header_start=527,
            body_start=529,
            body_length=46),

        PacketLocation(
            header_start=575,
            body_start=577,
            body_length=65),

    ],

}


def test_packet_locations():
    for short_filename, long_filename in SAMPLE_FILES:
        yield assert_packet_locations_equal, short_filename


def assert_packet_locations_equal(short_filename):
    with open(pjoin(SAMPLE_DIR, short_filename), 'rb') as f:
        assert_equal(
            EXPECTED_LOCATIONS.get(short_filename, []),
            find_packets(f)
        )
