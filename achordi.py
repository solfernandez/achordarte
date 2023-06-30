#!/usr/bin/env python3
from achordarte.main import main
import argparse

parser = argparse.ArgumentParser(
                    prog='Achordarte',
                    description='Find chords play on a MIDI instrument',
                    epilog='.')
parser.add_argument('-i', '--input-file', default='/dev/snd/midiC1D0')

#input_file = "/dev/snd/midiC1D0"
input_file = parser.parse_args().input_file
main(input_file)
