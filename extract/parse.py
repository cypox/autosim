#!/usr/bin/python3
import sys

def key_to_text(key):
  return key.split('|')[1].rstrip().lstrip()

def parse_report(filename = 'utilization_synth.rpt'):

  keywords_map = {
    #utilization report keys
    '| Slice LUTs*             |'    : 0,
    '| Slice Registers         |'    : 0,
    '| F7 Muxes                |'    : 0,
    '| F8 Muxes                |'    : 0,
    '| Slice                    |'   : 0,
    '| LUT as Logic             |'   : 0,
    '| LUT as Memory            |'   : 0,
    '| LUT Flip Flop Pairs      |'   : 0,
    '| Unique Control Sets      |'   : 0,
    '| Block RAM Tile |'             : 0,
    '| DSPs      |'                  : 0,
    '| Bonded IOB                  |': 0,
    '| OBUF     |'                   : 0,
    '| LUT6     |'                   : 0,
    '| IBUF     |'                   : 0,
    '| LUT5     |'                   : 0,
    '| LUT3     |'                   : 0,
    '| LUT4     |'                   : 0,
    '| LUT2     |'                   : 0,

    #power report keys
    '| Total On-Chip Power (W)  |'   : 0,
    '| Dynamic (W)              |'   : 0,
    '| Device Static (W)        |'   : 0,
    '| Slice Logic    |'             : 0,
    '| Signals        |'             : 0,
    '| I/O            |'             : 0,
    '| Static Power   |'             : 0
  }
  
  report = open(filename, 'r')

  for line in report:
    for key in keywords_map.keys():
      if key in line:
        keywords_map[key] = float(line.split('|')[2].replace("(Junction temp exceeded!)", ""))
  
  for key in keywords_map:
    print('{}: {}'.format(key_to_text(key), keywords_map[key]))

  report.close()

