# Decision log

| ID | Date | Status | Decision | Rationale or approval condition |
|---|---|---|---|---|
| D-001 | 2026-09-05 | Decided | Do not create a complete schematic or PCB layout yet. Document and measure the purchased parts first. | Module variants and footprints must be verified on delivered samples. |
| D-002 | 2026-09-05 | Decided | The first board is a carrier for ESP32-C3, LM2596, and isolated RS485 modules. | All three modules have already been purchased. Integrating individual ICs would be a different design. |
| D-003 | 2026-09-05 | Decided | J1 is the unshielded `6P6C` option from AliExpress item 1005003078110991. | The selection is fixed. Measure the hole pattern and contact order before releasing the PCB. |
| D-004 | 2026-09-05 | Decided | Do not add a 120 Ω termination resistor or footprint to the carrier PCB. | The selected RS485 module reportedly includes termination. Measure resistance between A and B before commissioning. |
| D-005 | 2026-09-05 | Decided | Do not add protection circuitry at the HCP input. | Reverse polarity is addressed by D-014. The design relies on the Hörmann supply for surge behavior and on the RS485 module for A/B ESD protection. |
| D-006 | 2026-09-05 | Decided | Add a disconnectable `BUS_PWR` link to the 5 V supply from the LM2596. | The Super Mini form-factor documentation prohibits simultaneous USB and external power. |
| D-007 | 2026-09-05 | Decided | Power the RS485 module from the ESP32-C3 Super Mini 3.3 V rail. | This avoids a possible 5 V signal at ESP32 RX. The vendor specifies 3.3 V operation; no separate qualification was requested. |
| D-008 | 2026-09-05 | Observed | The first build is not fully galvanically isolated. | The non-isolated LM2596 connects supply grounds. The RS485 module isolates only the signal path. |
| D-009 | 2026-09-05 | Decided | Generate the first schematic before footprints are finalized. | The electrical topology is known and does not depend on mechanical dimensions. |
| D-010 | 2026-09-05 | Provisionally decided | Generate a fully routed preliminary PCB with clearly identified provisional footprints. | This permits early review of board size, placement, and routing. Release still requires physical measurements. |
| D-011 | 2026-09-05 | Provisionally decided | Use a 65 × 44.5 mm PCB with module-specific footprints. Place J1 at the edge, and use module holes plus a hole below U1 for mounting. | Avoid wasted area. Confirm vendor-derived measurements before fabrication. |
| D-012 | 2026-09-05 | Decided | Generate schematic and PCB directly as KiCad files from `design.py`, without SKiDL. Run ERC, DRC, and netlist operations through `kicad-cli`. | The SKiDL route required regex post-processing for readable layout. Direct generation is shorter and produces a clean schematic. |
| D-013 | 2026-09-05 | Decided | Give J1 a custom `RJ12_95001_6P6C` footprint instead of the Amphenol 54601 footprint. | The initially reviewed 95001-family drawing used different pin and peg spacing. |
| D-014 | 2026-09-05 | Decided | Do not add reverse-polarity protection to the 25 V input. | Reverse polarity is possible only with a crossed telephone cable. Every cable must be verified as straight-through before connection. |
| D-015 | 2026-09-06 | Decided | Restore the Amphenol 54601-compatible footprint for J1, rotated 180 degrees. | The drawing for the purchased 6P6C type `53-6p6c` matches its 13.2 × 18 mm body, Ø3.2 mm pegs at 10.16 mm spacing, 1.27 mm staggered pins, and latch-down orientation. Supersedes D-013. |

Assign each new decision the next sequential ID. Record changed decisions as new entries so the original rationale remains visible.
