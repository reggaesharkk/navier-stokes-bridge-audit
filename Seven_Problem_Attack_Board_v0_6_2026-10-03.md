# Seven-Problem Attack Board v0.4
**Date:** 3 October 2026  
**Revision:** v0.4 — joint-pairing semantic gate audited; pilot stopped before compute  
**Purpose:** Define an ambitious first phase around seven major open scientific and mathematical targets, with each connection to the current research portfolio tested rather than assumed.

## Strategy

The first objective is a credible, independently checkable advance on a frontier problem. Any later public attention, collaborators, or resources are possible benefits, not inputs we can count on. Broader public benefit is a later phase.

There is no official universal ranking of the world's seven hardest open problems. This is a working slate, not a claim of consensus. Four targets below (Navier–Stokes, Riemann, P vs NP, Yang–Mills) appear on the Clay Mathematics Institute's Millennium list; the portfolio also includes quantum gravity, dark matter, and dark energy.

The dossier describes six distinct research programs and explicitly does not claim they form a unified law of nature. Existing results therefore enter this board as footholds, methods, or hypotheses—not as solutions to these seven problems.

## Target cards

### 1. 3D Navier–Stokes global regularity
**Fit:** Closest active mathematical target. The current line has finite Galerkin audits and conditional finite-cutoff certificates; the all-cutoff/continuum transfer remains open.

**Existing foothold:** WP19 finite chain through N18; v0.28 adjoint work remains conditional on imported segment bounds. The unresolved transfer includes recursive state/backreaction drift and high-frequency control. The targeted M15-support recomputation on steps 220–239 has now passed for its bounded reconstruction-based primal-tube contribution; the whole-path replay still does not close the signed margin.

**First attack:** The 20-step M15-support coefficients and exact-rational whole-path replay have been independently recomputed from the artifact and frozen input JSONs; all five aggregate values match. The target shard fell by 0.533%, while the full conservative remainder fell by 0.259%. Next, isolate the largest remaining terms and state the exact uniform estimate needed for recursive drift and high-frequency continuation. Test each proposed bound against concentration/scaling counterexamples.

**Credible milestone:** A new lemma or estimate with constants and hypotheses that close a named part of the transfer, or a rigorous obstruction showing why a proposed route cannot close it.

**Stop line:** Finite-dimensional sign crossings, sampled phase retention, or a fixed low-mode observable alone do not prove regularity or blow-up for the continuum PDE.

### 2. Riemann hypothesis
**Fit:** No established direct bridge from the current portfolio. LRSC's finite spectral/combinatorial certificates are methodological precedent only.

**First attack:** Write the exact analytic statement and choose one tractable subproblem: a new zero-free region, an explicit-formula bound, a rigorous finite verification extension, or a precisely formulated spectral-operator route. Separate numerical evidence from proof.

**Credible milestone:** A theorem that improves a known bound or proves a new implication, with a complete literature check and independently reproducible calculations where computation is used.

**Stop line:** Finite zero checks and spectral analogies do not imply the hypothesis.

### 3. P versus NP
**Fit:** LRSC demonstrates exact finite enumeration for one benchmark. It does not establish a general complexity lower bound or P ≠ NP.

**First attack:** Pick one formally defined restricted model (for example, a circuit class) and prove a lower bound there. Before investing in a route, map known barriers and state exactly what a result in that model would and would not imply for general circuits.

**Credible milestone:** A correct lower bound that exceeds known results in the selected model, or a rigorous reduction/barrier result that materially narrows candidate approaches.

**Stop line:** Finite exhaustive search or a hard benchmark instance is not a general complexity separation.

### 4. Yang–Mills existence and mass gap
**Fit:** No current theorem in the portfolio concerns quantum gauge fields. ODE stability, finite fluid certificates, and exact subset enumeration do not transfer automatically.

**First attack:** Choose the precise setting and axioms first. Identify one construction or estimate needed for a continuum quantum Yang–Mills theory with a positive mass gap; audit whether a finite-lattice result survives the required volume and continuum limits.

