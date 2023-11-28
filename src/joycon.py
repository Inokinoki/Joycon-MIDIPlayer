import color

class Joycon:

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
