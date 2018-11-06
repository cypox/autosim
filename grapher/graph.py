#!/usr/bin/python3
import os
import matplotlib.pyplot as plt
from extract.parse import parse_report


def plot_results(word_size = 8, outputs_folder = '/home/cy/dac-2019/autosim/outputs/', output_filename = 'figure.pdf')
  weights = []
  luts = []
  logics = []
  signals = []
  resources = []
  energy = []

  for i in range(0, 2**word_size):
    output_path = '{}/project'.format(format(i, '#0{}b'.format(word_size+2)))
    project_path = os.path.join(outputs_folder, output_path)
    (u, p) = parse_report(project_path)

    lut = u['| Slice                    |']
    logic = p['| Slice Logic    |']
    signal = p['| Signals        |']

    weights.append(i)
    luts.append(lut)
    logics.append(logic)
    signals.append(signal)

    resources.append(lut)
    energy.append(signal + logic)
    
  fig, ax1 = plt.subplots()
  ax1.bar(weights, resources)
  ax1.set_xlabel('Weights')
  # Make the y-axis label, ticks and tick labels match the line color.
  ax1.set_ylabel('Resources', color='b')
  ax1.tick_params('y', colors='b')

  ax2 = ax1.twinx()
  ax2.plot(weights, energy, 'r-')
  ax2.set_ylabel('Energy', color='r')
  ax2.tick_params('y', colors='r')

  fig.tight_layout()
  plt.savefig(output_filename)
  plt.show()