**Credible milestone:** A rigorous estimate uniform in the relevant cutoff/volume, or a new theorem closing a clearly identified construction step.

**Stop line:** A finite lattice spectrum or numerical gap alone is not the four-dimensional existence-and-gap result.

### 5. Quantum gravity / a Theory of Everything
**Fit:** Information-Theoretic Physics offers a phenomenological ODE theorem and a separate cosmology sandbox. The dossier marks the microscopic derivation and observer/horizon-entropy bridge as open.

**First attack:** Formalize Gate 0: define every state variable and unit; specify a map from a recognized microscopic framework to the model; derive, rather than posit, the entropy or horizon observable; recover an established limit; identify an observation that could distinguish the model.

**Credible milestone:** A derivation from a named physical theory with a checkable theorem and a discriminating prediction. A stochastic extension is relevant only if its noise law is physically derived or independently justified.

**Stop line:** Adding arbitrary Brownian noise, finding an invariant measure, or observing a structural resemblance to holography does not derive quantum gravity or Hawking radiation.

### 6. Dark matter
**Fit:** No current program supplies a tested microscopic candidate or an observationally constrained dark-matter model.

**First attack:** Specify a candidate model and derive one quantitative prediction that separates it from standard alternatives. Test against appropriate independent observations and state parameter ranges excluded as well as allowed.

**Credible milestone:** A derivation plus a successful out-of-sample observational test, or a robust exclusion of a model class.

**Stop line:** A stable information-physics sandbox or a generic information analogy is not evidence for dark matter's identity.

### 7. Dark energy / cosmological constant
**Fit:** The three-state cosmology sandbox could be examined as phenomenology only after its variables are given physical meaning and connected to measured expansion history. The dossier does not establish that mapping.

**First attack:** Specify the model-to-observable map, units, and initial conditions. Derive an expansion-history prediction and compare it against a stated baseline using public cosmological data; predefine what result would falsify the model.

**Credible milestone:** A reproducible fit or prediction that survives independent data and model checks and improves on a baseline without adding unconstrained parameters.

**Stop line:** Local asymptotic stability of an abstract ODE equilibrium does not explain cosmic acceleration.

## Common progress scale

Do not report “10% solved” unless the problem has a defensible quantitative decomposition. Record progress in verifiable steps:

1. Exact target statement and source literature.
2. Named gap or subproblem with assumptions fixed.
3. Candidate lemma, construction, or prediction.
4. Counterexample and failure search.
5. Proof or validated computation with reproducible inputs.
6. Independent audit and comparison with the strongest known result.
7. Any public claim states precisely what changed and what remains open.

## Operating rule

Keep all seven target cards active as a portfolio, but run one deep proof/experiment at a time. Start with Navier–Stokes because it has the strongest existing foothold. The targeted replay shows only a small improvement and no sign closure; the next NS task is to identify the dominant remaining budget term and a proof route that could reduce it. For the other six, begin with formalization and literature-gap maps before claiming that any existing method transfers.

## Current status

- Navier–Stokes targeted M15-support run: completed successfully. The 192-bit Arb shard covers steps 220–239; the whole-path replacement replay uses exact rational arithmetic and matches the frozen inputs. The artifact digest matches GitHub’s published SHA-256.
- Old selected-step quadratic upper: 79,714,789,407,812.3283; direct M15-support replacement: 79,290,095,908,202.2205 (0.533% reduction).
- Whole-path conservative remainder: 164,063,087,678,950.0886 before replacement; 163,638,394,179,339.9808 after replacement (0.259% reduction). Components after replacement: quadratic term 114,093,007,395,768.6501; terminal boundary term 49,545,386,543,507.4983; retained adjoint-defect term 240,063.8325.
- Frozen signed integral lower bound remains 5,758,574,435.6058, so the lower signed margin is still negative: −163,632,635,604,904.3750. The conservative remainder is about 28,416 times the frozen signed lower bound. This is a finite-path budget check only; it changes neither the frozen signed integral nor the original goal-weighted result and makes no continuum claim.
- Riemann, P vs NP, Yang–Mills, quantum gravity, dark matter, and dark energy: no new result is claimed by this board. These are proposed attack tracks, not completed advances.

