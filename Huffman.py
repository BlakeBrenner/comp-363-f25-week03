# ==========================
# Huffman Encoding in Python
# ==========================

# ----- Node Class -----
class Node:
    """Simple binary tree node for Huffman encoding"""

    def __init__(self, frequency: int, symbol: str | None = None):
        """Initialize a new node."""
        self.__frequency = frequency
        self.__symbol = symbol
        self.__left = None
        self.__right = None

    # -- Setters -- #
    def set_left(self, child) -> None:
        self.__left = child

    def set_right(self, child) -> None:
        self.__right = child

    # -- Getters -- #
    def get_frequency(self) -> int:
        return self.__frequency

    def get_symbol(self) -> str:
        return self.__symbol

    def get_left(self):
        return self.__left

    def get_right(self):
        return self.__right

    # -- Overloaded operators -- #
    def __str__(self) -> str:
        return f"({self.__symbol}:{self.__frequency})"

    def __repr__(self) -> str:
        return self.__str__()

    def __lt__(self, other: "Node") -> bool:
        return self.__frequency < other.__frequency


# ----- Constants -----
ASCII_SYMBOLS = 256


# ----- Step 1: Filter input -----
def filter_uppercase_and_spaces(input_string):
    """Keep only uppercase letters and spaces."""
    return ''.join([char for char in input_string if char.isupper() or char == ' '])


# ----- Step 2: Frequency of symbols -----
def frequency_of_symbols(message: str) -> list[int]:
    """Return a list of frequencies for all ASCII characters."""
    frequencies = [0] * ASCII_SYMBOLS
    for char in message:
        ascii_value = ord(char)
        frequencies[ascii_value] += 1
    return frequencies


# ----- Step 3: Create initial forest -----
def create_forest(frequencies):
    """Create a list of leaf nodes for characters that appear at least once."""
    forest = []
    for ascii_val in range(len(frequencies)):
        if frequencies[ascii_val] > 0:
            forest.append(Node(frequencies[ascii_val], chr(ascii_val)))
    return forest


# ----- Step 4: Get smallest node -----
def get_smallest(forest):
    """Pop and return the smallest node in the forest."""
    smallest_index = 0
    for i in range(1, len(forest)):
        if forest[i] < forest[smallest_index]:
            smallest_index = i
    return forest.pop(smallest_index)


# ----- Step 5: Build Huffman tree -----
def huffman(forest):
    """Build the Huffman tree from the initial forest."""
    if len(forest) == 0:
        return None
    while len(forest) > 1:
        s1 = get_smallest(forest)
        s2 = get_smallest(forest)
        new_node = Node(s1.get_frequency() + s2.get_frequency())
        new_node.set_left(s1)
        new_node.set_right(s2)
        forest.append(new_node)
    return forest[0]  # Root node


# ----- Step 6: Build encoding table -----
def build_encoding_table(root):
    """Generate a dictionary mapping symbols to Huffman codes."""
    table = {}

    def traverse(node, current_code=""):
        if node is None:
            return
        if node.get_symbol() is not None:
            table[node.get_symbol()] = current_code
            return
        traverse(node.get_left(), current_code + "0")
        traverse(node.get_right(), current_code + "1")

    traverse(root)
    return table


# ----- Step 7: Encode using table -----
def encode_with_table(message, table):
    """Encode a message using the precomputed Huffman table."""
    return ''.join(table[char] for char in message)


# ----- Step 8: Build reverse table -----
def build_reverse_table(table):
    """Create reverse lookup: Huffman code -> character."""
    return {code: symbol for symbol, code in table.items()}


# ----- Step 9: Decode using reverse table -----
def decode_with_table(encoded_message, reverse_table):
    """Decode an encoded message using the reverse table."""
    decoded = []
    current_bits = ""

    for bit in encoded_message:
        current_bits += bit
        if current_bits in reverse_table:
            decoded.append(reverse_table[current_bits])
            current_bits = ""

    return ''.join(decoded)


# ==========================
# Run Example
# ==========================
if __name__ == "__main__":
    message_to_compress = "HELLO WORLD"

    # Step A: Filter the message
    filtered_message = filter_uppercase_and_spaces(message_to_compress)

    # Step B: Build frequency table
    frequencies = frequency_of_symbols(filtered_message)

    # Step C: Build forest and Huffman tree
    forest = create_forest(frequencies)
    tree_root = huffman(forest)

    # Step D: Build encoding table
    encoding_table = build_encoding_table(tree_root)
    print("Encoding Table:", encoding_table)

    # Step E: Encode the message
    encoded_message = encode_with_table(filtered_message, encoding_table)
    print("Encoded Message:", encoded_message)

    # Step F: Build reverse table and decode
    reverse_table = build_reverse_table(encoding_table)
    decoded_message = decode_with_table(encoded_message, reverse_table)
    print("Decoded Message:", decoded_message)

    # Verify correctness
    assert decoded_message == filtered_message, "Decoding failed!"
    print("Compression and Decompression successful!")
