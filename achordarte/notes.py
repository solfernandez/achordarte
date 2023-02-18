import math

MIDI_C4_NUMBER = 60
ordered_note_names = ['do', 'do#', "re", "re#", "mi", "fa", "fa#", "sol", "sol#", "la", "la#", "si"]


def convert_midi_numero_de_tecla_to_note(numero_de_tecla):
    return Note(semitones_to_c4=numero_de_tecla - MIDI_C4_NUMBER)


class Note:
    def __init__(self, semitones_to_c4):
        self.semitones_to_c4 = semitones_to_c4

    def __lt__(self, other):
        return self.semitones_to_c4 < other.semitones_to_c4

    def __eq__(self, other):
        return self.semitones_to_c4 == other.semitones_to_c4

    def __hash__(self):
        return self.semitones_to_c4

    def base_name(self):
        return ordered_note_names[self.semitones_to_c4 % 12]

    def octave(self):
        return math.floor((self.semitones_to_c4 / 12)) + 4

    def __repr__(self):
        return f"Note({self.base_name()}{self.octave()})"


class Interval:
    def __init__(self, semitones):
        self.semitones = semitones

    def __eq__(self, other):
        return self.semitones == other.semitones

def notes_interval(note_from, note_to):
    return Interval(note_to.semitones_to_c4 - note_from.semitones_to_c4)


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


class Chord:
    def __init__(self, base_note, intervals):
        self.base_note = base_note
        self.intervals = intervals

    @classmethod
    def from_notes(cls, notes):
        base_note = notes[0]
        intervals = [notes_interval(base_note, note) for note in notes[1:]]
        return Chord(base_note, intervals)

    def __eq__(self, other):
        return self.base_note == other.base_note and self.intervals == other.intervals

class ProtoChord:
    def __init__(self, intervals):
        self.intervals = intervals

    def __eq__(self, other):
        if hasattr(other, 'intervals'):
            return self.intervals == other.intervals
        else:
            return False

    def __hash__(self):
        return id(self)


i3m = Interval(semitones=3)
i3M = Interval(semitones=4)
i5 = Interval(semitones=7)
major_chord = ProtoChord([i3M, i5])
minor_chord = ProtoChord([i3m, i5])

chord_types = {major_chord, minor_chord}

def classify_chord(chord):
    protochord = ProtoChord(chord.intervals)
    for chord_type in chord_types:
        if chord_type == protochord:
            return chord_type

def get_chord_name(chord):
    chord_type = classify_chord(chord)
    if chord_type == major_chord:
        return chord.base_note.base_name().capitalize()
    elif chord_type == minor_chord:
        return chord.base_note.base_name().capitalize() + "m"


c4, d4, e4, fa4, g4, la4, si4 = Note(0), Note(2), Note(4), Note(5), Note(7), Note(9), Note(11)
do4_sharp, re4_sharp, mi4_sharp, fa4_sharp, sol4_sharp, la4_sharp, si4_sharp = Note(1), Note(3), Note(5), Note(6), Note(8), Note(10), Note(12)
do4_flat, re4_flat, mi4_flat, fa4_flat, sol4_flat, la4_flat, si4_flat = Note(-1), Note(1), Note(3), Note(4), Note(6), Note(8), Note(10)