## Reference points

- Clay Mathematics Institute, *The Millennium Prize Problems*: https://www.claymath.org/millennium-problems/
- NASA Science, *Dark Matter*: https://science.nasa.gov/dark-matter/
- NASA Science, *What is Dark Energy?*: https://science.nasa.gov/dark-energy/
- Prince Upadhyay, *Master Research Dossier*, 1 October 2026 (source document in Library).


## WP19 v0.28 structural attack — 3 October 2026

**Disposition:** `STRUCTURAL_BOTTLENECK_IDENTIFIED; JOINT_PAIRING_THEOREM_SHAPE_DERIVED; NUMERICAL_CLOSURE_OPEN`

### Frozen provenance

- GitHub Actions run `37049588602`; artifact `11251177469`, `wp19-v0-28-m15-targeted-220-239`.
- Artifact SHA-256: `7186f6922efcaec2f3e612c18d68b2335319fa1c61a48a900703712f4828801f`; the downloaded ZIP reproduces this digest.
- Source branch/PR: `wp19-v0-28-duality-compatibility-audit`, PR #155, head `d6639f86359a8d2c205bfd0cf67ab433a13ae94f`.
- Frozen input identities are carried in `m15_weighted_remainder.json`; exact-rational replay script checks the artifact digest and the updated quadratic/total values at their published outward-decimal precision.

### Exact implemented terms and source relaxations

For half-step `n`, width `h=1/80000`, the updated quadratic upper is

`Q_n = h E_n^2 W_n`,

where `E_n` is the global M15 L2 difference radius from the scalar forced-radius recurrence. The replay recovers the old Young coefficient from the serialized M14 quadratic row and its source radius, applies the M15 support correction on steps 0–219, and replaces steps 220–239 by the direct 192-bit Arb M15-support coefficient. The direct target coefficient is

`W_n = 15 sum_k |lambda_k| + sqrt(14147) sqrt(sum_k |k|^2 |lambda_k|^2)`

maximized over global Bernstein controls. This collapses all modes into two global sums before multiplication by the scalar error radius squared. It loses shell localization, phase, block orthogonality, and exact quadratic-form structure. The residual source has no per-shell error vector, and the aggregate artifacts do not serialize per-shell contributions.

The linear adjoint-defect term is

`L_n = h E_n D_n`,

where `D_n` is the Bernstein supremum of the global L2 norm of `lambda_t - (DN(U)^* lambda + nu |k|^2 lambda)`. It uses Cauchy–Schwarz between this global defect and the global primal L2 radius. These 240 terms sum to only `240,063.832492240296`.

The terminal boundary term is

`B_T = ||lambda(T)||_2 E_240`.

It uses a global terminal-adjoint L2 norm and the global M15 radius, with no signed endpoint pairing. The replay implies `||lambda(T)||_2 = 4,691,959,667,101.2573649...` and `E_240 = 10.559636070809868141657764813075`. The initial boundary is zero (`E_0=0`); internal integration-by-parts endpoints telescope by source design. The linear endpoint product is distinct from a terminal Taylor/Hessian remainder.

The scalar radius recurrence uses the global M14 gradient bound and full-M15 residual bound, with a Grönwall exponential. The energy derivation notes transport cancellation and viscosity dissipation, but the scalar recurrence does not retain frequency-block damping or signed strain information. The target coefficient uses a global Fourier Young bound. No further Cauchy–Schwarz or triangle split can be attributed to individual shells from the serialized output.

### Time decomposition

Exact-rational sums of the printed per-step outward rows (steps 0–219) and the target replay (steps 220–239) give the following 20-step quadratic contributions. Tiny last-place aggregation differences are covered by the published outward aggregate.

