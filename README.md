![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg) ![](../../workflows/test/badge.svg) ![](../../workflows/fpga/badge.svg)

# IIC - Integrated Circuits Design KV

- [Moodle Course](https://moodle.jku.at/course/view.php?id=39685)
- [Tiny Tapeout Website](https://tinytapeout.com)

## Local Testing and Building

In the IIC OSIC Tools containter:

- Testing the Source Code

```bash
verilator --lint-only src/*.v
yosys -p "read_verilog "$name".v; proc; opt; flatten; techmap; stat"
```

- Testing the Testbeches

```bash
make
```

- Or run specific testbenches:

```bash
make test_counter
make test_bitcount
make test_pwm_encoding
make test_note2cnt
make test_osc
make test_rx
make test_midi
make test
```

- Testing GDS generation

```bash
source sak-pdk-script.sh sky130A sky130_fd_sc_hd > /dev/null
librelane --manual-pdk config.json
librelane --manual-pdk config.json --last-run --flow OpenInOpenROAD
```

# Tiny Tapeout TT-SKY25b Submission

- [Read the documentation for project](docs/info.md)  

## What is Tiny Tapeout?

Tiny Tapeout is an educational project that aims to make it easier and cheaper than ever to get your digital and analog designs manufactured on a real chip.

To learn more and get started, visit <https://tinytapeout.com>.

## Resources

- [FAQ](https://tinytapeout.com/faq/)
- [Digital design lessons](https://tinytapeout.com/digital_design/)
- [Learn how semiconductors work](https://tinytapeout.com/siliwiz/)
- [Join the community](https://tinytapeout.com/discord)
- [Build your design locally](https://www.tinytapeout.com/guides/local-hardening/)
