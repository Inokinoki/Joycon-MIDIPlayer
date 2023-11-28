from threading import Thread
import time

# White note/ black note pattern
PATTERN = [True, False, True, True, False, True, False, True, True, False, True, False]


class Note:
    def __init__(self, id):
        self.id = id
        self.playuntil = 0
        self.channel = 0
        self.velocity = 0
        self.particles = None
        self.is_on = False
        self.is_white = PATTERN[id % 12]
        self.joycon = None


class Piano(Thread):
    def __init__(self, notes):
        Thread.__init__(self)
        self.notes = notes
        self.running = True

    def run(self):
        delta = 0.01
        while self.running:
            tnow = time.time()
            for note in self.notes:
                if tnow < note.playuntil:
                    note.is_on = True
                else:
                    note.is_on = False
                    if note.joycon is not None:
                        joycon = note.joycon
                        note.joycon = None
                        joycon.note_off(0)  # TODO: note
            time.sleep(0.008)
            delta = time.time() - tnow

    def terminate(self):
        self.running = False
        self.join()
