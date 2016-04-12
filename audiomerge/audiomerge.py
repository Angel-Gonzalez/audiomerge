#!/usr/bin/env python3
import os
import sys
from optparse import OptionParser, OptParseError
from collections import OrderedDict
from datetime import datetime
from pydub import AudioSegment


def main():
    parser = OptionParser(usage="usage: %prog [options] arg [audio files]", description="Merge and join audio files")
    parser.add_option("-m", "--merge", action="store_true",
                      help="Merge the audio files passed as args, all files will start at 0 sg")
    parser.add_option("-j", "--join", action="store_true",
                      help="Joins the audio files passed as args in the same order")
    parser.add_option("-d", "--destination", action="store",
                      help="Set destination path, current folder as default")
    parser.add_option("-o", "--output", action="store", help="Output file name, date string as default")
    try:
        opts, args = parser.parse_args()
    except OptParseError as e:
        print(e)
        sys.exit(2)
    # Input verifications
    if opts.join is None and opts.merge is None:
        print("Choose -j to Join 2 or more file either -m to merge those files")
        sys.exit(1)
    if opts.output is None:
        opts.output = str(datetime.now()) + '.mp3'
    if opts.destination is None:
        opts.destination = os.getcwd()
    # If merge option was choose
    if opts.merge is True and opts.join is None:
        audio_list = {}
        # Read audio sequences and order it from larger to shorter
        for arg in args:
            segment = AudioSegment.from_file(arg, format=str(arg).split(".")[1])
            audio_list[int(segment.duration_seconds)] = segment
        ordered_segments = OrderedDict(sorted(audio_list.items(), key=lambda t: t[0], reverse=True))
        first = True
        for k, seg in ordered_segments.items():
            if first is True:
                # Create a silent base audio of length from the longest sequence from the loaded list
                audio = AudioSegment.silent(duration=k * 1000)
                first = False
            audio = audio.overlay(seg)
        # Save the audio results
        audio.export(opts.destination + opts.output, format=str(opts.output).split(".")[1])
        # Print the full path of the created audio file
        print(opts.destination + opts.output)
    if opts.join is True and opts.merge is None:
        # Create a 0 seg long sequence for base
        audio = AudioSegment.empty()
        for arg in args:
            # Load and attach the list of sequences given as args
            audio += AudioSegment.from_file(arg, format=str(arg).split(".")[1])
        # Save the audio results
        audio.export(opts.destination + opts.output, format=str(opts.output).split(".")[1])
        # Print the full path of the created audio file
        print(opts.destination + opts.output)


if __name__ == '__main__':
    main()
