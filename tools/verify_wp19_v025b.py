#!/usr/bin/env python3
"""Audit a WP19 v0.25b signed-C500 N11-N18 aggregate ZIP (stdlib only).

This verifier is intentionally packaging-aware but fail-closed. GitHub Actions
upload-artifact may flatten a staged "final/" directory so SHA256SUMS.txt can
legitimately contain entries like "final/N14_signed_C500.json" while the ZIP
member is "N14_signed_C500.json". Only that exact prefix rewrite is accepted;
arbitrary basename fallback is not.

Usage:
    python tools/verify_wp19_v025b.py path/to/wp19-v0-25b-signed-c500-n11-n18.zip
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
import zipfile
from decimal import Decimal, getcontext
from pathlib import PurePosixPath

getcontext().prec=50


def walk(obj,path=""):
    if isinstance(obj,dict):
        for k,v in obj.items():
            yield from walk(v,f"{path}/{k}")
    elif isinstance(obj,list):
        for i,v in enumerate(obj):
            yield from walk(v,f"{path}[{i}]")
    else:
        yield path,obj


def as_dec(x):
    try:
        return Decimal(str(x))
    except Exception:
        return None


def normalized_member(manifest_name,names):
    """Resolve only known GitHub artifact staging normalization."""
    raw=manifest_name.strip().replace("\\","/")
    while raw.startswith("./"):
        raw=raw[2:]
    candidates=[raw]
    if raw.startswith("final/"):
        candidates.append(raw[len("final/"):])
    hits=[c for c in candidates if c in names]
    if len(hits)!=1:
        raise ValueError(
            f"manifest path {manifest_name!r} resolves to {hits}; "
            f"allowed candidates were {candidates}"
        )
    return hits[0]


def main(zpath):
    ok=True
    with zipfile.ZipFile(zpath) as z:
        names=z.namelist()
        names_set=set(names)
        print("files:",names)

        sums=[n for n in names if PurePosixPath(n).name.upper().startswith("SHA256SUMS")]
        if len(sums)!=1:
            print("  expected exactly one SHA256SUMS file; found",sums)
            ok=False
        else:
            sums_name=sums[0]
            manifest=z.read(sums_name).decode()
            seen=set()
            for line in manifest.splitlines():
                m=re.match(r"^([0-9a-fA-F]{64})\s+\*?(.+)$",line.strip())
                if not m:
                    continue
                want,fn=m.group(1).lower(),m.group(2).strip()
                # A manifest cannot meaningfully authenticate itself. If a
                # historical bundle contains a self-entry, report and skip it.
                try:
                    member=normalized_member(fn,names_set)
                except ValueError as exc:
                    print("  PATH ERROR",exc)
                    ok=False
                    continue
                if member==sums_name:
                    print("  [skip] manifest self-entry",fn,"->",member)
                    continue
                if member in seen:
                    print("  DUPLICATE resolved manifest member",member)
                    ok=False
                    continue
                seen.add(member)
                got=hashlib.sha256(z.read(member)).hexdigest()
                good=got==want
                print(f"  [{'ok ' if good else 'BAD'}] {fn} -> {member}")
                ok &= good

        summ_candidates=[n for n in names if "SUMMARY" in PurePosixPath(n).name.upper() and n.lower().endswith(".json")]
        if len(summ_candidates)!=1:
            print("  expected exactly one JSON SUMMARY; found",summ_candidates)
            return 1
        summ_name=summ_candidates[0]
        summ=json.loads(z.read(summ_name))
        print("\nsummary status:",summ.get("status"),"| retuned:",summ.get("C500_retuned"))
        rows={int(r["N"]):r for r in summ["rows"]}
        if set(rows)!=set(range(11,19)):
            print("  BAD summary N set:",sorted(rows))
            ok=False

        for N,r in sorted(rows.items()):
            G=as_dec(r["certified_G_upper_decimal"])
            nlo=as_dec(r["normalizer_true_lower_bound_decimal"])
            good=(
                r["status"]=="PASS"
                and r["K36_sign_locked_count"]==36
                and bool(r["certified_signed_numerator_negative"])
                and G is not None and G<0
                and nlo is not None and nlo>0
            )
            line=f"N={N:2d} G_upper={G:.6f} norm_lo={nlo:.3f}"
            num=r.get("true_signed_numerator_upper_decimal")
            if num is not None:
                num=as_dec(num)
                if num is None or num>=0:
                    good=False
                else:
                    implied=(num/G).sqrt()
                    good &= implied>=nlo
                    line += (
                        f" num={num:.4e} implied_norm={implied:.3f} "
                        f"(gap {implied-nlo:.3f}, rel {((implied-nlo)/nlo):.2e})"
                    )
            print(("  [ok ] " if good else "  [BAD] ")+line)
            ok &= good

        print("\nper-N file contents (relevant numeric fields):")
        found=set()
        for n in sorted(names):
            m=re.search(r"(?:^|/)N(\d+)_signed_C500\.json$",n)
            if not m:
                continue
            N=int(m.group(1)); found.add(N)
            data=json.loads(z.read(n))
            print(f"\n{n}: top-level keys = {list(data)[:12] if isinstance(data,dict) else type(data)}")
            hits=[
                (p,v) for p,v in walk(data)
                if re.search(r"normaliz|numerat|k36|sign_lock|certified_G|G_upper",p,re.I)
                and not isinstance(v,(dict,list))
            ]
            for p,v in hits[:25]:
                print(f"    {p} = {v}")
            if len(hits)>25:
                print(f"    ... {len(hits)-25} more")
            r=rows.get(N)
            if r:
                for p,v in walk(data):
                    if p.endswith("certified_G_upper_decimal") and as_dec(v)!=as_dec(r["certified_G_upper_decimal"]):
                        print("    MISMATCH G_upper vs summary:",v,r["certified_G_upper_decimal"])
                        ok=False
                    if p.endswith("normalizer_true_lower_bound_decimal") and as_dec(v)!=as_dec(r["normalizer_true_lower_bound_decimal"]):
                        print("    MISMATCH normalizer vs summary:",v)
                        ok=False
        if found!=set(range(11,19)):
            print("  BAD per-N file set:",sorted(found))
            ok=False

    print("\nOVERALL:","PASS" if ok else "CHECK FAILURES ABOVE")
    return 0 if ok else 1


if __name__=="__main__":
    if len(sys.argv)!=2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
