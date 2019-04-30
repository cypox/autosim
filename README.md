# A-New-Storage-Less-Hardware-Compression-Technique-for-FPGA-based-CNNs-Using-Constant-Multiplication
[This is a minimal copy of the project, we made public for reviewer's answers. The main project contains the full structure.]

This project exploits constant multiplication in Convolutional Neural Networks.

The tool (autosim.py) takes quantization parameters as input. For the netwroks we used, weights are 8 bit fixed points numbers that includes a sign bit. This can be reduced to 7-bit integer multiplication since signs can be xor-ed together and radix is common in the representation we used (see reference in paper).

For a given bit-width 'w', we generate all possible numbers (2^w). For each number 'n', we call a generator (mgen.py) to create a ***squeezed*** representation of a multiplier with 'n' as one of its operands. The generated files are in VHDL.

The numbers in Figure 6 are obtained using a tcl script (script.tcl). The script is called automatically from autosim.py. In it, we create a Xilinx project with a given part/board (in our case xc7z020clg484-1/em.avnet.com:zed:part0:1.3). The project is synthetized, optimized, placed and routed using Vivado and reports are generated for each file.

