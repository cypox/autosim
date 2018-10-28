#!/usr/bin/python3
import os

def generate_multiplier(a_len = 4, b_len = 4, w = 0b1010, filename = 'sq_mult.vhd', top = 'sq_mult'):
  o_len = a_len + b_len

  W = format(w, '#0{}b'.format(a_len+2))[2:]
  W = W[::-1]

  assert(len(W) == a_len)

  f = open(filename, 'w')

  #header
  f.write('-- MULTIPLY BY 0x{}\n'.format(format(w, '#0{}b'.format(a_len+2))[2:]))
  f.write('-- HEADER\n');
  f.write('library IEEE;\n')
  f.write('use IEEE.STD_LOGIC_1164.ALL;\n')
  f.write('\n')
  f.write('entity {} is \n'.format(top))
  f.write('  Port (\n')
  f.write('    B : in STD_LOGIC_VECTOR ({} downto 0);\n'.format(b_len-1))
  f.write('    O : out STD_LOGIC_VECTOR ({} downto 0));\n'.format(o_len-1))
  f.write('end {};\n'.format(top))

  f.write('\n')

  #architecture
  f.write('-- ARCHITECTURE\n');
  f.write('architecture Behavioral of {} is\n'.format(top))

  f.write('\n')

  #components
  f.write('-- COMPONENTS\n');
  f.write('component fa\n')
  f.write('  Port (\n')
  f.write('    A : in STD_LOGIC;\n')
  f.write('    B : in STD_LOGIC;\n')
  f.write('    Cin : in STD_LOGIC;\n')
  f.write('    S : out STD_LOGIC;\n')
  f.write('    Co : out STD_LOGIC);\n')
  f.write('end component;\n')

  f.write('\n')

  #signals
  f.write('-- SIGNALS\n');
  for p in range(b_len):
    for stage in range(a_len):
      f.write('signal Si_{}_{}: std_logic;\n'.format(stage, p))
      f.write('signal So_{}_{}: std_logic;\n'.format(stage, p))
      f.write('signal Cr_{}_{}: std_logic;\n'.format(stage, p))

  f.write('\n')

  #logic
  f.write('-- LOGIC\n')
  f.write('begin\n')
  if W[0] == '0':
    for p in range(b_len):
      if p == 0:
        f.write('O({}) <= \'0\';\n'.format(0))
      else:
        f.write('So_{}_{} <= \'0\';\n'.format(0, p-1, p))
      if p == b_len-1:
        f.write('So_{}_{} <= \'0\';\n'.format(0, p))
  elif W[0] == '1':
    for p in range(b_len):
      if p == 0:
        f.write('O({}) <= B({});\n'.format(0, p))
      else:
        f.write('So_{}_{} <= B({});\n'.format(0, p-1, p))
      if p == b_len-1:
        f.write('So_{}_{} <= \'0\';\n'.format(0, p))
  f.write('\n')

  for stage in range(1, a_len):
    for p in range(b_len):
      f.write('Si_{}_{} <= So_{}_{};\n'.format(stage, p, stage-1, p))
  f.write('\n')

  for stage in range(1, a_len):
    if W[stage] == '0':
      f.write('O({}) <= Si_{}_0;\n'.format(stage, stage))
      for p in range(b_len):
        if p != b_len-1:
          f.write('So_{}_{} <= Si_{}_{};\n'.format(stage, p, stage, p+1))
        else:
          f.write('So_{}_{} <= \'0\';\n'.format(stage, p))
    elif W[stage] == '1':
      for p in range(b_len):
        if p == 0:
          f.write('B_{}_{}: fa port map(A => B({}), B => Si_{}_{}, Cin => \'0\', S => O({}), Co => Cr_{}_{});\n'.format(stage, p, p, stage, p, stage, stage, p))
        elif p < b_len-1:
          f.write('B_{}_{}: fa port map(A => B({}), B => Si_{}_{}, Cin => Cr_{}_{}, S => So_{}_{}, Co => Cr_{}_{});\n'.format(stage, p, p, stage, p, stage, p-1, stage, p-1, stage, p))
        else:
          f.write('B_{}_{}: fa port map(A => B({}), B => Si_{}_{}, Cin => Cr_{}_{}, S => So_{}_{}, Co => So_{}_{});\n'.format(stage, p, p, stage, p, stage, p-1, stage, p-1, stage, p))

  for p in range(b_len, o_len):
    f.write('O({}) <= So_{}_{};\n'.format(p, b_len-1, p-b_len))

  f.write('\n')

  f.write('\n')

  #end
  f.write('-- END\n');
  f.write('end Behavioral;\n')
  f.write('\n')

  f.close()