| Steps | Quadratic upper sum |
|---|---:|
| 0–19 | 56,851,493.5004 |
| 20–39 | 550,690,348.3996 |
| 40–59 | 2,487,531,778.4980 |
| 60–79 | 8,910,533,871.6721 |
| 80–99 | 28,731,796,488.2294 |
| 100–119 | 87,865,332,121.5261 |
| 120–139 | 262,855,070,512.0294 |
| 140–159 | 785,774,953,682.9028 |
| 160–179 | 2,383,065,138,218.1041 |
| 180–199 | 7,412,357,314,641.6179 |
| 200–219 | 23,830,256,274,409.9498 |
| 220–239 | 79,290,095,908,202.2205 |

The last 20 steps contribute about 69.5% of the updated quadratic term. Step 239 is largest at about `6.691946535049e12`. The endpoint term is a single time endpoint; it cannot be apportioned across time segments without changing the inequality.

### Updated budget and impact ceilings

| Quantity | Bound |
|---|---:|
| Whole-path quadratic `Q` | `114,093,007,395,768.6501` |
| Terminal boundary `B_T` | `49,545,386,543,507.4983` |
| Adjoint defect `L` | `240,063.8325` |
| Conservative sum `Q+B_T+L` | `163,638,394,179,339.9808` |
| Frozen signed-integral lower bound `P` | `5,758,574,435.6058` |
| Signed margin `P-(Q+B_T+L)` | `-163,632,635,604,904.3750` |
| Remainder / `P` | `28,416.4763` |

Removing `B_T` alone leaves a negative margin of about `-1.1408724906e14` (`Q/P` is about 19,811). Removing `Q` alone leaves about `-4.9539628209e13` (`B_T/P` is about 8,604). The defect term is negligible at this scale. A successful joint route must shrink or cancel essentially all of `Q+B_T`: to keep the same shapes and scale every radius uniformly by `alpha`, exact replay gives `alpha <= 0.0001161972`, a factor of about `8,606`; the terminal radius would need to fall from `10.5596` to about `0.001227`. Then `Q`, which is quadratic in the radius, falls to roughly `1.54e6`. These are necessary budget targets, not evidence such a bound holds.

### Theorem-shaped joint pairing identity

In the finite-dimensional M15 Galerkin system write `F(U)=-P(U·grad U)-nu A U`, `r=F(U)-U_t`, `e=V-U`, `A_U=DF(U)`, and `C(e,e)=F(U+e)-F(U)-A_U e`. Let `d=lambda_t + A_U^* lambda`; the code's defect `lambda_t-(DN(U)^*lambda+nu A lambda)` is this `d` under the stated vector-field convention. Then

`e_t = A_U e + C(e,e) + r`

and, by direct differentiation,

`d/dt <lambda,e> = <d,e> + <lambda,r> + <lambda,C(e,e)>`.

If `e(0)=0`, integrate to obtain

`<lambda(T),e(T)> = integral <lambda,r> + integral <d,e> + integral <lambda,C(e,e)>`.

If additionally `lambda(T)=grad G(U(T))`, then

`G(V(T))-G(U(T)) = integral <lambda,r> + integral <d,e> + integral <lambda,C(e,e)> + R_G`,

where `R_G = integral_0^1 (1-s) D^2G(U(T)+s e(T))[e(T),e(T)] ds`.

This exposes the strongest candidate: preserve the signed defect/nonlinear/terminal pairing jointly, rather than separately bounding `Q_n` and `||lambda(T)|| E_T`. The identity does not justify simply deleting the endpoint product: first verify the signed integral is the same `integral <lambda,r>`, certify terminal-gradient compatibility, enclose the true M15 error path, and bound the actual terminal Taylor remainder. The source explicitly says the current shard excludes the terminal Taylor remainder, adjoint/input-gradient uncertainty, and normalizer transfer; the present sum is therefore only the named finite-path budget, not a complete objective-transfer theorem.

### Ranked structural routes

