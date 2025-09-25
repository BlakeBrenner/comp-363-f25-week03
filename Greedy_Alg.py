from Node import Node

def filter_uppercase_and_spaces(input_string: str) -> str:
    """
    Filters the input string to retain only uppercase letters and spaces.
    """
    return "".join(
        char for char in input_string.upper() if char.isalpha() or char == " "
    )

def count_frequencies(input_string: str) -> list[int]:
    """
    Counts the frequency of each uppercase letter in the input string.
    Returns a list of 26 integers, where index 0-25 correspond to 'A'-'Z'.
    You can assume the input string contains only uppercase letters and spaces.
    And that spaces are the most frequent character, so really we dont need
    to count them.
    """
    frequencies = [0] * 27
    for char in input_string:
        if char == " ":
            frequencies[26] += 1 
        else:
            index = ord(char) - ord("A")
            frequencies[index] += 1
    return frequencies



def initialize_forest(frequencies: list[int]) -> list[Node]:
    """
    Initializes a forest (list) of Node objects for each character with a non-zero frequency.
    """
    forest = []
    for i, freq in enumerate(frequencies):
        if freq > 0:
            symbol = " " if i ==26 else chr(i + ord("A"))
            forest.append(Node(freq, symbol))
    return forest

def get_smallest(forest: list[Node]) -> Node:
    smallest_index = 0
    for i in range(1, len(forest)):
        if forest[i] < forest[smallest_index]:
            smallest_index = i
    return forest.pop(smallest_index)


def build_huffman_tree(frequencies: list[int]) -> Node:
    """
    Builds the Huffman tree from the list of frequencies and returns the root Node.
    """
    forest = initialize_forest(frequencies)
    if len(forest) == 0:
        return None # Handle empty input

    while len(forest) > 1:
        # Extract two smallest nodes
        s1 = get_smallest(forest)
        s2 = get_smallest(forest)

        # Create a new internal node
        new_node = Node(s1.get_frequency()+s2.get_frequency())
        new_node.set_left(s1)
        new_node.set_right(s2)

        forest.append(new_node)

    return forest[0] # Root of Huffman Tree


def build_encoding_table(huffman_tree_root: Node) -> list[str]:
    """
    Builds the encoding table from the Huffman tree.
    Returns a list of 27 strings, where index 0-25 correspond to 'A'-'Z'
    and index 26 corresponds to space.
    Each string is the binary encoding for that character.
    """
    table = [""] * 27

    def traverse(node: Node, code: str):
        if node is None:
            return
        if node.get_symbol() is not None:
            # Leaf node: assign code
            symbol = node.get_symbol()
            index = 26 if symbol == " " else ord(symbol) - ord("A")
            table[index] = code
            return
    
        #Traverse left and right
        traverse(node.get_left(), code + "0")
        traverse(node.get_right(), code + "1")

    traverse(huffman_tree_root, "")
    return table

def encode(input_string: str, encoding_table: list[str]) -> str:
    """
    Encodes the input string using the provided encoding table. Remember
    that the encoding table has 27 entries, one for each letter A-Z and
    one for space. Space is at the last index (26).
    """
    encoded = []
    for char in input_string:
        if char == " ":
            encoded.append(encoding_table[26])
        else:
            index = ord(char) - ord("A")
            encoded.append(build_encoding_table[index])
    return "".join(encoded)


def decode(encoded_string: str, huffman_root: Node) -> str:
    """
    Decodes the encoded string using the Huffman table as a key.
    """
    decoded = []
    current = huffman_root

    for bit in encoded_string:
        if bit == "0":
            current = current.get_left()
        elif bit == "1":
            current = current.get_right()
        
        if current.get_symbol() is not None:
            decoded.append(current.get_symbol)
            current = huffman_root
    return "".join(decoded)

if __name__ == "__main__":
    message = "HELLO WORLD"
    filtered = filter_uppercase_and_spaces(message)

    print("Filtered Message:", filtered)

    # Step 1: Count frequencies
    frequencies = count_frequencies(filtered)
    print("Frequencies:", frequencies)

    # Step 2: Build Huffman tree
    root = build_huffman_tree(frequencies)

    # Step 3: Build encoding table
    table = build_encoding_table(root)
    print("Encoding Table:", table)

    # Step 4: Encode message
    encoded = encode(filtered, table)
    print("Encoded Message:", encoded)

    # Step 5: Decode message
    decoded = decode(encoded, root)
    print("Decoded Message:", decoded)

    # Verify correctness
    assert decoded == filtered, "Error: Decoded message does not match original!"
    print("Compression and Decompression successful!")     