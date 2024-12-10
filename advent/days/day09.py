from typing import TextIO

ExpandedDisk = list[None | int]
Block = tuple[None | int, int]
ExpandedDiskV2 = list[Block]


def expand_disk(compressed: list[int]) -> ExpandedDisk:
    expanded = []
    block_index = 0
    is_block = True

    for n in compressed:
        expanded.extend([block_index if is_block else None] * n)

        if is_block:
            block_index += 1
        is_block = not is_block

    return expanded


def pack(expanded: ExpandedDisk) -> None:
    left = 0
    right = len(expanded) - 1

    while left < right:
        while expanded[left] is not None and left < right:
            left += 1
        while expanded[right] is None and left < right:
            right -= 1

        if left < right and expanded[left] is None and expanded[right] is not None:
            expanded[left], expanded[right] = expanded[right], expanded[left]


def expand_disk2(compressed: list[int]) -> ExpandedDiskV2:
    expanded = []
    block_index = 0
    is_block = True

    for n in compressed:
        expanded.append((block_index if is_block else None, n))

        if is_block:
            block_index += 1
        is_block = not is_block

    return expanded


def pack2(expanded: ExpandedDiskV2) -> None:
    file_index = None
    max_file_id = None

    # Find the rightmost block index, it's the biggest file id (N)
    for i, b in enumerate(reversed(expanded)):
        if b[0] is not None:
            max_file_id = b[0]
            file_index = len(expanded) - 1 - i
            break

    assert max_file_id is not None

    # We have to try to move files N to 1 to the leftmost empty block that can fit them
    for file_id in range(max_file_id, 0, -1):
        # Find the next block to move
        curr_file_id, size = expanded[file_index]
        while curr_file_id != file_id:
            file_index -= 1
            curr_file_id, size = expanded[file_index]

        # Otherwise it means it was not found
        assert curr_file_id == file_id

        # Find a spot to put it
        i = 0
        while i < file_index:
            candidate_file_id, candidate_size = expanded[i]
            if candidate_file_id is not None or candidate_size < size:
                i += 1
                continue
            break

        if i >= file_index:
            # We couldn't put it anywhere to the left
            continue

        extra = candidate_size - size
        expanded[i] = (file_id, size)
        expanded[file_index] = (None, size)

        # if extra we need to create a new block to the right
        if extra > 0:
            expanded.insert(i + 1, (None, extra))


def first(input: TextIO) -> int:
    disk_map = [int(c) for c in input.read().strip()]
    expanded = expand_disk(disk_map)
    pack(expanded)
    return sum(i * n for i, n in enumerate(expanded) if n is not None)


def second(input: TextIO) -> int:
    disk_map = [int(c) for c in input.read().strip()]
    expanded = expand_disk2(disk_map)
    pack2(expanded)

    # Compute the checksum, it's a little more annoying now
    i = 0
    total = 0
    for file_id, size in expanded:
        for _ in range(size):
            total += (0 if file_id is None else file_id) * i
            i += 1
    return total
