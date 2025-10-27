# Sample testbench for a Tiny Tapeout project

This is a sample testbench for a Tiny Tapeout project. It uses [cocotb](https://docs.cocotb.org/en/stable/) to drive the DUT and check the outputs.
See below to get started or for more information, check the [website](https://tinytapeout.com/hdl/testing/).

## Add testcases

1. Create a CocoTB Script `test_<modulename>.py` and write unittests (View existing CocoB Scripts for reference)
2. Edit [Makefile](Makefile) and add tests to `TEST_CONFIGS` with the Format
   - `<scriptname>:<toplevel-entity>:<testbench-file>`
   - `<scriptname>`: Name of the CocoTB script without .py extension
   - `<toplevel-entity>`: Name of the top level module to be tested
   - `<testbench-file>`: File name of the testbench Verilog file located in `test/benches/` (with .v extension)

## How to run

To run the RTL simulation:

```sh
make -B
```

To run gatelevel simulation, first harden your project and copy `../runs/wokwi/results/final/verilog/gl/{your_module_name}.v` to `gate_level_netlist.v`.

Then run:

```sh
make -B GATES=yes
```

## How to view the VCD file

Using GTKWave
```sh
gtkwave tb.vcd tb.gtkw
```

Using Surfer
```sh
surfer tb.vcd
```

## Tested

Atomic Modules

- [x] counter
- [x] rx
- [x] note2cnt
- [x] bitcount
- [ ] midi

Dependent Modules

- [ ] pwm
- [ ] oscillator stack

Top Level Module

- [ ] Top Level Design