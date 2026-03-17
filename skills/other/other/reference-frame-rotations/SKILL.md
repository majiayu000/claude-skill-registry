---
name: reference-frame-rotations
description: ReferenceFrameRotations.jl for 3D rotation representations (DCM, Quaternion, Euler angles). Use when constructing rotation matrices, converting between rotation representations, composing rotations, or computing attitude kinematics.
---

# ReferenceFrameRotations.jl

3D rotation representation and conversion library. Repo: [JuliaSpace/ReferenceFrameRotations.jl](https://github.com/JuliaSpace/ReferenceFrameRotations.jl)

## Types

- **`DCM{T}`** -- 3x3 Direction Cosine Matrix (`SMatrix{3,3,T}`)
- **`Quaternion{T}`** -- Scalar-first: `q = q0 + q1·i + q2·j + q3·k`
- **`EulerAngles{T}`** -- Three angles `(a1, a2, a3)` with rotation sequence symbol
- **`EulerAngleAxis{T}`** -- Angle `a` and axis vector `v`

## Construction

```julia
D = angle_to_dcm(θ₁, θ₂, θ₃, :ZYX)          # Euler angles -> DCM
q = angle_to_quat(θ₁, θ₂, θ₃, :ZYX)          # Euler angles -> Quaternion
D = smallangle_to_dcm(δx, δy, δz)             # Small angle approximation
q = Quaternion(1.0, 0.0, 0.0, 0.0)            # Identity quaternion
D = DCM(I)                                     # Identity DCM
```

**12 rotation sequences:** `:XYX`, `:XYZ`, `:XZX`, `:XZY`, `:YXY`, `:YXZ`, `:YZX`, `:YZY`, `:ZXY`, `:ZXZ`, `:ZYX`, `:ZYZ`

## Conversions (bidirectional between all types)

```julia
q = dcm_to_quat(D)              D = quat_to_dcm(q)
ea = dcm_to_angle(D, :ZYX)      D = angle_to_dcm(ea)
aa = dcm_to_angleaxis(D)        D = angleaxis_to_dcm(aa)
ea = quat_to_angle(q, :ZYX)     q = angle_to_quat(ea)
```

## Composition

```julia
D3 = compose_rotation(D1, D2)        # Same type required
D3 = D2 ∘ D1                         # Mixed types OK (converts to left type)
q3 = q1 * q2                         # Hamilton product
```

## Kinematics

```julia
dq = dquat(q_ba, ω_ba_b)    # Quaternion time-derivative from angular velocity
dD = ddcm(D_ba, ω_ba_b)     # DCM time-derivative from angular velocity
```

## Utilities

```julia
inv_rotation(D)        # Inverse rotation (transpose for DCM)
orthonormalize(D)      # Gram-Schmidt re-orthonormalization
conj(q)                # Quaternion conjugate
norm(q)                # Quaternion norm
```

## Key Conventions
- Quaternion scalar-first convention: `(q0, q1, q2, q3)`
- All angles in radians
- All types immutable, backed by StaticArrays
- AD support via ForwardDiff/Zygote extension