1. **Joint signed second-order duality with endpoint compatibility.** Potential maximum budget effect: the whole `Q+B_T` block, `1.63638e14`; only this route can exploit endpoint/interior correlation. Proof gate: derive the identity against the exact frozen target semantics and certify the terminal condition and `R_G`.
2. **Mode-resolved dissipative/logarithmic-norm propagation of `e`.** Preserve the `-nu |k|^2` damping and measured strain by low/high blocks, then propagate error in the adjoint-relevant low modes. The budget ceiling includes both `Q` and `B_T` if it reduces the whole path radius; required uniform reduction is about `8,606x`. No current shell-resolved error vector establishes this.
3. **Exact signed quadratic form / frequency-localized pairing.** Can at most remove the current `Q` block (`1.14093e14`) if treated alone; the boundary term still misses sign by about `8,604x`. Needs the M15 error vector and mode-pair phases.
4. **Endpoint compatibility alone.** At most removes `B_T` (`4.95454e13`), leaving `Q` about `19,811` times the positive signed lower bound. Not sufficient alone.
5. **More local support-coefficient tightening.** Rejected as a primary route: the completed targeted change improved the full remainder by only `0.259%`.

### Best next proof/computation

This was the v0.3 proposal. The v0.4 semantic audit stopped before pilot code or compute because terminal-gradient compatibility over the endpoint tube and `R_G` are not certified. Reconsider the steps 220–239 pilot only after those semantic gates pass and a validated vector error enclosure at step 219 exists; then apply the predeclared 10^4 improvement gate before any full-path work.

Conditional files if the semantic and vector-state gates reopen:

- `src/wp19_v0_28_m15_joint_pairing_pilot.py` — interval M15 difference-vector propagation and signed per-shell pairings, retaining viscous block damping.
- `results/wp19_v0_28/joint_pairing_20261003/tail_220_239.json` — pilot certificate bound to the frozen lower path, adjoint, residual, and artifact hashes.
- Full-path result plus a shell-wise summation audit only if the pilot clears the four-order value gate.

Suggested GitHub Actions workflow: dispatch `wp19-v0-28-joint-pairing-pilot.yml`; download the exact frozen lower-path and adjoint artifacts by run/name; verify their hashes; run the M15 Arb error-vector and pairing code on steps 220–239; upload the JSON certificate plus a manifest with input/source hashes. Heavy compute is conditional on first validating the M15 error-state data and proving the identity matches the objective represented by the signed integral. No workflow was launched in this turn because the needed vector-valued M15 error path is absent from the frozen inputs.

### Replay and rigor notes

- `wp19_v0_28_structural_decomposition_replay.py` and its JSON output replay the artifact SHA and aggregate budget using exact rational decimal parsing.
- The artifact workflow's decimal ceiling helper is used on a negative signed margin. Ceil rounds that value upward by one unit at 24 decimal places; the safe outward floor is `-163632635604904.374992408432849939981122`. This is immaterial numerically but should be corrected in a certificate serializer.
- Finite-path audit only. No sign closure, all-cutoff result, continuum statement, or global-regularity claim is made.


## WP19 v0.28 joint signed-pairing pilot — semantic stop (3 October 2026)

**Disposition:** `STOP_SEMANTIC_GATE_FAILED_BEFORE_CODE_OR_HEAVY_COMPUTE`

The frozen signed integral is the signed integral of the saved Hermite/binary64 reconstructions, computed coefficientwise as `integral <lambda_reconstruction, r_reconstruction>` with `r=F_15(U)-U_t`. Thus frozen P equals that reconstructed pairing. It is not certified as the pairing along a rigorously enclosed M15 error trajectory. The adjoint export explicitly identifies its values and right-hand sides as binary64 reconstruction data, not an adjoint-trajectory or quadrature certificate.

The objective is the fixed degree-7 polynomial signed C500 numerator on P11 modes under the frozen K36 sign chart. The terminal adjoint is initialized from the floating gradient at a nominal projected endpoint. Exact terminal equality over the endpoint uncertainty set is not established. The frozen objective transfer excludes the terminal gradient/input-gradient uncertainty and the Taylor/Hessian term

`R_G = integral_0^1 (1-s) D^2G(U(T)+s e(T))[e(T),e(T)] ds`.

