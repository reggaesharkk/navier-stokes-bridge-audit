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


## v0.6 dual-weighted residual bridge

WP19 v0.6 replaces the norm-first endpoint perturbation route with a goal-oriented discrete-adjoint scout.

A post-hoc N11-derived C500 outside coalition is frozen with SHA-256 `79bdc347358705b4611f10f76a50db16e5edff572d1822ca1459cd868e15c216`. Using
`n_g = Im(w_g * conj(z))` and fixed signs `tau_g`, it defines the exact upper surrogate

`G_C500 = (sum_K36 |n_g| - 9 sum_C500 tau_g n_g)/|z|^2`

with `F <= G_C500` whenever the normalizer is nonzero.

The C500 surrogate depends on exactly 1,048 ordered source pairs and 1,159 Fourier modes for every cutoff at least 11. The materialized C500 JSON is retained in the v0.6 archive; `src/wp19_v0_6_build_fixed_c500.py` deterministically regenerates it and verifies its hash.

The non-rigorous discrete-adjoint scout gives:

- N11->N12: base upper margin `-47.816278`, projected-higher value `-55.152798`, linearized dual-weighted defect sum `-7.505923`, observed nonlinear remainder `+0.169403`, and sum of absolute step contributions `9.489442`.
- N12->N13: base upper margin `-55.152798`, projected-higher value `-55.760507`, linearized dual-weighted defect sum `-0.604941`, observed remainder `-0.002768`, and sum of absolute step contributions `6.198853`.

These are floating scouting quantities, not interval certificates. The next proof target is a rigorous scalar dual-weighted residual bound plus a second-order remainder enclosure, not a global state-norm bound.

The archived v0.6 ZIP SHA-256 is `ed6346092007e9cd15ad17c157aa55b69990606fdaed4397874edff037d9dedd`.


## v0.7 exact-rational C500 endpoint certificate

WP19 v0.7 validates the v0.6 C500 endpoint surrogate on the already certified same-datum N11-N13 trajectories.

The saved endpoint node is reconstructed using the same exact-decimal solenoidal/reality projection rule as the Arb endpoint certificate, and `G_C500` is evaluated with exact rational arithmetic. The previously certified endpoint error formula is a key-independent coefficient-9 source/normalizer envelope, so it also encloses perturbations of `G_C500`.

Certified intervals are:

- N11: `[-54.174149219, -41.458407264]`
- N12: `[-56.770960917, -53.534635536]`
- N13: `[-57.555599822, -53.965413679]`

All three upper endpoints are strictly negative. This certifies the C500 upper functional at the existing finite cutoffs; it does not yet certify a lower-cutoff-only next-cutoff prediction or any continuum statement.

The archived v0.7 ZIP SHA-256 is `17c3d67aaa9ef113b6534f61e83532c914eeba28f21c46550ca30a71ff46113c`.


## v0.8 kink-safe quadratic dual bridge

WP19 v0.8 removes the absolute-value sign-flip obstruction from the dual-weighted endpoint architecture with the exact scalar inequality

`|x| <= sign(x0)*x + (x-x0)^2/(2|x0|)`.

Applied groupwise at the lower endpoint, this gives

`G_C500(v) <= G_C500(a) + [L_a(v)-L_a(a)] + Q_a(v)`,

where `L_a` is a smooth signed endpoint functional and `Q_a` is an explicit nonnegative quadratic correction over only the 36 K36 ratios. No K36 sign-stability assumption is required.

On the saved transitions the observed quadratic corrections are `0.750228` for N11->N12 and `0.268059` for N12->N13. Reinterpreting the v0.6 adjoint as the first-order sensitivity of `L_a`, the smooth observed remainders are only `-0.048112` and `-0.002768`.

After charging the v0.7 certified base upper margin, the sum of absolute observed first-order terms, the observed Q term, and the absolute smooth remainder, the scouting residual margins are approximately `31.17` and `47.06`. These are design budgets, not interval certificates.

The archived v0.8 ZIP SHA-256 is `b192fd222da5e7d50d908cf4037981f83f2ce4c6a79a9b4517d1f21bfa804b47`.
