# WP19 bridge results

This folder records the compact, repository-friendly outputs from the three WP19 bridge packages archived separately in Drive.

## Archive ZIP hashes

- WP19_Consecutive_Cutoff_Bridge_Gate_v0_1.zip  
  SHA-256: 83001f1ec9bfbcccac8d06dd23abe81c477e68ec397e55097a1a0dff9212d8aa
- WP19_v0_2_Evidence_Inventory_and_Bridge_Map.zip  
  SHA-256: a53e8636ae7e4fe3b1dc10d573e4c2355b4124bbe9d727e754aafd1f687acd53
- WP19_v0_3_Consecutive_Cutoff_Bridge_Scout.zip  
  SHA-256: baedca8e915f479240bd5704a41a154757dcde4602b3e35bc6c407919c86246d

## Repository contents

- `N14_N17_ARTIFACT_INVENTORY.json` — provenance map for the earlier N14-N17 prospective cutoff program.
- `N14_N17_EVIDENCE_LEDGER.csv` — compact evidence-class ledger.
- `WP19_v0_2_BRIDGE_PLAN.json` — proof-first bridge plan keeping the optimizer-derived N14-N17 track separate from the later same-rational-datum Arb track.
- `WP19_v0_3_SCOUT_RESULTS.json` — compact scouting metrics for N11->N12 and N12->N13.
- `BRIDGE_SCOUT_TABLE.csv` — headline comparison table.

The full node-by-node scouting traces and sampled physical-strain arrays are retained in the archived v0.3 ZIP. They are reproducible with the scripts in `src/`.

## Evidence boundary

The v0.3 computation is explicitly **non-rigorous scouting**. It identifies the current proof-loss bottleneck: the Fourier-l1 strain majorant is much looser than the sampled physical-space symmetric strain. The next proof target is a whole-segment rigorous enclosure of `||S(u_N)||_{L-infinity,op}`, combined with an Arb enclosure of the newly opened-shell forcing.

The historical N14-N17 phase/time-gate data are not the same datum as the later N11-N13 rational-witness Arb certificate family and must not be relabeled as such.
