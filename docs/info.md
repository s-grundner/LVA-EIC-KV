# Polyphonic MIDI Synthesizer ASIC

## How it works

**Square Waves** based on note ON and note OFF commands. The Oscillator stack
is capable of synthesizing up to 3 voices simultaneously. Each voice is routed
to a different output pin, allowing for external mixing of the signals. Each
Oscillator responds to a **different MIDI-Channel** (1, 2, 3), which was
necessary to simplify the voice allocation logic inside the ASIC. Additionally,
a PWM signal is provided on a separate output pin, which encodes the number of
currently active voices. This PWM signal can be used to control the gain of the
mixed output through lowpass filtering. The ASIC receives MIDI messages via a
simple UART reciever and synthesizes.

### How the AISC responds to Edge Cases

TODO

- If a second note ON command is received for a voice that is already active...


### Where do I get the MIDI messages from?

There are multiple ways to feed the ASIC with MIDI messages:

1. Use a Microcontroller to Emulate a MIDI device. This is the easiest way to get started. You can use an e.g. the onboard RP2040 or any other microcontroller with UART capabilities.
2. Use a MIDI Controller (Piano, Pads) with a native MIDI-OUT DIN connector. You will need a PMOD as a physical layer to convert the differential signal to a single-ended UART signal.
3. Use a Computer to send MIDI Messages via a USB serial interface. You can use the RP2040 or an FTDI Chip and send raw MIDI messages over a serial connection.
4. If you have a Digital Audio Workstation (DAW) available, you can send MIDI messages from virtual instruments inside the DAW to a virtual MIDI Port.

Here are some software recommendations for option 4:

- Create a virtual MIDI Port on your Computer with [loopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) by Tobias Erichsen (Free for personal use)
- Connect a virtual MIDI interface to a COM-Port with [Hairless MIDI Serial](https://projectgus.github.io/hairless-midiserial/) (FOSS under GPLv2)
- Digital Audio Workstations:
  - [LMMS](https://lmms.io/) (FOSS under GPLv2)
  - [Ableton Live](https://www.ableton.com/en/live/) (Proprietary, Paid)

## How to test

Connect a MIDI device. Press a key and Measure output pin 0 with an oscilloscope for the correct frequency. Press multiple keys simultaneously, and check each pin for the expected output.

## External hardware

- MIDI Controller (Piano, Pads)
- MIDI DIN connector PMOD as a physical layer for the differential midi signal
- (Optional) External Mixing circuitry. Example circuit provided in the repository
- Speaker (High impedance when used without a driver)
