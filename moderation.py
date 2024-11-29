def linked_list(self, data):
    self.data = data
    self.next = None

def warn_user(user_inputs: str)-> str:
    banned_phrase = user_inputs
    if banned_phrase == 'dsfd':
        return