No rigorous bound for `R_G` is in the frozen files. This fails the user-defined semantic gate, so no pilot code or workflow was launched, and no signed shell totals, identity residual, or improvement factor are reported. The requested output path contains a stop record, not a numerical pilot certificate.

The finite-dimensional identity under the repository sign convention remains conditional: with `F(U)=-P_15(U·grad U)-nu A U`, `r=F(U)-U_t`, `e=V-U`, `A_U=DF(U)`, `C(e,e)=F(U+e)-F(U)-A_U e`, and `d=lambda_t+A_U^*lambda` (the code form is `lambda_t-(DN(U)^*lambda+nu A lambda)`),

`e_t=A_U e+C(e,e)+r`,

`d/dt <lambda,e> = <d,e> + <lambda,r> + <lambda,C(e,e)>`.

For `e(0)=0`, integrate to obtain `<lambda(T),e(T)> = integral<lambda,r> + integral<d,e> + integral<lambda,C(e,e)>`. The objective difference additionally requires `<grad G(U(T))-lambda(T),e(T)> + R_G`; neither term is certified away.

### Bottleneck decomposition and structural limits

The prior exact-rational replay already gives a time-band split: steps 0–19 `56,851,493.5004`; 20–39 `550,690,348.3996`; 40–59 `2,487,531,778.4980`; 60–79 `8,910,533,871.6721`; 80–99 `28,731,796,488.2294`; 100–119 `87,865,332,121.5261`; 120–139 `262,855,070,512.0294`; 140–159 `785,774,953,682.9028`; 160–179 `2,383,065,138,218.1041`; 180–199 `7,412,357,314,641.6179`; 200–219 `23,830,256,274,409.9498`; 220–239 `79,290,095,908,202.2205`. The final 20 steps account for about 69.5% of Q, with step 239 largest at about `6.691946535049e12`. The terminal endpoint term is not apportioned across time. Frozen aggregate files do not expose a mode/shell or primal/adjoint subterm split.

- Whole-path quadratic: `Q_n=h E_n^2 W_n`, `h=1/80000`; `E_n` is a scalar global L2 M15 error radius. `W_n` uses global Fourier sums and a global Bernstein control, including `15 sum|lambda_k| + sqrt(14147)*sqrt(sum |k|^2 |lambda_k|^2)`. Frozen aggregates do not expose per-shell, mode, source, or primal/adjoint subterm values, so the requested granular numerical decomposition is not recoverable without new data.
- Terminal boundary: `B_T=||lambda(T)||_2 E_240`, with reported `||lambda(T)||_2=4,691,959,667,101.2573649...` and `E_240=10.559636070809868141657764813075`. It is an independent global norm product, not a signed endpoint pairing.
- Adjoint defect: `L_n=h E_n D_n` uses a global L2 defect and global scalar error radius; Cauchy–Schwarz discards correlation. Its total `240,063.832492240296` is small beside Q and B.
- Scalar error propagation loses phase, shell damping and mode identity; the Young/Fourier coefficient and terminal product also erase signed or blockwise structure. The N15 same-datum artifact and adjoint exports are saved trajectory/reconstruction artifacts, not a certified modewise interval tube for `e_n`.

### Ranked candidates and maximum budget ceiling

1. **Joint signed duality with certified endpoint compatibility and Hessian remainder.** Ceiling: remove/cancel at most `Q+B_T = 163,638,394,179,276.148329841175920939981122` from the current bound (not an achieved reduction). The method can in principle use interior/endpoint correlation, but the current semantic, vector-state, and Hessian gates fail.
2. **Mode-block dissipative/logarithmic-norm propagation.** Potentially affects both Q and B if it gives adjoint-relevant mode contraction; no quantified result exists. The prior uniform-radius budget analysis calls for roughly an 8,606-fold reduction.
3. **Exact signed quadratic form/frequency localization.** Ceiling if used alone: Q=`114,093,007,395,768.650060299107920939981122`; B remains. Requires a complex-phase interval error vector.
4. **Endpoint compatibility alone.** Ceiling if used alone: B=`49,545,386,543,507.498269542068`; Q remains. Also requires a mismatch enclosure and `R_G`.
5. **Further local support-coefficient tightening.** Not pursued: prior full remainder reduction was 0.259%, far below the 28,416× gap.

