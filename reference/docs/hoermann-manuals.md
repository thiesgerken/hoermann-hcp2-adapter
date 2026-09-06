# Hörmann manual analysis

The manuals supplied with this project remain unchanged under [`reference/manuals/`](../manuals/). They are the primary sources for the specific ProMatic 4 opener and its accessories.

## ProMatic 4 installation, operation, and maintenance

- File: [promatic-4-montage-betrieb-wartung-4511178-b0-18-2022.pdf](../manuals/promatic-4-montage-betrieb-wartung-4511178-b0-18-2022.pdf)
- Document number: `4511178 B0`
- Edition: `18-2022 / RE`
- Language: German
- Title: Garage door operator, instructions for fitting, operation, and maintenance

Relevant sections:

- Section 5.5 describes DIL switch C for internal lighting, BUS, and pre-warning.
- Section 5.10 describes the BUS scan.
- A BUS scan removes and rediscovers connected accessories.
- HOR 1-HCP and UAP 1-HCP are listed as Series 4 accessories.
- Electrical work and mains-voltage areas are reserved for qualified personnel.

## ProMatic 4 functional description and accessories

- File: [promatic-4-funktionen-zubehoer-4553098-b0-21-2022.pdf](../manuals/promatic-4-funktionen-zubehoer-4553098-b0-21-2022.pdf)
- Document number: `4553098 B0`
- Edition: `21-2022`
- Title: Garage door operator, functional description and accessories
- Languages: multilingual; German begins on page 2

Relevant sections:

- Section 3.9 identifies the BUS socket for accessories with special functions.
- BUS scan procedure: connect participants, move DIL switch H from OFF to ON, then back to OFF.
- A scan removes and rediscovers BUS accessories.
- Section 4 sets a 350 mA maximum combined accessory load on the opener.
- Series 3 accessories require the HAP 1 HCP adapter.
- HOR 1-HCP and UAP 1-HCP are explicitly listed as HCP accessories.

The 350 mA value is a combined accessory limit, not the automatic allowance for this adapter alone. Measure the actual startup current of the ESP32, RS485 module, and LM2596 during a BUS scan and keep it comfortably below that limit.

## HOR1-HCP option relay

- File: [hor1-hcp-tr30a117-07-2019.pdf](../manuals/hor1-hcp-tr30a117-07-2019.pdf)
- Document number: `TR30A117`
- Edition: `07.2019`
- Product: `HOR1-HCP`

Relevant sections:

- The wiring diagram specifies Series 4 and a maximum BUS cable length of 10 m.
- The BUS participant connects through the opener's BUS interface.
- Status LED: flashing green means not registered, solid green means registered, and three red flashes indicate a BUS scan.
- Relay ratings are 2.5 A at 30 V DC or 500 W at 250 V AC. These values do not apply to the adapter electronics.

## Consolidated design limits

| Limit | Source | Design consequence |
|---|---|---|
| Series 4 only | ProMatic and HOR1-HCP manuals, ESPHome | No compatibility claim for Series 3 |
| 350 mA maximum combined accessories | Functional description, section 4 | Measure adapter startup and operating current |
| 10 m maximum BUS cable | HOR1-HCP wiring diagram | Record the installed cable length |
| Accessories are rediscovered during scans | Both ProMatic manuals | Connect the adapter before scanning and keep it able to boot during the scan |
| No work while mains is connected | Safety sections | Disconnect the mains plug and any emergency battery before installation |

The exact HCP2 contact assignment and UART parameters come from the ESPHome HCP documentation. The Hörmann manuals confirm the BUS connection, Series 4 scope, and scan procedure, but the reviewed passages do not provide a reliable six-pin signal assignment.
