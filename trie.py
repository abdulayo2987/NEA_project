#TODO write about this data structure inside the NEA document degsin and analysis

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
            if character in current_node.children:              #if the character is not in the children nodes
                current_node.children[character] = trie_node()  #add the character as a key and set make it point to a new node
            current_node = current_node.children[character]     #set this node as the current node regardless of if it is a new character or not 
        current_node.is_end_of_word = True


    def search(self, word:str):
        current_node = self.root
        for character in word:
            if character not in current_node.children:
                return False
            current_node = current_node[character]
        return current_node.is_end_of_word

    def delete_helper_function(self, current_node, word:str, index):
        pass

    def delete(self, word:str):
        self.delete_helper_function(self.root, word, 0)

        #https://youtu.be/y3qN18t-AhQ?t=850

    

    def list_words(self):
        pass