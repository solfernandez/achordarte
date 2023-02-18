import pytest
from achordarte.notes import (VirtualInstrument, Interval,
                              c4, d4, e4, g4, re4_flat, do4_sharp, mi4_flat,
                              i3M, i3m, i5, notes_interval,
                              Note, Chord, classify_chord, major_chord, minor_chord, get_chord_name,
                              convert_midi_numero_de_tecla_to_note)


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
    do4 = Note(semitones_to_c4=0)
    assert do4 == Note(semitones_to_c4=0)
    assert do4 != Note(semitones_to_c4=1)
    assert do4 != d4

    assert d4.base_name() == "re"
    b3 = Note(semitones_to_c4=-1)
    assert b3.base_name() == "si"

    # Enharmony test
    assert do4_sharp == re4_flat


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
    do_mayor = Chord.from_notes([c4, e4, g4])
    assert classify_chord(do_mayor) == major_chord

    do_menor = Chord.from_notes([c4, mi4_flat, g4])
    assert classify_chord(do_menor) == minor_chord

def test_chord_naming():
    assert get_chord_name(Chord.from_notes([c4, e4, g4])) == "Do"
    assert get_chord_name(Chord(c4, [i3m, i5])) == "Dom"

def test_midi_to_notes():
    d3 = Note(semitones_to_c4=-10)
    assert convert_midi_numero_de_tecla_to_note(60) == c4
    assert convert_midi_numero_de_tecla_to_note(50) == d3


def test_file_to_chords():
    chords = chordify_file("tests/song.rec")
    do_mayor = Chord.from_notes([c4, e4, g4])
    do_menor = Chord.from_notes([c4, mi4_flat, g4])
    assert chords == [do_mayor, do_menor]