### Next proof target

Before any tail run, certify (i) the exact endpoint map and terminal seed relation, including an interval enclosure of `grad G(U(T))-lambda(T)` over the full endpoint tube, and (ii) a rigorous Hessian supremum for the fixed polynomial G on that tube, yielding a bound for `R_G`. Define a replayable vector-state certificate supplying `e_219` and per-mode residual/state enclosures while preserving complex phase, conjugate symmetry, divergence-free projection, and viscosity. Only then reconsider the steps 220–239 pilot and its predeclared 10^4 gate.

**Gate status:** four-order pilot gate `NOT_RUN_SEMANTIC_STOP`; no shell pairings, joint identity residual, `R_G` interval, or pilot improvement factor. No full-path workflow was created or launched. Full stop-record provenance and SHA list are at `results/wp19_v0_28/joint_pairing_20261003/tail_220_239.json` and `SHA256SUMS.txt`. No continuum, regularity, blow-up, or Millennium claim is made.


## WP19 v0.28 semantic repair — v0.5 update (3 October 2026)

**Disposition:** `STOP_PILOT_NOT_AUTHORIZED`. The exact terminal objective is now recovered as a degree-seven sparse polynomial with all 536 frozen coefficients, its P11 mode convention, real-coordinate derivative rules, and source/artifact provenance. This repairs the objective-definition gate, but not the full joint-pairing semantics.

The exported terminal seed is assigned from the binary64 Torch gradient at the nominal P11 physical-projected predictor endpoint. The independent 192-bit Arb certificate bounds the nominal aggregate L2 difference by `0.002378116682`; equality is therefore approximate, not exact. The endpoint-ball certificate supplies a M14 endpoint L2 radius `0.000012825905` and aggregate gradient-variation L2 upper `15845467881.27747`, hence aggregate mismatch upper `15845467881.279848116682`. Per-mode mismatch intervals cannot be recovered because the frozen artifacts do not serialize the gradient or difference vectors componentwise.

The new exact-rational global Hessian certificate uses the analytic product-rule Hessian of the frozen polynomial and the M15 scalar radius `E_T=10.559636070809868141657764813075`. It gives `sup ||D²G|| <= 3.2223882545274038e24` and `R_G <= 1.7965767370810693e26`. The derivative implementation's fixed-seed full-support finite-difference sanity check and Hessian symmetry check pass at relative errors below `2e-7`; these are numerical diagnostics, while the Hessian/Taylor upper uses exact rational input arithmetic and integer-isqrt outward bounds. The global Taylor bound is about `3.12e16` times P and about `1.10e12` times the old Q+B+L budget: it is rigorous but unusable for closure.

The endpoint mismatch contribution is separately bounded by `B_grad <= 167322374198.021901...` using the aggregate gradient tube and M15 scalar endpoint error. This alone exceeds P by about `29.1x`. Frozen P matches the implemented quadrature of `<lambda_reconstruction,r_reconstruction>` on saved Hermite/binary64 data, but this does not certify equality with the exact integral along an interval-enclosed M15 path.

No modewise interval error vector at step 219 is present in the frozen artifacts; they provide scalar L2 radii and saved predictor data only. The earliest certified propagation state available is `e_0=0`; a proof-producing modewise propagation must begin at step 0 unless a separately validated interval checkpoint is supplied. The schema in `e219_certificate_spec.json` specifies the required complex balls, reality/divergence constraints, support, projection, viscosity, residuals, time conventions, and provenance.

### v0.5 gate and next target

- Exact objective reconstruction: **PASS**.
- Aggregate terminal-gradient mismatch over endpoint tube: **PASS as an L2 bound; per-mode comparison BLOCKED**.
- `B_grad`: **bounded separately, but too large to help the sign**.
- `R_G`: **rigorously bounded by a global scalar Hessian estimate, but route-killing in value**.
- `e_219` vector certificate: **not available**.
- Tail pilot and four-order gate: **not run; pilot not authorized**.

