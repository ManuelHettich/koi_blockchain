"""
This module provides the Block class and several helper functions.
"""

import os
import hashlib


class Block:
    """
    The Block object contains all the necessary attributes as required by
    the project specification and it can generate its own hash as well
    as check the integrity of a file when provided a list of Block objects.

    :param file_hash: Hash of the original file
    :param index_all: The amount of blocks of the original file
    :param chunk: A 500 byte chunk of the original file
    :param hash_previous: The hash of the previous Block object in the chain
                          (the first Block contains a '0')
    """

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
        Generate a SHA256 hash of the given block instance, using its four attributes:
        hash, index_all, chunk and hash_previous.

        :return: SHA256 hash of this block instance using all its attributes.
        """
        block_hash = hashlib.sha256()
        block_hash.update(bytes(self.hash, 'utf-8'))
        block_hash.update(bytes(str(self.index_all), 'utf-8'))
        block_hash.update(self.chunk)
        block_hash.update(bytes(self.hash_previous, 'utf-8'))
        return block_hash.hexdigest()

    def check_file_integrity(self, blocks_of_file, file_hash, index_all):
        """
        Check if all the blocks belonging to this first block of a file have a valid
        integrity. This method must be called on the first block of a file and it only
        returns True if each block contains the correct hash of the original file
        (SHA256 checksum), there are a correct number of blocks and they reference
        each other correctly in a sequential way using their individual hashes.

        :param blocks_of_file: A list of all the blocks of the file
        :param file_hash: The original hash (SHA256 checksum) of the file
        :param index_all: The original number of blocks of the file
        :return: A boolean statement about whether the file has a valid integrity
        """

        # Check the number of blocks of the original file
        if len(blocks_of_file) != index_all:
            # The number of blocks does not match the original count
            return False

        # Check if each block of the given file references the correct hashes and number of blocks
        # Check the first block
        if (self.index_all != index_all or
                self.hash_previous != '0'):
            return False
        # Finish if there was only one block
        if len(blocks_of_file) == 1:
            # The file has only one block and it was already correctly checked
            return True

        # Check the second block
        second_block = blocks_of_file[1]
        if (second_block.index_all != index_all or
                second_block.hash != file_hash or
                second_block.hash_previous != self.generate_hash()):
            return False

        # Check the rest of the blocks
        for block_idx, block in list(enumerate(blocks_of_file))[2:]:
            if (block.index_all != index_all or
                    block.hash != file_hash or
                    block.hash_previous != blocks_of_file[block_idx - 1].generate_hash()):
                return False

        # All checks passed for this file
        return True


def calculate_file_hash(filepath):
    """
    Calculate the SHA256 checksum hash of a given file.

    :param filepath: Relative path to the file
    :return: SHA256 checksum hash of the file
    """

    # Calculate the hash (SHA256 checksum) for a given file
    buffer_size = 1024 * 2048
    sha256 = hashlib.sha256()

    with open(filepath, "rb") as file:
        while True:
            # Only read in 2 MB at a time to minimise memory usage
            file_buffer = file.read(buffer_size)
            if not file_buffer:
                break
            sha256.update(file_buffer)
    return sha256.hexdigest()


def generate_blocks(filepath):
    """
    Generate all the necessary Block objects of a given file by splitting
    the files into many 500 byte sized chunks.

    :param filepath: Relative path to the file
    :return: A list of all the Block objects of the given file
    """

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


if __name__ == "__main__":
    pass
