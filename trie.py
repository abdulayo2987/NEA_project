

class trie_node:
    def __init__(self):
        self.children = dict()
        self.is_end_of_word = False

class trie:
    def __init__(self):
        self.root = trie_node()

    def insert(self, word:str) -> None:
        current_node = self.root
        
        for character in word:
            if character not in current_node.children:        
                current_node.children[character] = trie_node() 
            current_node = current_node.children[character]
        current_node.is_end_of_word = True


    def search(self, word:str):
        current_node = self.root
        for character in word:
            if character not in current_node.children:
                return False
            current_node = current_node.children[character]
        return current_node.is_end_of_word

    def delete_helper_function(self, current_node, word:str, index):
        if index == len(word):
            if not current_node.is_end_of_word:
                return False
            current_node.is_end_of_word = False
            return len(current_node.children) == 0
        character = word[index]
        node = current_node.children.get(character)

        if node is None:
            return False
        delete_current_node = self.delete_helper_function(node, word, index + 1)
        if delete_current_node:
            del current_node.children[character]
        return len(current_node.children) == 0 and not current_node.is_end_of_word


    def delete(self, word:str):
        self.delete_helper_function(self.root, word, 0)

    def list_words(self):
        words = []
        def traverse(current_node, word):
            if current_node.is_end_of_word:
                words.append("".join(word))
            for character, child in current_node.children.items():
                traverse(child, word + [character])

        traverse(self.root, [])
        return (f"The following words are banned: {words}")

