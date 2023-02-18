#!/usr/bin/env python3
from achordarte.notes import convert_midi_numero_de_tecla_to_note, VirtualInstrument, get_chord_name, Chord

NOTE_ON_MASK = 0x90

f = open("/dev/snd/midiC1D0", "rb")
virtual_instrument = VirtualInstrument()

while True:
    current_byte = f.read(1)
    # we are not interested in these MIDI events
    if current_byte in [b'\xf8', b'\xfe']:
        continue

    # get all Note On events from all MIDI channels
    # Note On: 0x90 to 0x9F where the low nibble is the MIDI channel.
    if ord(current_byte) & NOTE_ON_MASK == NOTE_ON_MASK:
        numero_de_tecla = ord(f.read(1))
        intensidad = ord(f.read(1))

        nota = convert_midi_numero_de_tecla_to_note(numero_de_tecla)
        if intensidad == 0:  # Es un Note off
            # print("Note OFF: nota=%r" % nota)
            virtual_instrument.process_note_off(nota)
        else:
            virtual_instrument.process_note_on(nota)
            # print("Note ON: nota=%r, intensidad=%r" % (nota, intensidad))
        print(virtual_instrument)
        current_notes = virtual_instrument.get_current_notes_as_list()
        if current_notes:
            print("\tchord: ", get_chord_name(Chord.from_notes(current_notes)))
