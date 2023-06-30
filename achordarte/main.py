#!/usr/bin/env python3
from achordarte.notes import get_chord_name, Chord
from achordarte.midi import convert_midi_key_number_to_note, VirtualInstrument, MIDIEvent, MIDI_NOTE_ON_BITMASK, MIDI_NOTE_OFF_BITMASK
import logging


#TODO: ESCRIBIR TEST DEL PROCESS_NOTE_OFF (QUE TESTEE LA LECTURA DE BYTES)

logger = logging.getLogger(__name__)


def main(input_file):
    f = open(input_file, "rb")
    virtual_instrument = VirtualInstrument()
    chords = []
    while True:
        current_byte = f.read(1)
        logger.debug("current byte: %s", current_byte)
        if current_byte == b'':
            break
        # we are not interested in these MIDI events
        if current_byte in [b'\xf8', b'\xfe']:
            continue

        midi_event = None
        # Note On: 0x90 to 0x9F where the low nibble is the MIDI channel.
        # Note Off: 0x80 to 0x8F where the low nibble is the MIDI channel.
        if ord(current_byte) & 0xF0 == MIDI_NOTE_ON_BITMASK:
            midi_event = MIDIEvent.NOTE_ON
        elif ord(current_byte) & 0xF0 == MIDI_NOTE_OFF_BITMASK:
            midi_event = MIDIEvent.NOTE_OFF

        if midi_event in [MIDIEvent.NOTE_ON, MIDIEvent.NOTE_OFF]:
            key_number = ord(f.read(1))
            intensity = ord(f.read(1))
            logger.debug("intensity: %s", intensity)

            note = convert_midi_key_number_to_note(key_number)
            if midi_event is MIDIEvent.NOTE_OFF or (midi_event is MIDIEvent.NOTE_ON and intensity == 0):
                logger.debug("Note OFF: note=%r", note)
                virtual_instrument.process_note_off(note)
            else:
                virtual_instrument.process_note_on(note)
            logger.debug("%r", virtual_instrument)
            current_notes = virtual_instrument.get_current_notes_as_list()
            if current_notes:
                chord = Chord.from_notes(current_notes)
                chord_name = get_chord_name(chord)
                if chord_name:
                    print("\tchord: ", chord_name)
                    chords.append(chord)
    return chords

