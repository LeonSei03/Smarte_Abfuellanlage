import nfc_reader
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":

    nfc_reader = nfc_reader.NFCReader()

    logger.info("Waiting for RFID/NFC card...")
    while True:
        uid = nfc_reader.read_passive_target(timeout=0.5)
        print(".", end="")
        if uid is None:
            continue
        logger.info("Found card with UID: %s", [hex(i) for i in uid])
        break

    blocks_data = nfc_reader.read_all_blocks(uid)
    for block_number, block_data in enumerate(blocks_data):
        hex_values = " ".join([f"{byte:02x}" for byte in block_data])
        logger.info("Data in Block %d: %s", block_number, hex_values)