Next proof target: produce a modewise endpoint error tube and gradient-mismatch enclosure over the objective's active low-mode support, then evaluate the exact sparse Hessian quadratic form blockwise. Reopen the tail pilot only when this reduces the terminal Taylor term by orders of magnitude and a validated e-vector certificate is available. The finite-dimensional identity remains conditional on matching state/residual/adjoint conventions and certified quadrature.

Updated machine-readable gate: `results/wp19_v0_28/semantic_repair_20261003/semantic_repair_gate.json`. No continuum or global-regularity claim is made.


## WP19 v0.28 active-support endpoint feasibility — v0.6 (3 October 2026)

**Disposition: ACTIVE_SUPPORT_ROUTE_BLOCKED.** The exact frozen objective formula footprint was independently reconstructed from its 536 coefficient rows at PR #155 head `02df009de32e669355a7b915edff5608b9b8f863`: 1,159 Fourier mode entries, 937 conjugate pairs, 3,748 independent real solenoidal coordinates before real-coordinate polynomial cancellation, with maximum `|k|=11`. The objective is evaluated after P11 truncation and physical projection; M15 modes outside P11 do not enter G directly.

The supplied screenshot reports a symbolic real-coordinate reduction to 3,740 active coordinates, one connected Hessian component, an approximately 826-fold Hessian rebound, and an active-only perturbation of norm at most 5.6 with `|R_G| >= 7.553e9 > P`. The underlying coordinate cancellation map, Hessian graph, sparse-bound source, and perturbation witness were not available in this workspace, so those screenshot-only numbers are recorded as reported, not independently verified. A machine-readable exact formula-footprint list is included; it is explicitly not presented as the post-cancellation coordinate list.

Using the global certified Hessian upper `H=3.222388254527403832581260762399...e24`, the outward-safe active error radius needed for `|R_G|<=P` is below `5.9783805641154709e-8`; using the screenshot's approximate 826 factor gives about `1.718199471071945329e-6`. For `0.1P`, those thresholds are `1.8905299301887187e-8` and about `5.43342380308393824e-7`. The available certified projection bound is only the scalar `E_T=10.559636070809868...`, over 6.1 million times the approximate active-support threshold. The previously certified aggregate `B_grad=1.67322374198e11` already exceeds P; no active-mode mismatch vector is available.

Fourier selection rules also defeat a simple closed low-mode subsystem: the exact lattice count gives 9,001,373 ordered M15 convolution slots into the formula-active outputs with both inputs outside the active formula support, and 10,836,849 slots with at least one such input. These counts precede divergence-free coefficient cancellations. A coarse unitary-Fourier estimate is `||P_S B(x,y)||_2 <= 15 sqrt(1159)||x||_2||y||_2`; the two linearized cross terms cost at most `30 sqrt(1159)||U||_2||e||_2`. Modes outside P11 have `|k|^2>=122`, so their viscous decay is at least `122 nu`; no certified low/high forcing inequality with useful constants follows from the stored scalar radii. The projection residual also has only a global bound.

**Gate:** `FAIL` for continuing this route with present frozen uncertainty. Do not launch projected vector propagation or the 220–239 pilot. Further generic endpoint/Hessian tightening is no longer a primary route. The screenshot's claimed perturbation would strengthen this to `ACTIVE_SUPPORT_ROUTE_FALSIFIED_UNDER_CURRENT_UNCERTAINTY` once its exact witness and arithmetic are checked in; this classification concerns the current enclosure's ability to certify a sign, not the actual M15 trajectory.

Next direction: freeze WP19 endpoint/joint-pairing as blocked pending genuinely new modewise endpoint and residual data. Redirect proof effort to a structurally different target (the Riemann R0.12 line from the handoff), while retaining the current finite M14/M15 audit as a bounded negative result. No continuum regularity, blow-up, or Millennium claim is made.
