#!/usr/bin/python3
import matplotlib.pyplot as plt

output_filename = 'figure.pdf'

results = open('results', 'r')

weights = []
luts = []
logics = []
signals = []
resources = []
energy = []

for line in results:
  if line == '\n':
    continue

  weight = int(line.split(':')[0])
  res = line.split(':')[1]
  lut = float(res.split(',')[0])
  logic = float(res.split(',')[1])
  signal = float(res.split(',')[2])

  weights.append(weight)
  luts.append(lut)
  logics.append(logic)
  signals.append(signal)

  resources.append(lut)
  energy.append(signal + logic)

results.close()

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
