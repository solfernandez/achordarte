import pytest
from achordarte.midi import VirtualInstrument, convert_midi_key_number_to_note
from achordarte.notes import (Interval,
                              c4, d4, e4, g4, d4_flat, c4_sharp, e4_flat, b4_flat, b4,
                              i3M, i3m, i5, notes_interval,
                              Note, Chord, classify_chord, major_chord, major_chord_maj7, major_chord_7, minor_chord,
                              minor_chord_7, get_chord_name)


def test_playing_with_the_instrument():
    vi = VirtualInstrument()
    assert vi.get_current_notes() == set()
    assert vi.get_current_notes_as_list() == []

    vi.process_note_on(d4)
    assert vi.get_current_notes() == {d4}

    vi.process_note_on(c4)
    assert vi.get_current_notes() == {c4, d4}
    assert vi.get_current_notes_as_list() == [c4, d4]

    vi.process_note_off(c4)
    assert vi.get_current_notes() == {d4}

    vi.process_note_off(e4)
    assert vi.get_current_notes() == {d4}


def test_notes():
    c4 = Note(semitones_to_c4=0)
    assert c4 == Note(semitones_to_c4=0)
    assert c4 != Note(semitones_to_c4=1)
    assert c4 != d4

    assert d4.base_name() == "d"
    b3 = Note(semitones_to_c4=-1)
    assert b3.base_name() == "b"

    # Enharmony test
    assert c4_sharp == d4_flat


def test_intervals():
    i3M = Interval(4)
    assert i3M == Interval(4)
    assert i3M != Interval(5)

    assert i3M == notes_interval(c4, e4)
    assert Interval(2) == notes_interval(c4, d4)


def test_notes_to_chords():
    assert Chord.from_notes([c4, e4, g4]) == Chord(c4, [i3M, i5])
    assert Chord.from_notes([c4]) == Chord(c4, [])
    assert Chord.from_notes([c4]).intervals == []

def test_chords_to_protochords():
    c_major = Chord.from_notes([c4, e4, g4])
    assert classify_chord(c_major) == major_chord

    c_major_7 = Chord.from_notes([c4, e4, g4, b4_flat])
    assert classify_chord(c_major_7) == major_chord_7

    c_major_maj7 = Chord.from_notes([c4, e4, g4, b4])
    assert classify_chord(c_major_maj7) == major_chord_maj7

    c_minor = Chord.from_notes([c4, e4_flat, g4])
    assert classify_chord(c_minor) == minor_chord

    c_minor_7 = Chord.from_notes([c4, e4_flat, g4, b4_flat])
    assert classify_chord(c_minor_7) == minor_chord_7

def test_chord_naming():
    assert get_chord_name(Chord.from_notes([c4, e4, g4])) == "C"
    assert get_chord_name(Chord(c4, [i3m, i5])) == "Cm"
    assert get_chord_name(Chord.from_notes([c4, e4, g4, b4_flat])) == 'C7'
    assert get_chord_name(Chord.from_notes([c4, e4, g4, b4])) == 'Cmaj7'
    assert get_chord_name(Chord.from_notes([c4, e4_flat, g4, b4_flat])) == 'Cm7'


def test_midi_to_notes():
    d3 = Note(semitones_to_c4=-10)
    assert convert_midi_key_number_to_note(60) == c4
    assert convert_midi_key_number_to_note(50) == d3


#def test_file_to_chords():
#    chords = chordify_file("tests/song.rec")
#    c_major = Chord.from_notes([c4, e4, g4])
#    c_minor = Chord.from_notes([c4, e4_flat, g4])
#    assert chords == [c_major, c_minor]