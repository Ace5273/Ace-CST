from abc import ABC, abstractmethod
from arcade import key

key_pressed_down = set()

pressing_key = set()
releasing_key = set()

class KeyHelper():

    @staticmethod
    def is_key_pressed_down(key):
        return key in key_pressed_down
    
    @staticmethod
    def is_pressing_key(key):
        return key in pressing_key

    @staticmethod
    def is_releasing_key(key):
        return key in releasing_key

    @staticmethod
    def press_key(key):

        # Currently pressing a key
        pressing_key.add(key)

        # The key is pressed down
        key_pressed_down.add(key)
    
    @staticmethod
    def release_key(key):
        
        # Currently releasing a key
        releasing_key.add(key)

        # The key isn't pressed down any more
        key_pressed_down.discard(key)
    
    @staticmethod
    def update():

        # Since there is an update
        # every pressing and releasing key
        # are now pressed down or not pressed down
        pressing_key.clear()
        releasing_key.clear()

    

class BaseKeyboard(ABC):

    keys = None

    def __init__(self, **keys):
        self.keys = keys
        pass
    
    @abstractmethod
    def is_key_pressed_down(self, key):
        pass
    
    @abstractmethod
    def is_key_pressing(self, key):
        pass
    
    @abstractmethod
    def is_key_releasing(self, key):
        pass
    
    def get_amount_of_keys(self):
        return len(self.keys)

class PlayerKeyboard(BaseKeyboard):
    
    def is_key_pressed_down(self, key):
        return KeyHelper.is_key_pressed_down(self.keys[key])
    
    def is_key_pressing(self, key):
        return KeyHelper.is_pressing_key(self.keys[key])

    def is_key_releasing(self, key):
        return KeyHelper.is_releasing_key(self.keys[key])

class BotKeyboard(BaseKeyboard):

    def __init__(self, **keys):
        super().__init__(keys)
        self.pressing_key = set()
        self.releasing_key = set()
    
    def is_key_pressed_down(self, key):
        return self.keys[key]
    
    def is_key_pressing(self, key):
        return KeyHelper.is_pressing_key(self.keys[key])

    def is_key_releasing(self, key):
        return KeyHelper.is_releasing_key(self.keys[key])
    
    def press_key(self, key: str):

        if self.is_key_pressed_down(key):
            self.pressing_key.add(key)
        elif key in pressing_key:
            self.pressing_key.discard(key)

        self.keys[key] = True
    
    def press_key_by_index(self, index: int):
        press_key(self.keys.keys[index])
    
    def release_key(self, key: str):

        if not self.is_key_pressed_down(key):
            self.releasing_key.add(key)
        elif key in releasing_key:
            self.releasing_key.discard(key)

        self.keys[key] = False
    
    def release_key_by_index(self, index: int):
        release_key(self.keys.keys[index])
    
    def press_all(self):
        for key in self.keys.keys:
            self.press_key(key)
    
    def release_all(self):
        for key in self.keys.keys:
            self.release_key(key)

WASDKeyboard    = PlayerKeyboard(up = key.W, down = key.S, left = key.A, right = key.D)
ArrowKeyboard   = PlayerKeyboard(up = key.UP, down = key.DOWN, left = key.LEFT, right = key.RIGHT)
BaseBotKeyboard = BotKeyboard(up = False, down = False, left = False, right = False)
BotLeftRightKeyboard = BotKeyboard(left = False, right = False)
