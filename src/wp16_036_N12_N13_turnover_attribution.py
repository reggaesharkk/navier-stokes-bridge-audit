"""Post-hoc N12/N13 source-orbit attribution of the early K36 margin turnover.

Reconstructs the six archived finite-Galerkin states, evolves them only on the
already-used dt=1e-4 grid through t=0.001, and takes local directional
central differences along the Galerkin RHS. The N11-derived K36 coalition,
phase states, and prospective holdout results are never retuned.

Finite post-hoc mechanism diagnostic only; not a prospective holdout,
cutoff-uniform estimate, continuum result, or Navier-Stokes regularity proof.
"""

import argparse
from collections import defaultdict
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np

import wp16_036_N12_frozen_K36_holdout as hold
from wp16_036_dealiased_trajectory_gate import DealiasedSystem

DT = 1e-4
STEPS = 10
TRACE_H = 1e-8
STABILITY_H = (5e-9, 1e-8, 2e-8, 4e-8)
TOP = 10
STATE_NAMES = ("inherited", "target_only", "full_final")
LEADING_GROUP = ((3, 3, 4), (0, 2, 3))

EXPECTED_LF_SHA256 = {
    "n10_n11": "34a10cf119ab6614c46d29540c4d4701eab082229582fb0a8189add0cd8f96a5",
    "n12": "ec07d1a263eb43c1a1d6228164ba80a4e29b90b6206bb606c612192a4ee38855",
    "n13": "13e5e56676b9398e7c7ec32f55e32a4d07dec5a3830c67787c6cd6fb5c8e59cd",
}
SOURCE_GZ_SHA256 = "ab238d8df279eb925cf8145cb33cb5670513aea61a2547a1ac0a7ae1b1493f95"
SOURCE_JSON_SHA256 = "193cbb7f485ab54ceed0d5cb38f97f0fc98c197e5f88e288fdbd277627608c8e"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json_checked(path, expected_lf_sha=None):
    raw = path.read_bytes().replace(b"\r\n", b"\n")
    actual = digest(raw)
    if expected_lf_sha is not None and actual != expected_lf_sha:
        raise ValueError(f"LF-normalized SHA-256 mismatch for {path}: {actual}")
    return json.loads(raw), actual


def read_source(path):
    raw = path.read_bytes()
    if path.suffix == ".gz":
        if digest(raw) != SOURCE_GZ_SHA256:
            raise ValueError(f"compressed source SHA-256 mismatch: {digest(raw)}")
        raw = gzip.decompress(raw)
    else:
        raw = raw.replace(b"\r\n", b"\n")
    if digest(raw) != SOURCE_JSON_SHA256:
        raise ValueError(f"source JSON SHA-256 mismatch: {digest(raw)}")
    return json.loads(raw)


def prepare_groups(system):
    ki = system.index[hold.K]
    keys, key_to_id = [], {}
    gids = np.empty(len(system.left), dtype=np.int32)
    for n, (li, ri) in enumerate(zip(system.left, system.right)):
        key = (hold.orbit(system.modes[int(li)]), hold.orbit(system.modes[int(ri)]))
        gid = key_to_id.get(key)
        if gid is None:
            gid = len(keys)
            key_to_id[key] = gid
            keys.append(key)
        gids[n] = gid
    return {
        "ki": ki, "li": system.left, "ri": system.right,
        "keys": keys, "key_to_id": key_to_id, "gids": gids,
        "Pk": system.projectors[ki], "weight": float(system.square[ki] ** 2),
    }


def rhs_batch(system, a):
    """Same dealiased RHS as DealiasedSystem.rhs, vectorized over states."""
    f = np.zeros((len(a), system.L, system.L, system.L, 3), complex)
    f[:, system.slots[0], system.slots[1], system.slots[2], :] = a
    u = np.fft.ifftn(f, axes=(1, 2, 3)) * system.L**3
    prod = np.zeros_like(u)
    for j in range(3):
        wave = system.waves_grid(j)[None, ..., None]
        grad = np.fft.ifftn(1j * wave * f, axes=(1, 2, 3)) * system.L**3
        prod += u[..., j, None] * grad
    conv = np.fft.fftn(prod, axes=(1, 2, 3))[:, system.slots[0], system.slots[1], system.slots[2], :] / system.L**3
    nonlinear = np.einsum("kij,bkj->bki", system.projectors, conv)
    return -nonlinear - system.nu * system.square[None, :, None] * a


