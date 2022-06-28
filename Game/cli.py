import msvcrt
from key_bytes import BYTE_KEYS


class Wrapper:
    def __init__(self):
        self.binds = {}
        self.running = False
        self.items = []
    
    
    def bind(self, key: str | bytes | BYTE_KEYS, command: str) -> None:
        match key:
            case key if type(key) == BYTE_KEYS:
                pass
            
            case key if type(key) == bytes:
                pass
            
            case key if type(key) == str:
                key = bytes(key.encode('utf-8'))
                
        self.binds[key] = command
    
    def run(self, *args):
        self.running = True
        while self.running:
            key = msvcrt.getch()
            match key:
                case key if key in self.binds.keys():
                    cmd = self.binds[key]
                    exec(cmd)
                    
                case esc if esc == b'\x00':
                    key = msvcrt.getch()
                    cmd = self.binds[(b'\x00', key)]
                    exec(cmd)
                
                case _:
                    print(key)

                    
    
    def quit(self):
        self.running = False


class Grid:...


class Frame:...


if __name__ == '__main__':
    w = Wrapper()
    w.bind('q', 'self.quit()')
    w.bind(BYTE_KEYS.UP, 'UP!!!')
    w.run()