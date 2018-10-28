#!/usr/bin/python3
import sys, os
import shutil
from subprocess import call
from vhdl.mgen import generate_multiplier
from tcl.sgen import generate_tcl_script

if __name__ == "__main__":
  if len(sys.argv) == 2:
    word_size = int(sys.argv[1])
  else:
    word_size = 4

  fa_source_vhdl = 'vhdl/fa.vhd'
  vivado_path = '/opt/Xilinx/Vivado/2017.4/bin/vivado'
  top = 'sq_mult'

  outputs_dir = os.path.join(os.getcwd(), 'outputs')
  if not os.path.exists(outputs_dir):
    os.makedirs(outputs_dir)

  for i in range(13, 14): # for debug only
  #for i in range(0, 2**word_size):
    output_path = '{}'.format(format(i, '#0{}b'.format(word_size+2)))

    source_path = os.path.join(outputs_dir, output_path)
    if not os.path.exists(source_path):
        os.makedirs(source_path)
    source_file = os.path.join(source_path, 'multiplier.vhd')
    print('generating source file {} for input {}'.format(source_file, format(i, '#0{}b'.format(word_size+2))))
    
    generate_multiplier(a_len = word_size, b_len = word_size, w = i, filename = source_file, top = top)
    shutil.copy2(fa_source_vhdl, source_path)

    script_path = source_path
    script_name = 'script.tcl'
    script_file = os.path.join(script_path, script_name)
    generate_tcl_script(path=script_path, filename = script_name, top = top)
    print('generating tcl script in {}'.format(script_path))

    # vivado -mode batch -source script.tcl
    command = vivado_path + ' -mode batch -source ' + '"{}"'.format(script_file)
    print('executing: \'{}\''.format(command))
    os.system(command)

    utilization_file = os.path.join(script_file, )
