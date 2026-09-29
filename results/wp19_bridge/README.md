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

## v0.4 one-sided observable bridge

WP19 v0.4 proves an exact finite algebraic monotonicity statement for the frozen K36 observable: once the low coefficients are fixed and the cutoff is at least 10, newly added higher modes cannot increase F=I-9O. They cannot enter any selected K36 orbit-pair key, while new outside-key masses contribute nonnegatively to O.

The dynamic cutoff problem therefore reduces to controlling the high shell's backreaction on the old low modes. The accompanying scout records low-mode endpoint drifts 0.225582 for N11->N12 and 0.203005 for N12->N13, with sampled backreaction recurrences 0.373078 and 0.322998. These are diagnostics, not certificates.

The archived v0.4 ZIP SHA-256 is `1cfa821bc7ccadc50db77c068dc756cfd1b89051595e2caa7b708625f8a123a4`.


## v0.5 fixed finite coalition locality

WP19 v0.5 freezes a post-hoc N11-derived set of 200 outside-K36 orbit-pair groups. Because omitted outside groups only decrease the full observable, the retained coalition defines an exact upper observable `U_C200` with `F <= U_C200`.

The union of K36 and C200 uses exactly 461 ordered K-channel source pairs and 569 unique Fourier modes. Every retained orbit has norm at most 11, so this support is unchanged at N=11,12,13,14,17 and, algebraically, for every larger cutoff.

The unchanged C200 upper observable is negative at the saved same-datum endpoints:
- N11: -33.178421
- N12: -44.220575
- N13: -46.113595

These three values are floating transfer diagnostics. The support-locality theorem and `F <= U_C200` inequality are exact. A single global low-mode L2 perturbation ball remains far too loose, so the next gate must propagate support-aware or direction-aware error on the fixed 569-mode set.

C200 SHA-256: `4fb5531fcc6c4490aa7826992ff843f27fefdbc1427c7587ac0544027420e698`.

The archived v0.5 ZIP SHA-256 is `fa1c440248016c015bd974b191232d1ffc687f2b5b722eabb31bf61ee30a5a5f`.