def rk4_batch_with_k1(system, a, dt, k1):
    k2 = rhs_batch(system, a + dt * k1 / 2)
    k3 = rhs_batch(system, a + dt * k2 / 2)
    k4 = rhs_batch(system, a + dt * k3)
    return a + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)


def grouped_values(system, a, prep):
    pi, qi, ki = system.index[hold.P], system.index[hold.Q], prep["ki"]
    b = prep["Pk"] @ (1j * np.dot(np.asarray(hold.Q, float), a[pi]) * a[qi])
    z = -prep["weight"] * np.vdot(a[ki], b)
    if abs(z) < 1e-30:
        raise ValueError("tracked normalizer vanished")
    li, ri = prep["li"], prep["ri"]
    qdot = np.einsum("ij,ij->i", system.waves[ri], a[li])
    raw = 1j * qdot[:, None] * a[ri]
    dak = -(raw @ prep["Pk"].T)
    dz = -prep["weight"] * np.einsum("ij,j->i", np.conj(dak), b)
    sums = np.zeros(len(prep["keys"]), dtype=complex)
    np.add.at(sums, prep["gids"], dz)
    return np.imag(sums / z), z


def rates_with_velocity(system, a, velocity, prep, frozen_mask, h):
    g0, z0 = grouped_values(system, a, prep)
    gp, _ = grouped_values(system, a + h * velocity, prep)
    gm, _ = grouped_values(system, a - h * velocity, prep)
    abs0 = np.abs(g0)
    rates = (np.abs(gp) - np.abs(gm)) / (2 * h)
    inside = float(abs0[frozen_mask].sum())
    outside = float(abs0[~frozen_mask].sum())
    inside_rate = float(rates[frozen_mask].sum())
    outside_rate = float(rates[~frozen_mask].sum())
    return {
        "inside": inside, "outside": outside,
        "mass_fraction": inside / (inside + outside), "F": inside - 9 * outside,
        "inside_rate": inside_rate, "outside_rate": outside_rate,
        "F_rate": inside_rate - 9 * outside_rate,
        "group_rates": rates, "group_abs": abs0, "normalizer": z0,
    }


def top_outside(prep, frozen_mask, d, n=TOP):
    ids = np.flatnonzero(~frozen_mask)
    order = ids[np.argsort(d["group_rates"][ids])[::-1]]
    rows = []
    for idx in order[:n]:
        key = prep["keys"][int(idx)]
        rows.append({
            "left_orbit": list(key[0]), "right_orbit": list(key[1]),
            "absolute_mass_rate": float(d["group_rates"][idx]),
            "absolute_mass": float(d["group_abs"][idx]),
        })
    return rows


def archived_anchor_rate(archive, N, state):
    return float(archive["N"][str(N)][state]["anchor"]["rates"]["1e-08"]["full"]["margin_central"])


