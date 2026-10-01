#!/usr/bin/env python3
"""Independent Fourier-ball recomputation of the M14 step-237 residual bound.

The verifier does not import the residual producer. It rebuilds the frozen
primal and adjoint Hermite fields from the saved arrays, evaluates the VJP
with a separately laid out carry-free convolution, and forms an Arb Bernstein
upper for the whole half-segment. This checks one residual segment only.
"""
from __future__ import annotations
import argparse, hashlib, json, math
from fractions import Fraction
from pathlib import Path
import numpy as np
from flint import acb, acb_poly, arb, ctx

M=14
STEP_DEFAULT=237
H=arb(1)/40000
HALF_H=arb(1)/80000
NU=arb(1)/10
EXPECTED_SEGMENTS={
 239:"d1b41363c88173594ec6c9e90453513cd3c8ed3e32c7037d2e73304d057a8c08",
 238:"c0bbf407df850b95e1a4b0daa3e1175962ce128e7e5f080d39127bd22b431fa6",
 237:"c2110c2f7a245a36534a24f7ab6983b74bf4a51ba8fb209a0ec92a8727eecfdc",
}
EXPECTED_ADJOINT_REPORT="981dc8d6286f5d989e73dec050ad406776c1320ead36596ac173de95d6a7edc8"
EXPECTED_ADJOINT_VALUES="00a230b47c66d3417b1fc259ead4e58ff46542753ddb7710c83a64dd4cd882ab"
EXPECTED_ADJOINT_RHS="8c838ac0e93d70c5d170925e0d27799b745f0adc3c7296a0335219b7359c783c"
EXPECTED_NODES="e0b0a36d8b308cccb5befb3abe45777ec0775cbc7e5a76fef0011eed0fd1f7f0"
EXPECTED_RHS="f3a55190e9cba625b7285e5ba3e09e68fa4027e7a8909d1ad80671c1ee1ef253"
FROZEN={
 "witness_sha256":"4789e27170f28279b3c6878f8874547b303d5cbd4a20848f3d5d8088bd10a624",
 "K36_sha256":"7da5fc6d39ee03140d42ba40c5158cc20b043de33e4cc7f3ea52b71b79143f47",
 "K36_sign_chart_sha256":"de2e7cf42373285f16a4d357422d7784afa98c997f90e6594c0102952bf6d3d1",
 "C500_portable_semantic_sha256":"1e9509cef054bf605d4a28af6580e383d021914f600a01b21cb1ebdf1086f71f",
}

def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()

