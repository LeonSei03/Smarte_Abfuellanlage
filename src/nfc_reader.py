# Example how to build a NFCReader that implements an Interface
from abc import ABC, abstractmethod
import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI
import logging


# Configure logging
logger = logging.getLogger("shared_logger")

# Constants
DEFAULT_KEY_A = bytes([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
BLOCK_COUNT = 64


class NFCReaderInterface(ABC):

    @abstractmethod
    def config(self):
        pass
    @abstractmethod
    def add_logger(self, filepath : str):
        pass
    @abstractmethod
    def read_block(self, uid : bytes , block_number : int):
        pass

    @abstractmethod
    def read_all_blocks(self, uid : int):
        pass

    @abstractmethod
    def write_block(self, uid : bytes, block_number : int, data : bytes):
        pass


class NFCReader(NFCReaderInterface):
    def __init__(self):
        self._pn532 = self.config()

    def __getattr__(self, name):
        """
        Delegate any call to PN532_SPI if it's not explicitly defined in NFCReader.
        """
        return getattr(self._pn532, name)
    # TODO: add logging config
    def add_logger(self, filepath : str):
        pass
    def config(self):
        try:
            spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
            cs_pin = DigitalInOut(board.D8)
            pn532 = PN532_SPI(spi, cs_pin, debug=False)

            ic, ver, rev, support = pn532.firmware_version
            logger.info("Found PN532 with firmware version: %d.%d", ver, rev)

            # Configure PN532 to communicate with MiFare cards
            pn532.SAM_configuration()
            return pn532
        except Exception as e:
            logger.error("Failed to configure PN532: %s", e)
            raise

    def read_block(self, uid, block_number):
        try:
            authenticated = self._pn532.mifare_classic_authenticate_block(
                uid, block_number, 0x60, key=DEFAULT_KEY_A
            )
            if not authenticated:
                logger.error("Failed to authenticate block %d", block_number)
                return None

            block_data = self._pn532.mifare_classic_read_block(block_number)
            if block_data is None:
                logger.error("Failed to read block %d", block_number)
                return None

            return block_data
        except Exception as e:
            logger.exception("Error reading block %d: %s", block_number, e)
            return None

    def read_all_blocks(self, uid):
        blocks_data = []
        for block_number in range(BLOCK_COUNT):
            block_data = self.read_block(uid, block_number)
            if block_data:
                blocks_data.append(block_data)
            else:
                logger.warning("No data read from Block %d", block_number)
        return blocks_data

    def write_block(self, uid, block_number, data):
        try:
            # Validate `uid` type
            if not isinstance(uid, bytes):
                logger.error("UID must be of type 'bytes'. Provided type: %s", type(uid))
                return False

            # Validate `data` type and length
            if not isinstance(data, bytes) or len(data) != 16:
                logger.error(
                    "Data must be a 'bytes' object of exactly 16 bytes. Provided: type=%s, length=%d",
                    type(data),
                    len(data) if isinstance(data, bytes) else 0,
                )
                return False
        
            authenticated = self._pn532.mifare_classic_authenticate_block(
                uid, block_number, 0x60, key=DEFAULT_KEY_A
            )
            if not authenticated:
                logger.error("Failed to authenticate block %d for writing", block_number)
                return False

            success = self._pn532.mifare_classic_write_block(block_number, data)
            if not success:
                logger.error("Failed to write to block %d", block_number)
                return False

            logger.info("Successfully wrote data to block %d", block_number)
            return True
        except Exception as e:
            logger.exception("Error writing block %d: %s", block_number, e)
            return False

    def write_block(self, uid, block_number, data):
        try:
            authenticated = self._pn532.mifare_classic_authenticate_block(
                uid, block_number, 0x60, key=DEFAULT_KEY_A
            )
            if not authenticated:
                logger.error("Failed to authenticate block %d for writing", block_number)
                return False

            success = self._pn532.mifare_classic_write_block(block_number, data)
            if not success:
                logger.error("Failed to write to block %d", block_number)
                return False

            logger.info("Successfully wrote data to block %d", block_number)
            return True
        except Exception as e:
            logger.exception("Error writing block %d: %s", block_number, e)
            return False

if __name__ == "__main__":

    nfc_reader = NFCReader()

    logger.info("Waiting for RFID/NFC card...")
    while True:
        uid = nfc_reader.read_passive_target(timeout=0.5)
        print(".", end="")
        if uid is None:
            continue
        logger.info("Found card with UID: %s", [hex(i) for i in uid])
        break

    uid_bytes = bytes(uid)
    uid_16 = bytes([
    0x93, 0x5f, 0xa7, 0x91,  # First 4 bytes
    0x01, 0x02, 0x03, 0x04,  # Next 4 bytes
    0x05, 0x06, 0x07, 0x08,  # Next 4 bytes
    0x09, 0x0A, 0x0B, 0x0C   # Last 4 bytes
    ])
    nfc_reader.write_block(uid = uid_bytes, block_number = 2, data = uid_16)
    
    blocks_data = nfc_reader.read_all_blocks(uid)
    for block_number, block_data in enumerate(blocks_data):
        hex_values = " ".join([f"{byte:02x}" for byte in block_data])
        logger.info("Data in Block %d: %s", block_number, hex_values)
