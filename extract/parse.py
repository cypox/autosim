#!/usr/bin/python3
import os, sys

def key_to_text(key):
  return key.split('|')[1].rstrip().lstrip()

def parse_report(path = '.'):
 
  util_file = os.path.join(path, 'utilization_placed.rpt')
  power_file = os.path.join(path, 'power_routed.rpt')

  u_keywords_map = {
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
    '| LUT2     |'                   : 0
  }

  p_keywords_map = {
    #power report keys
    '| Total On-Chip Power (W)  |'   : 0,
    '| Dynamic (W)              |'   : 0,
    '| Device Static (W)        |'   : 0,
    '| Slice Logic    |'             : 0,
    '| Signals        |'             : 0,
    '| I/O            |'             : 0,
    '| Static Power   |'             : 0
  }
  
  report = open(util_file, 'r')
  for line in report:
    for key in u_keywords_map:
      if key in line:
        u_keywords_map[key] = float(line.split('|')[2])
  report.close()
  
  report = open(power_file, 'r')
  for line in report:
    for key in p_keywords_map:
      if key in line:
        p_keywords_map[key] = float(line.split('|')[2].replace("(Junction temp exceeded!)", ""))
  report.close()

  return (u_keywords_map, p_keywords_map)
