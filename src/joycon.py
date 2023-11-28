import color

class Joycon:
    FREQ_OFFSET = 36
    FREQ_OFFSET_MAX = 96
    freqs = [
        # C2 is 36
        65.41, 69.30, 73.42, 77.78, 82.41, 87.31, 92.50, 98.00, 103.83, 110.00, 116.54, 123.47,
        130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00, 233.08, 246.94,
        261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88,
        523.25, 554.37, 587.33, 622.25, 659.25, 698.46, 739.99, 783.99, 830.61, 880.00, 932.33, 987.77,
        1046.50, 1108.73, 1174.66, 1244.51, 1318.51, 1396.91, 1479.98, 1567.98, 1661.22, 1760.00, 1864.66, 1975.53,
        # C7 is 96
    ]

    def __init__(self, device_id, joycon_color=color.RED):
        self._timer = 0
        self._is_busy = False
        self._device_id = device_id
        self._buf = None
        self._color = joycon_color

        # buf = libjoycon.joycon_allocate_buffer(buffer_len)

        # Init handler
        try:
            print(f"Opening the device {device_id}")

            # h = hid.device()
            # h.open(0x57e, device_id, None)

            print("Open device")

            # TODO: Try to get color from joycon

            # libjoycon.joycon_packet_rumble_enable_only(buf, self._timer & 0xF)
            # h.write(buf2list(buf, buffer_len))

            # enable non-blocking mode
            # h.set_nonblocking(1)

            # self._handler = h
            # self._buf = buf
        except IOError as ex:
            print(ex)
            self._handler = None
            # libjoycon.joycon_free_buffer(buf)

    def is_busy(self):
        return self._is_busy
    
    def is_connected(self):
        # return self._handler is not None
        return True

    def note_off(self, note):
        if self._buf:
            try:
                self._timer += 1
                if note - JoyconNoteOutput.FREQ_OFFSET < len(JoyconNoteOutput.freqs):
                    libjoycon.joycon_packet_rumble_only(self._buf, self._timer & 0xF,\
                        JoyconNoteOutput.freqs[note - JoyconNoteOutput.FREQ_OFFSET], 0)
                    self._handler.write(buf2list(self._buf, buffer_len))
            except IOError as ex:
                print(ex)
        self._is_busy = False
        print(f"\tNote off {note}")

    def note_on(self, note, amp=0.5):
        if self._buf and (note - JoyconNoteOutput.FREQ_OFFSET) < len(JoyconNoteOutput.freqs):
            try:
                self._timer += 1
                libjoycon.joycon_packet_rumble_only(self._buf, self._timer & 0xF,\
                    JoyconNoteOutput.freqs[note - JoyconNoteOutput.FREQ_OFFSET], amp)
                self._handler.write(buf2list(self._buf, buffer_len))
            except IOError as ex:
                print(ex)
        self._is_busy = True
        print(f"\tNote on {note}")

    def get_color(self):
        return self._color
