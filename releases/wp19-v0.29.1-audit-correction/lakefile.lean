import Lake
open Lake DSL

package wp19_v029_audit_correction

require mathlib from git "https://github.com/leanprover-community/mathlib4.git" @ "v4.35.0"

@[default_target]
lean_lib NavierStokesWP19Bridge where
  srcDir := "lean"
  roots := #[`NavierStokesWP19Bridge, `NavierStokesWP19BridgeCert]
