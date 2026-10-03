#!/usr/bin/env python3
"""WP19 v0.28 exact-rational global Hessian/Taylor bound for terminal G.

The objective is the frozen degree-seven polynomial specified by
results/wp19_v0_28/semantic_repair_20261003/objective_definition.json.
This checker derives its first and second directional derivatives from the
bilinear maps B and D_g by the product rule, runs directional finite-difference
sanity checks on the exact frozen coefficient support, and emits an exact-
rational outward global Hessian bound.  The bound is intentionally global and
coarse; it is not a modewise endpoint evaluation.

No Arb dependency is needed: every reported enclosure is constructed using
Fractions and integer square roots.  Floating point is used only for the
non-certifying directional derivative sanity diagnostics.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from random import Random

P, Q, K = (3, 2, 2), (3, -2, 1), (6, 0, 3)
WEIGHT = 2025
MAX_MODE_RADIUS = 11
SUM_ABS_COEFF = 36 + 9 * 500


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sqrt_upper(q: Fraction, places: int = 40) -> Fraction:
    """Return a rational decimal-grid upper bound for sqrt(q), exactly."""
    if q < 0:
        raise ValueError("negative square-root input")
    scale = 10**places
    n, d = q.numerator * scale * scale, q.denominator
    m = math.isqrt(n // d)
    if m * m * d < n:
        m += 1
    return Fraction(m, scale)


def dec(q: Fraction, places: int = 24) -> str:
    """Outward upper endpoint: ceiling on a fixed decimal grid."""
    scale = 10**places
    n = q.numerator * scale
    k = -((-n) // q.denominator)  # ceil(n/d), valid for either sign
    return f"{k // scale}.{abs(k) % scale:0{places}d}" if k >= 0 else f"-{(-k) // scale}.{(-k) % scale:0{places}d}"


def dec_lower(q: Fraction, places: int = 24) -> str:
    """Outward lower endpoint: floor, including for negative certificates."""
    scale = 10**places
    k = (q.numerator * scale) // q.denominator  # Python // is mathematical floor
    return f"{k // scale}.{abs(k) % scale:0{places}d}" if k >= 0 else f"-{(-k) // scale}.{(-k) % scale:0{places}d}"


def orbit(k):
    return tuple(sorted(abs(int(x)) for x in k))


def modes_ball(radius=MAX_MODE_RADIUS):
    return [(i, j, k) for i in range(-radius, radius + 1)
            for j in range(-radius, radius + 1)
            for k in range(-radius, radius + 1)
            if i*i + j*j + k*k <= radius*radius]


def proj_k(x):
    # P_K = I - K K^T/|K|^2; |K|^2=45.
    import numpy as np
    v = np.asarray(K, dtype=float)
    return np.asarray(x) - v * (np.dot(v, x) / 45.0)


class Objective:
    def __init__(self, coeff_rows):
        import numpy as np
        self.np = np
        self.modes = modes_ball()
        self.index = {k: i for i, k in enumerate(self.modes)}
        self.pi, self.qi, self.ki = (self.index[x] for x in (P, Q, K))
        self.groups = {}
        for row in coeff_rows:
            key = (tuple(row["left_orbit"]), tuple(row["right_orbit"]))
            self.groups[key] = int(row["coefficient"])
        wanted = set(self.groups)
        self.pairs = {key: [] for key in wanted}
        for li, ell in enumerate(self.modes):
            r = tuple(K[i] - ell[i] for i in range(3))
            ri = self.index.get(r)
            if ri is None:
                continue
            key = (orbit(ell), orbit(r))
            if key in wanted:
                self.pairs[key].append((li, ri, r))
        if set(k for k, v in self.pairs.items() if v) != wanted:
            raise ValueError("objective support not fully represented in |k|<=11")

    def maps(self, a, h=None, k=None):
        """Return B/B1/B2 and each D/D1/D2 for directional vectors h,k."""
        np = self.np
        zero = np.zeros_like(a)
        h = zero if h is None else h
        k = zero if k is None else k
        B = proj_k(1j * np.dot(Q, a[self.pi]) * a[self.qi])
        B1h = proj_k(1j * (np.dot(Q, h[self.pi]) * a[self.qi] + np.dot(Q, a[self.pi]) * h[self.qi]))
        B1k = proj_k(1j * (np.dot(Q, k[self.pi]) * a[self.qi] + np.dot(Q, a[self.pi]) * k[self.qi]))
        B2 = proj_k(1j * (np.dot(Q, h[self.pi]) * k[self.qi] + np.dot(Q, k[self.pi]) * h[self.qi]))
        D, D1h, D1k, D2 = {}, {}, {}, {}
        for key, pairs in self.pairs.items():
            vals = [np.zeros(3, complex) for _ in range(4)]
            for li, ri, r in pairs:
                rv = np.asarray(r, float)
                vals[0] -= proj_k(1j * np.dot(rv, a[li]) * a[ri])
                vals[1] -= proj_k(1j * (np.dot(rv, h[li]) * a[ri] + np.dot(rv, a[li]) * h[ri]))
                vals[2] -= proj_k(1j * (np.dot(rv, k[li]) * a[ri] + np.dot(rv, a[li]) * k[ri]))
                vals[3] -= proj_k(1j * (np.dot(rv, h[li]) * k[ri] + np.dot(rv, k[li]) * h[ri]))
            D[key], D1h[key], D1k[key], D2[key] = vals
        return B, B1h, B1k, B2, D, D1h, D1k, D2

    def value_d1_d2(self, a, h, k):
        """Evaluate G(a), DG(a)[h], D2G(a)[h,k] by exact product structure."""
        np = self.np
        B, B1h, B1k, B2, D, D1h, D1k, D2 = self.maps(a, h, k)
        z = -WEIGHT * np.vdot(a[self.ki], B)
        z1h = -WEIGHT * (np.vdot(h[self.ki], B) + np.vdot(a[self.ki], B1h))
        z1k = -WEIGHT * (np.vdot(k[self.ki], B) + np.vdot(a[self.ki], B1k))
        z2 = -WEIGHT * (np.vdot(h[self.ki], B1k) + np.vdot(k[self.ki], B1h) + np.vdot(a[self.ki], B2))
        G = d1 = d2 = 0.0
        for key, c in self.groups.items():
            w = -WEIGHT * np.vdot(D[key], B)
            w1h = -WEIGHT * (np.vdot(D1h[key], B) + np.vdot(D[key], B1h))
            w1k = -WEIGHT * (np.vdot(D1k[key], B) + np.vdot(D[key], B1k))
            w2 = -WEIGHT * (np.vdot(D2[key], B) + np.vdot(D1h[key], B1k) + np.vdot(D1k[key], B1h) + np.vdot(D[key], B2))
            G += c * float(np.imag(w * np.conj(z)))
            d1 += c * float(np.imag(w1h * np.conj(z) + w * np.conj(z1h)))
            d2 += c * float(np.imag(w2 * np.conj(z) + w1h * np.conj(z1k) + w1k * np.conj(z1h) + w * np.conj(z2)))
        return G, d1, d2


def run(args):
    import numpy as np
    obj_path = Path(args.objective)
    forced_path = Path(args.forced_radius)
    endpoint_path = Path(args.endpoint_ball)
    objective_json = json.loads(obj_path.read_text())
    coeff_rows = objective_json["coefficient_rows"]
    if len(coeff_rows) != 536 or sum(abs(int(r["coefficient"])) for r in coeff_rows) != SUM_ABS_COEFF:
        raise ValueError("frozen coefficient cardinality or l1 norm mismatch")
    model = Objective(coeff_rows)

    # Deterministic non-certifying finite-difference sanity test on the exact
    # frozen support. This exercises the full 536-group polynomial.
    rng = np.random.default_rng(19028)
    a = np.zeros((len(model.modes), 3), dtype=np.complex128)
    h = np.zeros_like(a); k = np.zeros_like(a)
    touched = sorted({ix for pairs in model.pairs.values() for li, ri, _ in pairs for ix in (li, ri)} | {model.pi, model.qi, model.ki})
    for ix in touched:
        a[ix] = rng.normal(size=3) + 1j*rng.normal(size=3)
        h[ix] = rng.normal(size=3) + 1j*rng.normal(size=3)
        k[ix] = rng.normal(size=3) + 1j*rng.normal(size=3)
    G0, d1, d2 = model.value_d1_d2(a, h, k)
    eps = 2e-4
    gp = model.value_d1_d2(a + eps*h, h, k)[0]
    gm = model.value_d1_d2(a - eps*h, h, k)[0]
    fd1 = (gp - gm)/(2*eps)
    mixed = (model.value_d1_d2(a+eps*h+eps*k,h,k)[0] - model.value_d1_d2(a+eps*h-eps*k,h,k)[0]
             - model.value_d1_d2(a-eps*h+eps*k,h,k)[0] + model.value_d1_d2(a-eps*h-eps*k,h,k)[0])/(4*eps*eps)
    _, _, d2kh = model.value_d1_d2(a, k, h)
    fd1_rel = abs(fd1-d1)/max(1.0,abs(fd1),abs(d1))
    fd2_rel = abs(mixed-d2)/max(1.0,abs(mixed),abs(d2))
    sym_rel = abs(d2-d2kh)/max(1.0,abs(d2),abs(d2kh))
    frozen_margin = Fraction("-163632635604904.374992408432849939981122")
    safe_margin = dec_lower(frozen_margin)

    forced = json.loads(forced_path.read_text())
    endpoint = json.loads(endpoint_path.read_text())
    E = Fraction(forced["final_forced_error_L2_upper"])
    delta14 = Fraction(endpoint["certified_endpoint_uncertainty"]["lower_cutoff_terminal_L2_error_upper_decimal"])
    u0_sq = Fraction(621401994135931720911914617315947586894290053276728518977463107567623,
                     50234486915870484862364730000000000000000000000000000000000000000)
    u0 = sqrt_upper(u0_sq)
    R = u0 + delta14 + E

    # Bounds: ||B||<=sqrt(14)R^2, ||D_g||<=11R^2,
    # ||Z||<=sqrt(14)WR^3, ||Z'||<=3sqrt(14)WR^2,
    # ||Z''||<=6sqrt(14)WR, ||W'_g||<=44sqrt(14)WR^3,
    # ||W''_g||<=132sqrt(14)WR^2. Their product-rule Hessian coefficient
    # is 14*(132 + 2*44*3 + 11*6) = 6468 before W^2*sum|c|.
    # The factor 14 comes from the two sqrt(14) factors in each product.
    hess_coeff = Fraction(SUM_ABS_COEFF * WEIGHT**2 * 14 * (132 + 2*44*3 + 11*6))
    H = hess_coeff * R**5
    RG = Fraction(1,2) * H * E**2

    # Floating display of gradient mismatch is the rigorous aggregate tube
    # mismatch from the existing Arb certificates, not a per-mode vector.
    grad_tube = Fraction("15845467881.27747") + Fraction("0.002378116682")
    Bgrad = grad_tube * E
    P = Fraction("5758574435.605829673039071")
    old_tail = Fraction("114093007395768.650060299107920939981122") + Fraction("49545386543507.498269542068")
    out = {
        "schema": "wp19-v0.28-terminal-hessian-remainder-v1",
        "status": "PASS_COARSE_GLOBAL_HESSIAN_BOUND_ROUTE_KILLING",
        "arithmetic": "exact rational input arithmetic; sqrt upper bounds from integer isqrt; outward decimal ceiling",
        "input_sha256": {"objective_definition": sha(obj_path), "forced_radius": sha(forced_path), "endpoint_gradient_ball": sha(endpoint_path)},
        "objective_degree": 7,
        "coefficient_rows": len(coeff_rows),
        "sum_absolute_coefficients": SUM_ABS_COEFF,
        "mode_count_ball_radius_11": len(model.modes),
        "represented_objective_groups": len(model.pairs),
        "directional_sanity_noncertifying": {
            "seed": 19028, "epsilon": eps, "G_at_test_point": G0,
            "first_directional_relative_error": fd1_rel,
            "mixed_second_directional_relative_error": fd2_rel,
            "Hessian_symmetry_relative_error": sym_rel,
            "pass_threshold": 2e-5,
            "pass": max(fd1_rel,fd2_rel,sym_rel) < 2e-5,
        },
        "outward_rounding_check": {"rule":"lower endpoints use floor; upper endpoints use ceiling", "frozen_negative_margin_exact":str(frozen_margin), "safe_lower_24_places":safe_margin, "expected_safe_lower_24_places":"-163632635604904.374992408432849939981122", "pass":safe_margin == "-163632635604904.374992408432849939981122"},
        "analytic_derivative": "B1[h]=B(h,a)+B(a,h), B2[h,k]=B(h,k)+B(k,h); D derivatives are the same bilinear product rule; D2G is the four-factor product rule in the source implementation.",
        "endpoint_radius_inputs": {"initial_energy_norm_upper": dec(u0), "M14_terminal_uncertainty": str(delta14), "M15_error_radius": str(E), "global_segment_norm_radius_R": dec(R)},
        "hessian_operator_bound": {"coefficient_exact": str(hess_coeff), "R_power": 5, "upper_decimal": dec(H)},
        "terminal_taylor_remainder": {"formula": "0.5 * sup_{segment} ||D^2G|| * ||e(T)||^2", "upper_exact_fraction": str(RG), "upper_decimal": dec(RG), "scope": "M15 scalar L2 error ball; global polynomial Hessian bound; no modewise endpoint vector"},
        "comparison": {"frozen_signed_integral_P": str(P), "RG_over_P_upper_ratio_decimal": dec(RG/P), "old_Q_plus_B_majorant": str(old_tail), "RG_over_old_Q_plus_B_ratio_decimal": dec(RG/old_tail), "pilot_gate": "STOP; this scalar-only Taylor bound is many orders above P and cannot certify useful joint closure"},
        "claim_boundary": "Finite-dimensional frozen terminal objective and M15 scalar-radius bound only; no joint-pairing pilot, no sign closure, no all-cutoff or continuum Navier-Stokes claim."
    }
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(out_path), "hessian_upper": out["hessian_operator_bound"]["upper_decimal"], "RG_upper": out["terminal_taylor_remainder"]["upper_decimal"], "sanity": out["directional_sanity_noncertifying"], "sha256": sha(out_path)}, indent=2))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--objective", required=True)
    p.add_argument("--forced-radius", required=True)
    p.add_argument("--endpoint-ball", required=True)
    p.add_argument("--output", required=True)
    run(p.parse_args())


if __name__ == "__main__":
    main()
