from abc import ABC, abstractmethod
from arcade import key

key_down = set()

pressing_key = set()
releasing_key = set()

class KeyHelper():

    @staticmethod
    def is_key_down(key):
        return key in key_down

    @staticmethod
    def is_key_up(key):
        return key not in key_down
    
    @staticmethod
    def is_pressing_key(key):
        return key in pressing_key

    @staticmethod
    def is_releasing_key(key):
        return key in releasing_key

    @staticmethod
    def press_key(key):
        
        if(KeyHelper.is_key_up(key)):
            pressing_key.add(key)
        elif(key in pressing_key):
            pressing_key.remove(key)        

        key_down.add(key)
    
    @staticmethod
    def release_key(key):
        
        if(KeyHelper.is_key_down(key)):
            releasing_key.add(key)
        elif(key in releasing_key):
            releasing_key.remove(key)   
        
        key_down.remove(key)

    

class BaseKeyboard(ABC):

    keys = None

    def __init__(self, **keys):
        self.keys = keys
        pass

    @abstractmethod
    def is_key_up(self, key):
        pass
    
    @abstractmethod
    def is_key_down(self, key):
        pass
    
    @abstractmethod
    def is_key_pressing(self, key):
        pass
    
    @abstractmethod
    def is_key_releasing(self, key):
        pass

class PlayerKeyboard(BaseKeyboard):

    def is_key_up(self, key):
        return KeyHelper.is_key_up(self.keys[key])
    
    def is_key_down(self, key):
        return KeyHelper.is_key_down(self.keys[key])
    
    def is_key_pressing(self, key):
        return KeyHelper.is_pressing_key(self.keys[key])

    def is_key_releasing(self, key):
        return KeyHelper.is_releasing_key(self.keys[key])

class BotKeyboard(BaseKeyboard):

    pressing_key = set()
    releasing_key = set()

    def is_key_up(self, key):
        return not self.keys[key]
    
    def is_key_down(self, key):
        return self.keys[key]
    
    def is_key_pressing(self, key):
        return KeyHelper.is_pressing_key(self.keys[key])

    def is_key_releasing(self, key):
        return KeyHelper.is_releasing_key(self.keys[key])
    
    def press_key(self, key):

        if self.is_key_up(key):
            pressing_key.add(key)
        elif key in pressing_key:
            pressing_key.remove(key)

        self.keys[key] = True
    
    def release_key(self, key):

        if self.is_key_up(key):
            releasing_key.add(key)
        elif key in releasing_key:
            releasing_key.remove(key)

        self.keys[key] = False

AWSDKeyboard    = PlayerKeyboard(up = key.W, down = key.S, left = key.A, right = key.D)
ArrowKeyboard   = PlayerKeyboard(up = key.UP, down = key.DOWN, left = key.LEFT, right = key.RIGHT)
BaseBotKeyboard = BotKeyboard(up = False, down = False, left = False, right = False)
