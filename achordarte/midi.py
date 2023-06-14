import enum
from achordarte.notes import Note

MIDI_C4_NUMBER = 60
MIDI_NOTE_ON_BITMASK = 0x90
MIDI_NOTE_OFF_BITMASK = 0x80

def convert_midi_key_number_to_note(key_number):
    return Note(semitones_to_c4=key_number - MIDI_C4_NUMBER)

class MIDIEvent(enum.Enum):
    NOTE_ON = 1
    NOTE_OFF = 2

class VirtualInstrument:
    def __init__(self):
        self.current_notes = set()

    def __repr__(self):
        return 'VirtualInstrument: ' + repr(sorted(self.current_notes))

    def process_note_on(self, note):
        self.current_notes.add(note)

    def process_note_off(self, note):
        if note in self.current_notes:
            self.current_notes.remove(note)

    def get_current_notes(self):
        return self.current_notes

    def get_current_notes_as_list(self):
        return sorted(list(self.current_notes))