def outward(x, places):
 mid,rad,exp=(int(v) for v in x.mid_rad_10exp())
 n=mid+rad; shift=exp+places
 if shift>=0: grid=n*10**shift; units=grid
 else:
  den=10**(-shift); grid=n; units=-((-n)//den)
 units+=1
 if shift>=0: above=units>grid
 else: above=units*den>grid
 if not above: raise ArithmeticError('decimal upper was not outward')
 sign='-' if units<0 else ''; digits=str(abs(units)).zfill(places+1)
 return sign+(digits[:-places]+'.'+digits[-places:] if places else digits)

def modes(cutoff):
 return [(x,y,z) for x in range(-cutoff,cutoff+1)
         for y in range(-cutoff,cutoff+1)
         for z in range(-cutoff,cutoff+1)
         if x*x+y*y+z*z<=cutoff*cutoff]

def squares(waves): return [sum(v*v for v in k) for k in waves]

def exact_complex(z):
 z=complex(z); rn,rd=z.real.as_integer_ratio(); imn,imd=z.imag.as_integer_ratio()
 return acb(arb(rn)/rd,arb(imn)/imd)

def decimal_complex(z):
 z=complex(z)
 return acb(str(float(z.real)),str(float(z.imag)))

def solenoidal(waves,array,importer):
 out=[[acb(0),acb(0),acb(0)] for _ in waves]
 index={k:i for i,k in enumerate(waves)}; sq=squares(waves)
 for i,k in enumerate(waves):
  neg=tuple(-v for v in k)
  if k<=neg: continue
  a=[importer(z) for z in array[i]]
  dot=sum((a[t]*k[t] for t in range(3)),acb(0))
  b=[a[t]-dot*k[t]/sq[i] for t in range(3)]
  out[i]=b; out[index[neg]]=[z.conjugate() for z in b]
 return out

def hermite(a,b,f,g,h):
 return [a,
  [[h*z for z in row] for row in f],
  [[3*(b[i][t]-a[i][t])-h*(2*f[i][t]+g[i][t]) for t in range(3)] for i in range(len(a))],
  [[2*(a[i][t]-b[i][t])+h*(f[i][t]+g[i][t]) for t in range(3)] for i in range(len(a))]]

def restrict_half(c,start):
 width=arb(1)/2
 return [[[sum((c[d][i][t]*math.comb(d,r)*start**(d-r)*width**r
                     for d in range(r,4)),acb(0)) for t in range(3)]
          for i in range(len(c[0]))] for r in range(4)]

def bernstein(c):
 degree=len(c)-1
 return [[[sum((c[d][i][t]*math.comb(j,d)/math.comb(degree,d)
                    for d in range(j+1)),acb(0)) for t in range(3)]
           for i in range(len(c[0]))] for j in range(degree+1)]

def l2_upper(rows):
 total=arb(0)
 for row in rows:
  for z in row: total+=z.abs_upper()**2
 return total.sqrt().upper()

def sup_l2(c):
 return max((l2_upper(b) for b in bernstein(c)),default=arb(0)).upper()

def strain_upper(waves,c):
 best=arb(0); invsqrt2=arb(1)/arb(2).sqrt()
 for control in bernstein(c):
  value=arb(0)
  for k,row in zip(waves,control):
   value+=arb(sum(v*v for v in k)).sqrt()*l2_upper([row])*invsqrt2
  best=best.max(value).upper()
 return best

def carry_free_vjp(waves, u, lam):
 """Build temporal polynomials using a distinct reversed-axis radix layout."""
 n=max(max(abs(v) for v in k) for k in waves); base=4*n+2; stride=base**3
 # z is the low-order digit here (the producer uses x).
 left=[k[2]+n+base*(k[1]+n)+base**2*(k[0]+n) for k in waves]
 right=[k[2]+2*n+base*(k[1]+2*n)+base**2*(k[0]+2*n) for k in waves]
 def pack(c,component,derivative=None):
  values={}
  for i,slot in enumerate(left):
   factor=acb(0,waves[i][derivative]) if derivative is not None else acb(1)
   for d in range(4):
    z=c[d][i][component]*factor
    if not z.is_zero(): values[slot+d*stride]=z
  p=acb_poly([])
  for exponent in sorted(values,reverse=True): p[exponent]=values[exponent]
  return p
 U=[pack(u,j) for j in range(3)]
 L=[pack(lam,j) for j in range(3)]
 out=[[[acb(0) for _ in range(3)] for _ in waves] for _ in range(7)]
 for target in range(3):
  product=acb_poly([0])
  for i in range(3):
   product+=L[i]*pack(u,i,target)-U[i]*pack(lam,target,i)
  for i,k in enumerate(waves):
   for d in range(7): out[d][i][target]=product[right[i]+d*stride]
 for d in range(7):
  for i,k in enumerate(waves):
   kk=sum(v*v for v in k)
   if kk==0: out[d][i]=[acb(0)]*3; continue
   dot=sum((out[d][i][t]*k[t] for t in range(3)),acb(0))
   out[d][i]=[out[d][i][t]-dot*k[t]/kk for t in range(3)]
 return out

def direct_vjp(waves,u,lam):
 """Small-system explicit pair sum used to audit the packed implementation."""
 idx={k:i for i,k in enumerate(waves)}; sq=squares(waves)
 out=[[[acb(0) for _ in range(3)] for _ in waves] for _ in range(7)]
 for oi,k in enumerate(waves):
  if sq[oi]==0: continue
  for pi,p in enumerate(waves):
   qi=idx.get(tuple(k[t]-p[t] for t in range(3)))
   if qi is None: continue
   q=waves[qi]
   for a in range(4):
    for b in range(4):
     dot=sum((lam[a][pi][t]*u[b][qi][t] for t in range(3)),acb(0))
     adv=sum((u[b][pi][t]*q[t] for t in range(3)),acb(0))
     for t in range(3): out[a+b][oi][t]+=acb(0,1)*(q[t]*dot-adv*lam[a][qi][t])
  for d in range(7):
   kd=sum((out[d][oi][t]*k[t] for t in range(3)),acb(0))
   out[d][oi]=[out[d][oi][t]-kd*k[t]/sq[oi] for t in range(3)]
 return out

def self_check():
 ctx.prec=192
 c=[[[acb(v),acb(0),acb(0)] for _ in modes(2)] for v in range(4)]
 # Make two smooth, reality-symmetric transverse polynomial fields.
 w=modes(2); rng=np.random.default_rng(20261001)
 def random_field():
  a=(rng.integers(-3,4,(len(w),3))+1j*rng.integers(-3,4,(len(w),3)))/8
  return solenoidal(w,a,exact_complex)
 u=[random_field() for _ in range(4)]; lam=[random_field() for _ in range(4)]
 packed=carry_free_vjp(w,u,lam); direct=direct_vjp(w,u,lam)
 for d in range(7):
  for i in range(len(w)):
   for t in range(3):
    diff=packed[d][i][t]-direct[d][i][t]
    if not diff.contains(0): raise ValueError(('small explicit convolution mismatch',d,i,t,str(diff)))
 print('PASS independent radix-layout VJP self-check')

def primal_radius(lower,nodes,rhs):
 meta=json.loads((lower/'metadata.json').read_text())
 if meta.get('N')!=M or meta.get('steps')!=120 or meta.get('h_exact_decimal')!='0.000025' or meta.get('initial_error_bound_decimal')!='0':
  raise ValueError('frozen lower-certificate metadata mismatch')
 if sha(lower/'nodes.npy')!=EXPECTED_NODES or sha(lower/'rhs.npy')!=EXPECTED_RHS: raise ValueError('lower arrays hash mismatch')
 e=arb(0); radii=[]
 for step in range(120):
  row=json.loads((lower/f'{step:03d}.json').read_text())
  digest=hashlib.sha256(b''.join(x.tobytes() for x in (nodes[step],nodes[step+1],rhs[step],rhs[step+1]))).hexdigest()
  if row.get('step')!=step or row.get('input_binary_sha256')!=digest: raise ValueError(('lower segment input mismatch',step))
  if step==0 and row.get('exact_rational_initial_field_sha256')!=FROZEN['witness_sha256']: raise ValueError('initial field witness mismatch')
  r=arb(row['residual_L2_upper_decimal']); g=arb(row['gradient_Fourier_l1_upper_decimal'])
  if not r>=0 or not g>=0: raise ValueError(('negative primal majorant',step))
  e=arb(outward((g*H).exp()*(e+H*r),12)); radii.append(e)
 return radii

def run(lower,adjoint,segment_path,output,step):
 ctx.prec=192
 if step not in EXPECTED_SEGMENTS: raise ValueError('this checker supports steps 237, 238, and 239 only')
 if sha(segment_path)!=EXPECTED_SEGMENTS[step]: raise ValueError(('segment record hash mismatch',step))
 seg=json.loads(segment_path.read_text())
 if seg.get('M')!=14 or seg.get('step')!=step or seg.get('frozen')!=FROZEN: raise ValueError('segment frozen identity mismatch')
 if seg.get('status')!='CONTINUOUS_SEGMENT_ENCLOSURE_ONLY' or seg.get('source_sha256')!='e1495d9e6e9ebcfa79f7440ca6abecf01a9d77f0bc64a200b8f68a2af1844f31': raise ValueError('segment producer identity mismatch')
 report=adjoint/'M14_arb_vjp_point.json'
 if sha(report)!=EXPECTED_ADJOINT_REPORT: raise ValueError('adjoint path report hash mismatch')
 rep=json.loads(report.read_text())
 if rep.get('status')!='PASS ARB VJP CROSSCHECK AND ADJOINT PATH EXPORT' or rep.get('frozen')!=FROZEN: raise ValueError('adjoint path report/frozen mismatch')
 rec=rep['adjoint_reconstruction']
 paths={k:adjoint/rec[k+'_file'] for k in ('values','rhs')}
 if sha(paths['values'])!=EXPECTED_ADJOINT_VALUES or sha(paths['rhs'])!=EXPECTED_ADJOINT_RHS: raise ValueError('adjoint arrays hash mismatch')
 nodes=np.load(lower/'nodes.npy',mmap_mode='r'); prhs=np.load(lower/'rhs.npy',mmap_mode='r')
 av=np.load(paths['values'],mmap_mode='r'); ar=np.load(paths['rhs'],mmap_mode='r')
 low=modes(14); high=modes(15); lowidx={k:i for i,k in enumerate(low)}; highidx={k:i for i,k in enumerate(high)}
 if nodes.shape!=(121,len(low),3) or prhs.shape!=nodes.shape or av.shape!=(241,len(high),3) or ar.shape!=av.shape: raise ValueError('frozen array shape mismatch')
 for name,path in (('nodes',lower/'nodes.npy'),('rhs',lower/'rhs.npy')):
  if sha(path)!=seg['inputs']['lower_'+name+'_sha256']: raise ValueError(('segment lower hash mismatch',name))
 if sha(report)!=seg['inputs']['adjoint_report_sha256'] or sha(paths['values'])!=seg['inputs']['adjoint_values_sha256'] or sha(paths['rhs'])!=seg['inputs']['adjoint_rhs_sha256']:
  raise ValueError('segment adjoint inputs mismatch')
 # Independent exact-dyadic and decimal-centre primal Hermite reconstructions.
 J=step//2
 bd=[solenoidal(low,nodes[x],exact_complex) for x in (J,J+1)]+[solenoidal(low,prhs[x],exact_complex) for x in (J,J+1)]
 dc=[solenoidal(low,nodes[x],decimal_complex) for x in (J,J+1)]+[solenoidal(low,prhs[x],decimal_complex) for x in (J,J+1)]
 up=hermite(bd[0],bd[1],bd[2],bd[3],H); ud=hermite(dc[0],dc[1],dc[2],dc[3],H)
 diff=[[[up[d][i][t]-ud[d][i][t] for t in range(3)] for i in range(len(low))] for d in range(4)]
 centre_gap=sup_l2(diff)
 radius=(primal_radius(lower,nodes,prhs)[J]+centre_gap).upper()
 # Restrict the primal polynomial to the second quarter-step half.
 uh=restrict_half(up,arb(step%2)/2)
 uh_high=[[[acb(0) for _ in range(3)] for _ in high] for _ in range(4)]
 for i,k in enumerate(low): uh_high[0][highidx[k]]=uh[0][i]
 for d in range(1,4):
  for i,k in enumerate(low): uh_high[d][highidx[k]]=uh[d][i]
 # Rebuild the saved M15 adjoint cubic from exact binary64 dyadics.
 adj_coeff=[solenoidal(high,arr,exact_complex) for arr in (av[step],av[step+1],ar[step],ar[step+1])]
 L=hermite(*adj_coeff,HALF_H)
 vjp=carry_free_vjp(high,uh_high,L)
 residual=[[[((d+1)*L[d+1][i][t]/HALF_H if d<3 else 0)
               -vjp[d][i][t]-(NU*squares(high)[i]*L[d][i][t] if d<4 else 0)
               for t in range(3)] for i in range(len(high))] for d in range(7)]
 nominal=sup_l2(residual); lsup=sup_l2(L)
 ksq=sum(squares(low)); count=len(low)
 uncertainty=(arb(ksq).sqrt()+arb(M+1)*arb(count).sqrt())*radius*lsup
 total=(nominal+uncertainty).upper()
 strain=(strain_upper(low,uh)+(arb(ksq)/2).sqrt()*radius).upper()
 corrected_log=(strain+arb('22.5')).upper()
 bounds=seg['bounds']
 archived_nominal=arb(bounds['nominal_residual_L2_upper'])
 archived_penalty=arb(bounds['primal_uncertainty_residual_penalty_upper'])
 archived_residual=arb(bounds['residual_L2_upper'])
 archived_adjoint=arb(bounds['adjoint_polynomial_L2_upper'])
 archived_strain=arb(bounds['logarithmic_norm_upper'])
 checks={
  'independent_nominal_residual_le_archived':bool(nominal<=archived_nominal),
  'independent_uncertainty_penalty_le_archived':bool(uncertainty<=archived_penalty),
  'independent_total_residual_le_archived':bool(total<=archived_residual),
  'independent_adjoint_polynomial_norm_le_archived':bool(lsup<=archived_adjoint),
  'independent_strain_le_archived_primal_strain':bool(strain<=archived_strain),
 }
 result={
  'schema':'wp19-v0.28-independent-residual-bernstein-check-v1',
  'status':f'INDEPENDENT_STEP_{step}_RECOMPUTATION_COMPLETE_ARCHIVE_COMPARISON_RECORDED',
  'M':14,'adjoint_cutoff':15,'step':step,'backward_order_index':239-step,'precision_bits':ctx.prec,
  'segment_sha256':sha(segment_path),'adjoint_report_sha256':sha(report),
  'adjoint_values_sha256':sha(paths['values']),'adjoint_rhs_sha256':sha(paths['rhs']),
  'lower_nodes_sha256':sha(lower/'nodes.npy'),'lower_rhs_sha256':sha(lower/'rhs.npy'),
  'mode_counts':{'M14':len(low),'M15':len(high)},'sum_squared_M14_wave_numbers':ksq,
  'bounds':{
   'independent_nominal_residual_L2_upper':outward(nominal,6),
   'independent_primal_uncertainty_residual_penalty_upper':outward(uncertainty,6),
   'independent_total_residual_L2_upper':outward(total,6),
   'independent_adjoint_polynomial_L2_upper':outward(lsup,6),
   'independent_primal_centre_gap_upper':outward(centre_gap,18),
   'independent_true_primal_radius_upper':outward(radius,15),
   'independent_primal_strain_upper':outward(strain,12),
   'corrected_backward_log_norm_upper':outward(corrected_log,12),
   'archived_residual_L2_upper':bounds['residual_L2_upper'],
   'archived_strain_only_upper':bounds['logarithmic_norm_upper'],
  },
  'component_checks':checks,
  'archive_comparison_differences':{
   'nominal_residual_upper_minus_archived':outward(nominal-archived_nominal,6),
   'uncertainty_penalty_upper_minus_archived':outward(uncertainty-archived_penalty,6),
   'total_residual_upper_minus_archived':outward(total-archived_residual,6),
   'adjoint_polynomial_norm_upper_minus_archived':outward(lsup-archived_adjoint,6),
   'primal_strain_upper_minus_archived':outward(strain-archived_strain,12),
  },
  'method':'exact dyadic projection; independent reversed-axis carry-free spatial encoding; degree-six residual Bernstein L2 hull; independent primal uncertainty penalty',
  'scope':{'checked':['frozen array/report identities','primal centre/radius reconstruction','saved M15 adjoint Hermite reconstruction','whole-half-segment VJP residual Bernstein L2 upper','reverse-diffusion corrected log norm'],
           'not_checked':['other 239 segments','full adjoint path error','dual quadrature','nonlinear remainder','normalizer','endpoint transfer','continuum regularity']}
 }
 output.parent.mkdir(parents=True,exist_ok=True); output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps(result,indent=2),flush=True)

def main():
 p=argparse.ArgumentParser(); p.add_argument('--self-check',action='store_true'); p.add_argument('--step',type=int,default=STEP_DEFAULT)
 p.add_argument('--lower-dir',type=Path); p.add_argument('--adjoint-dir',type=Path)
 p.add_argument('--segment',type=Path); p.add_argument('--output',type=Path)
 a=p.parse_args()
 if a.self_check: self_check(); return
 if any(v is None for v in (a.lower_dir,a.adjoint_dir,a.segment,a.output)): p.error('supply --lower-dir, --adjoint-dir, --segment, and --output')
 run(a.lower_dir,a.adjoint_dir,a.segment,a.output,a.step)

if __name__=='__main__': main()
