import math

ordered_note_names = ['c', 'c#', "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]


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
    def __init__(self, name, intervals):
        self.name = name
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
i7m = Interval(semitones=10)
i7M = Interval(semitones=11)
i9 = Interval(semitones=14)

major_chord = ProtoChord('', [i3M, i5])
major_chord_7 = ProtoChord('7', [i3M, i5, i7m])
major_chord_7_9 = ProtoChord('9', [i3M, i5, i7m, i9])
major_chord_maj7 = ProtoChord('maj7', [i3M, i5, i7M])
minor_chord = ProtoChord('m', [i3m, i5])
minor_chord_7 = ProtoChord('m7', [i3m, i5, i7m])

chord_types = {major_chord, major_chord_7, major_chord_7_9, major_chord_maj7, minor_chord, minor_chord_7}

def classify_chord(chord):
    protochord = ProtoChord('unknown', chord.intervals)
    for chord_type in chord_types:
        if chord_type == protochord:
            return chord_type

def get_chord_name(chord):
    chord_type = classify_chord(chord)
    return chord.base_note.base_name().capitalize() + chord_type.name

c4, d4, e4, f4, g4, a4, b4 = Note(0), Note(2), Note(4), Note(5), Note(7), Note(9), Note(11)
c4_sharp, d4_sharp, e4_sharp, f4_sharp, g4_sharp, a4_sharp, b4_sharp = Note(1), Note(3), Note(5), Note(6), Note(8), Note(10), Note(12)
c4_flat, d4_flat, e4_flat, f4_flat, g4_flat, a4_flat, b4_flat = Note(-1), Note(1), Note(3), Note(4), Note(6), Note(8), Note(10)
