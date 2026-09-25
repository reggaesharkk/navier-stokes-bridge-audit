"""WP12 energy-level coefficient falsifier for the WP11 L2-L3 target.

Defines the tautological required coefficient

    b_req = max(N_high - theta*nu*Y, 0)/X

and compares it with the unique energy/enstrophy monomial having the required
amplitude and Navier-Stokes scaling, sqrt(G).

The audit is diagnostic. b_req is circular and cannot be used as a proof
coefficient.
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np

from adversarial_cutoff_gate import SCENARIOS, make_initial
from evolve_galerkin import System
from phase_cascade_trajectory import NU
from wp11_scaling_audit import dilated_system, discrepancy

HERE = Path(__file__).resolve().parent


def observables(system, a, s, K, theta):
    weights = system.square.astype(float)**s
    X = float(np.sum(weights[:, None] * abs(a)**2))
    Y = float(np.sum((weights*system.square)[:, None] * abs(a)**2))
    G = float(np.sum(system.square[:, None] * abs(a)**2))

    high = system.square[system.left] > K*K
    out, left, right = (x[high] for x in
                        (system.out, system.left, system.right))
    qdot = np.einsum('ij,ij->i', system.qwaves[high], a[left])
    z = -1j * weights[out] * qdot * np.einsum(
        'ij,ij->i', np.conj(a[out]), a[right])
    high_transfer = float(np.real(np.sum(z)))

    residual = max(high_transfer - theta*system.nu*Y, 0.0)
    b_req = residual/X if X > 0 else 0.0
    sqrt_G = math.sqrt(G)
    ratio = b_req/sqrt_G if sqrt_G > 0 else 0.0

    return dict(
        X=X,
        Y=Y,
        G=G,
        high_transfer=high_transfer,
        reserve_fraction=theta,
        reserve=theta*system.nu*Y,
        positive_residual=residual,
        b_required=b_req,
        sqrt_G=sqrt_G,
        Q_energy=ratio,
    )


def evolve_trace(N, scenario, amplitude_multiplier, s, K, theta, dt, t_end):
    system = System(N=N, nu=NU)
    a = amplitude_multiplier*make_initial(
        system, *SCENARIOS[scenario]
    )
    steps = round(t_end/dt)
    rows = []

    for step in range(steps+1):
        row = observables(system, a, s, K, theta)
        row["time"] = step*dt
        rows.append(row)
        if step < steps:
            a = system.rk4(a, dt)

    b_integral = float(np.trapezoid(
        [r["b_required"] for r in rows], dx=dt
    ))
    sqrt_G_integral = float(np.trapezoid(
        [r["sqrt_G"] for r in rows], dx=dt
    ))

    return dict(
        cutoff=N,
        scenario=scenario,
        amplitude_multiplier=amplitude_multiplier,
        K=K,
        theta=theta,
        s=s,
        dt=dt,
        t_end=t_end,
        integral_b_required=b_integral,
        integral_sqrt_G=sqrt_G_integral,
        max_Q_energy=max(r["Q_energy"] for r in rows),
        rows=rows,
    )


def dilation_check(N, scenario, amplitude_multiplier, s, K, theta, lam=2):
    base = System(N=N, nu=NU)
    scaled = dilated_system(base, lam)
    a = amplitude_multiplier*make_initial(base, *SCENARIOS[scenario])
    b = lam*a.copy()

    x = observables(base, a, s, K, theta)
    y = observables(scaled, b, s, lam*K, theta)

    errors = dict(
        X=discrepancy(y["X"], lam**(2*s+2)*x["X"]),
        Y=discrepancy(y["Y"], lam**(2*s+4)*x["Y"]),
        G=discrepancy(y["G"], lam**4*x["G"]),
        high_transfer=discrepancy(
            y["high_transfer"], lam**(2*s+4)*x["high_transfer"]
        ),
        b_required=discrepancy(
            y["b_required"], lam**2*x["b_required"]
        ),
        sqrt_G=discrepancy(
            y["sqrt_G"], lam**2*x["sqrt_G"]
        ),
        Q_energy=discrepancy(y["Q_energy"], x["Q_energy"]),
    )
    return dict(
        N=N,
        scaled_N=lam*N,
        K=K,
        scaled_K=lam*K,
        lambda_factor=lam,
        base=x,
        scaled=y,
        relative_errors=errors,
        maximum_error=max(errors.values()),
        representation="invariant image sublattice",
    )


def run(
    cutoffs=(4,7),
    scenarios=("reference","combined_double_quarter_high"),
    amplitudes=(0.5,1.0,2.0,4.0),
    thetas=(0.25,0.5,0.75),
    s=2.0,
    K=2,
    dt=0.0005,
    t_end=0.005,
):
    traces = []
    for scenario in scenarios:
        for N in cutoffs:
            for amplitude in amplitudes:
                for theta in thetas:
                    traces.append(evolve_trace(
                        N, scenario, amplitude, s, K, theta, dt, t_end
                    ))

    dilation = []
    for scenario in scenarios:
        for N in cutoffs:
            for theta in thetas:
                dilation.append(dilation_check(
                    N, scenario, 1.0, s, K, theta, lam=2
                ))

    max_scaling_error = max(x["maximum_error"] for x in dilation)
    if max_scaling_error > 2e-11:
        raise AssertionError(
            f"Scaling error too large: {max_scaling_error}"
        )

    return dict(
        definition=(
            "b_required=max(N_high-theta*nu*Y,0)/X; "
            "Q_energy=b_required/sqrt(G)"
        ),
        warning=(
            "b_required is tautological/circular and cannot prove L2-L3. "
            "Finite Q_energy values can falsify proposed constants only on "
            "the tested families; they cannot establish a uniform theorem."
        ),
        s=s,
        K=K,
        nu=NU,
        cutoffs=list(cutoffs),
        scenarios=list(scenarios),
        amplitudes=list(amplitudes),
        reserve_fractions=list(thetas),
        interval=[0.0,t_end],
        max_scaling_error=max_scaling_error,
        dilation_checks=dilation,
        traces=traces,
    )


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output",
        type=Path,
        default=HERE/"wp12_energy_coefficient_results.json",
    )
    p.add_argument("--t-end", type=float, default=0.005)
    args = p.parse_args()
    result = run(t_end=args.t_end)
    args.output.write_text(
        json.dumps(result, indent=2)+"\n", encoding="utf-8"
    )
    print("Wrote", args.output)
    print("max_scaling_error=", result["max_scaling_error"])
    for row in sorted(
        result["traces"],
        key=lambda x:x["max_Q_energy"],
        reverse=True
    )[:12]:
        print(
            row["scenario"],
            "N=", row["cutoff"],
            "A=", row["amplitude_multiplier"],
            "theta=", row["theta"],
            "max_Q=", row["max_Q_energy"],
            "int_b=", row["integral_b_required"],
        )
