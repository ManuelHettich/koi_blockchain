import os
import hashlib


class Block:
    def __init__(self, file_hash, index_all, chunk, hash_previous):
        self.hash = file_hash
        self.index_all = index_all
        self.chunk = chunk
        self.hash_previous = hash_previous

    def generate_hash(self):
        block_hash = hashlib.sha256()
        block_hash.update(bytes(self.hash, 'utf-8'))
        block_hash.update(bytes(str(self.index_all), 'utf-8'))
        block_hash.update(self.chunk)
        block_hash.update(bytes(self.hash_previous, 'utf-8'))
        return block_hash.hexdigest()

    @staticmethod
    def generate_blocks(filepath):
        try:
            # Calculate the number of blocks needed for this file
            filesize = os.path.getsize(filepath)
            num_blocks = filesize // 500 + (filesize % 500 > 0)

            # Calculate the hash for the file overall
            buffer_size = 1024 * 1024
            sha256 = hashlib.sha256()
            with open(filepath, "rb") as file:
                while True:
                    file_buffer = file.read(buffer_size)
                    if not file_buffer:
                        break
                    sha256.update(file_buffer)
            file_hash = sha256.hexdigest()

            # Generate the necessary number of blocks for the file
            blocks = []
            with open(filepath, "rb") as file:
                # Create the first block
                chunk = file.read(500)
                blocks.append(Block(file_hash=file_hash,
                                    index_all=num_blocks,
                                    chunk=chunk,
                                    hash_previous='0'))

                # Process the rest of the file
                chunk = file.read(500)
                while chunk:
                    blocks.append(Block(file_hash=file_hash,
                                        index_all=num_blocks,
                                        chunk=chunk,
                                        hash_previous=blocks[-1].generate_hash()))
                    chunk = file.read(500)

            return blocks
        except IOError:
            print("Could not access file")
            return []


if __name__ == "__main__":
    Block.generate_blocks("test_files/isaac-martin-61d2hT57MAE-unsplash.jpg")