def run(args):
    j11, h11 = read_json_checked(args.n10_n11, EXPECTED_LF_SHA256["n10_n11"])
    j12, h12 = read_json_checked(args.n12, EXPECTED_LF_SHA256["n12"])
    j13, h13 = read_json_checked(args.n13, EXPECTED_LF_SHA256["n13"])
    source = read_source(args.source)
    archive, _ = read_json_checked(args.margin_velocity)
    frozen = set(hold.frozen_keys(source))
    assert len(frozen) == 36
    hold.System = DealiasedSystem

    result = {
        "status": "post-hoc finite N12/N13 K36 turnover source-rate attribution; no retuning",
        "input_sha256": {
            "n10_n11_lf_normalized": h11, "n12_lf_normalized": h12, "n13_lf_normalized": h13,
            "source_json_uncompressed": SOURCE_JSON_SHA256,
            "source_gzip": SOURCE_GZ_SHA256 if args.source.suffix == ".gz" else None,
        },
        "dt": DT, "steps": STEPS, "directional_step": TRACE_H, "frozen_K36_size": 36,
        "leading_common_outside_group": {"left_orbit": list(LEADING_GROUP[0]), "right_orbit": list(LEADING_GROUP[1])},
        "N": {}, "persistent_t001_outside_growth_groups": [], "checks": {},
        "interpretation_rule": (
            "Post-hoc finite-Galerkin mechanism diagnostic. Source rankings and sampled turnover times are descriptive; "
            "no frozen key, phase, or threshold is retuned and no all-N/continuum claim follows."
        ),
    }
    occurrence = defaultdict(lambda: {"states": 0, "ranks": [], "rates": []})
    max_archive_error = 0.0
    detailed_stability = None

    for N, prev, curr in (
        (12, hold.get_row(j11, 11), hold.get_row(j12, 12)),
        (13, hold.get_row(j12, 12), hold.get_row(j13, 13)),
    ):
        system, states = hold.reconstruct(prev, curr)
        prep = prepare_groups(system)
        frozen_mask = np.asarray([key in frozen for key in prep["keys"]], bool)
        lead_id = prep["key_to_id"][LEADING_GROUP]
        A = np.stack([states[name] for name in STATE_NAMES])

        batch_v = rhs_batch(system, A)
        batch_error = float(np.max(np.abs(batch_v[0] - system.rhs(A[0]))))
        if batch_error > 2e-10:
            raise AssertionError((N, "batch RHS mismatch", batch_error))

        state_rows = {name: {"trace": [], "first_sampled_negative_F_rate_time": None,
                             "first_sampled_positive_leading_group_rate_time": None}
                      for name in STATE_NAMES}
        endpoint_ds = {}

        for step in range(STEPS + 1):
            V = rhs_batch(system, A)
            for i, name in enumerate(STATE_NAMES):
                d = rates_with_velocity(system, A[i], V[i], prep, frozen_mask, TRACE_H)
                lead_rate = float(d["group_rates"][lead_id])
                state_rows[name]["trace"].append({
                    "t": step * DT,
                    "mass_fraction": d["mass_fraction"],
                    "F": d["F"],
                    "I_rate": d["inside_rate"],
                    "O_rate": d["outside_rate"],
                    "F_rate": d["F_rate"],
                    "leading_group_rate": lead_rate,
                })
                if state_rows[name]["first_sampled_negative_F_rate_time"] is None and d["F_rate"] < 0:
                    state_rows[name]["first_sampled_negative_F_rate_time"] = step * DT
                if state_rows[name]["first_sampled_positive_leading_group_rate_time"] is None and lead_rate > 0:
                    state_rows[name]["first_sampled_positive_leading_group_rate_time"] = step * DT
                if step == 0:
                    archived_rate = archived_anchor_rate(archive, N, name)
                    err = d["F_rate"] - archived_rate
                    max_archive_error = max(max_archive_error, abs(err))
                    if abs(err) > 2e-4:
                        raise AssertionError((N, name, d["F_rate"], archived_rate, err))
                    state_rows[name]["anchor_F_rate_archived"] = archived_rate
                    state_rows[name]["anchor_F_rate_difference_from_archive"] = err
                if step == STEPS:
                    endpoint_ds[name] = d
            if step < STEPS:
                A = rk4_batch_with_k1(system, A, DT, V)

        if N == 13:
            V = rhs_batch(system, np.stack([states["inherited"]]))[0]
            detailed_stability = {
                f"{h:.0e}": rates_with_velocity(system, states["inherited"], V, prep, frozen_mask, h)["F_rate"]
                for h in STABILITY_H
            }

        result["N"][str(N)] = {}
        for name in STATE_NAMES:
            endpoint = state_rows[name]["trace"][-1]
            d_end = endpoint_ds[name]
            top10 = top_outside(prep, frozen_mask, d_end, TOP)
            for rank, row in enumerate(top10, 1):
                key = (tuple(row["left_orbit"]), tuple(row["right_orbit"]))
                occurrence[key]["states"] += 1
                occurrence[key]["ranks"].append(rank)
                occurrence[key]["rates"].append(float(row["absolute_mass_rate"]))
            top5_sum = sum(row["absolute_mass_rate"] for row in top10[:5])
            state_rows[name]["ordered_outside_group_count"] = int((~frozen_mask).sum())
            state_rows[name]["t001"] = {
                "I_rate": d_end["inside_rate"],
                "O_rate": d_end["outside_rate"],
                "nine_O_rate": 9 * d_end["outside_rate"],
                "F_rate": d_end["F_rate"],
                "leading_group_rate": float(d_end["group_rates"][lead_id]),
                "leading_group_share_of_net_O_rate": float(d_end["group_rates"][lead_id]) / d_end["outside_rate"],
                "top5_positive_outside_rate_sum": top5_sum,
                "top5_positive_outside_rate_share_of_net_O_rate": top5_sum / d_end["outside_rate"],
                "top10_outside_growth": [
                    {"left_orbit": r["left_orbit"], "right_orbit": r["right_orbit"],
                     "rate": r["absolute_mass_rate"], "absolute_mass": r["absolute_mass"]}
                    for r in top10
                ],
            }
            result["N"][str(N)][name] = state_rows[name]
            print("CHECKED", N, name, "F'(0)=", state_rows[name]["trace"][0]["F_rate"],
                  "F'(.001)=", endpoint["F_rate"], "lead'(.001)=", state_rows[name]["t001"]["leading_group_rate"], flush=True)

    persistent = []
    for key, row in occurrence.items():
        persistent.append({
            "left_orbit": list(key[0]), "right_orbit": list(key[1]),
            "top10_occurrence_count_out_of_6": row["states"],
            "mean_rank_when_present": float(np.mean(row["ranks"])),
            "mean_rate_when_present": float(np.mean(row["rates"])),
        })
    persistent.sort(key=lambda x: (-x["top10_occurrence_count_out_of_6"], x["mean_rank_when_present"], -x["mean_rate_when_present"]))
    result["persistent_t001_outside_growth_groups"] = persistent
    result["checks"] = {
        "max_abs_anchor_F_rate_difference_from_archived_margin_velocity": max_archive_error,
        "N13_inherited_anchor_F_rate_stability": detailed_stability,
        "N13_inherited_anchor_F_rate_stability_spread": max(detailed_stability.values()) - min(detailed_stability.values()),
        "all_six_t001_I_rates_positive": all(result["N"][N][s]["t001"]["I_rate"] > 0 for N in ("12", "13") for s in STATE_NAMES),
        "all_six_t001_O_rates_positive": all(result["N"][N][s]["t001"]["O_rate"] > 0 for N in ("12", "13") for s in STATE_NAMES),
        "all_six_t001_F_rates_negative": all(result["N"][N][s]["t001"]["F_rate"] < 0 for N in ("12", "13") for s in STATE_NAMES),
        "leading_common_group_rank1_at_t001_all_six": all(
            result["N"][N][s]["t001"]["top10_outside_growth"][0]["left_orbit"] == list(LEADING_GROUP[0])
            and result["N"][N][s]["t001"]["top10_outside_growth"][0]["right_orbit"] == list(LEADING_GROUP[1])
            for N in ("12", "13") for s in STATE_NAMES
        ),
    }

    stored = {
        "status": result["status"],
        "input_sha256": result["input_sha256"],
        "dt": DT, "steps_to_t001": STEPS, "directional_step": TRACE_H,
        "frozen_K36_size": 36,
        "leading_common_outside_group": result["leading_common_outside_group"],
        "states": {},
        "persistent_t001_top10_groups_all_six": [
            {"left_orbit": r["left_orbit"], "right_orbit": r["right_orbit"],
             "mean_rank": r["mean_rank_when_present"], "mean_rate": r["mean_rate_when_present"]}
            for r in result["persistent_t001_outside_growth_groups"]
            if r["top10_occurrence_count_out_of_6"] == 6
        ],
        "checks": result["checks"],
        "interpretation_rule": result["interpretation_rule"],
    }
    for N in ("12", "13"):
        stored["states"]["N" + N] = {}
        for name in STATE_NAMES:
            row = result["N"][N][name]
            stored["states"]["N" + N][name] = {
                "F_rate_anchor": row["trace"][0]["F_rate"],
                "I_rate_t001": row["t001"]["I_rate"],
                "O_rate_t001": row["t001"]["O_rate"],
                "F_rate_t001": row["t001"]["F_rate"],
                "first_sampled_F_rate_negative": row["first_sampled_negative_F_rate_time"],
                "first_sampled_leading_group_rate_positive": row["first_sampled_positive_leading_group_rate_time"],
                "leading_group_rate_t001": row["t001"]["leading_group_rate"],
                "leading_group_share_of_net_O_rate_t001": row["t001"]["leading_group_share_of_net_O_rate"],
                "top5_positive_outside_rate_share_of_net_O_rate_t001": row["t001"]["top5_positive_outside_rate_share_of_net_O_rate"],
            }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    tmp = args.output.with_name(args.output.name + ".tmp")
    tmp.write_text(json.dumps(stored, indent=2) + "\n", encoding="utf-8")
    tmp.replace(args.output)
    print("SAVED", args.output, flush=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--n10-n11", type=Path, required=True)
    p.add_argument("--n12", type=Path, required=True)
    p.add_argument("--n13", type=Path, required=True)
    p.add_argument("--source", type=Path, required=True)
    p.add_argument("--margin-velocity", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    run(p.parse_args())


if __name__ == "__main__":
    main()
