import os
import hashlib


class Block:
    hash: str
    index_all: int
    chunk: bytes
    hash_previous: str

    def __init__(self, file_hash, index_all, chunk, hash_previous):
        self.hash = file_hash
        self.index_all = index_all
        self.chunk = chunk
        self.hash_previous = hash_previous

    def generate_hash(self):
        """
        Generates a SHA256 hash of the given block instance, using its four attributes:
        hash, index_all, chunk and hash_previous.

        :return: SHA256 hash of this block instance using all its attributes.
        """
        block_hash = hashlib.sha256()
        block_hash.update(bytes(self.hash, 'utf-8'))
        block_hash.update(bytes(str(self.index_all), 'utf-8'))
        block_hash.update(self.chunk)
        block_hash.update(bytes(self.hash_previous, 'utf-8'))
        return block_hash.hexdigest()

    def check_file_integrity(self):
        pass


def calculate_file_hash(filepath):
    # Calculate the hash (SHA256 checksum) for a given file
    buffer_size = 1024 * 1024
    sha256 = hashlib.sha256()

    with open(filepath, "rb") as file:
        while True:
            file_buffer = file.read(buffer_size)
            if not file_buffer:
                break
            sha256.update(file_buffer)

    return sha256.hexdigest()


def generate_blocks(filepath):
    try:
        # Get the SHA256 hash of the whole file
        file_hash = calculate_file_hash(filepath)

        # Generate the necessary number of blocks for the file
        blocks = []
        with open(filepath, "rb") as file:
            # Calculate the number of blocks needed for this file
            filesize = os.path.getsize(filepath)
            index_all = filesize // 500 + (filesize % 500 > 0)

            # Create the first block of the given file
            chunk = file.read(500)
            first_block = Block(file_hash=file_hash,
                                index_all=index_all,
                                chunk=chunk,
                                hash_previous='0')
            blocks.append(first_block)

            # Process the rest of the file
            chunk = file.read(500)
            while chunk:
                blocks.append(Block(file_hash=file_hash,
                                    index_all=index_all,
                                    chunk=chunk,
                                    hash_previous=blocks[-1].generate_hash()))
                chunk = file.read(500)

        return blocks
    except IOError:
        print("Could not access file")
        return []


if __name__ == "__main__":
    pass
