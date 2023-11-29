#!/usr/bin/env python3
import logging
from achordarte.main import main
import argparse

parser = argparse.ArgumentParser(
                    prog='Achordarte',
                    description='Find chords play on a MIDI instrument',
                    epilog='.')
parser.add_argument('-i', '--input-file', default='/dev/snd/midiC1D0')
parser.add_argument('-v', '--verbosity', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='INFO')

level = parser.parse_args().verbosity

# create logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)
ch.setLevel(level)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


#input_file = "/dev/snd/midiC1D0"
input_file = parser.parse_args().input_file
logger.info('Start of execution')
main(input_file)
logger.info('End of execution')
