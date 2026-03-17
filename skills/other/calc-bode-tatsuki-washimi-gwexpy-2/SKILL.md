---
name: calc_bode
description: python-controlを使用して、メカニカルシステムの状態空間モデルから伝達関数（Bode Plot）を計算・表示する
---

# `calc_bode`

This skill builds a state-space model from a mechanical system defined by mass (M), stiffness (K), and damping (C) matrices, and generates a frequency response (Bode Plot) using the `python-control` library.

## Workflow

1.  **System Matrix Acquisition**:
    - Extract the $M$ and $K$ matrices from a physical model or linearization tool.
    - Define the damping matrix $C$ as needed (typically proportional to stiffness or using modal damping).

2.  **State-Space Construction**:
    - Define the state vector as $x = [q, v]^T$, where $q$ is displacement and $v$ is velocity.
    - Transform the system's equation of motion $M \ddot{q} + C \dot{q} + K q = F u$ into the standard state-space form $\dot{x} = Ax + Bu$:
    - $A = \begin{bmatrix} 0 & I \\ -M^{-1}K & -M^{-1}C \end{bmatrix}$
    - $B = \begin{bmatrix} 0 \\ M^{-1}F \end{bmatrix}$

3.  **Application of `python-control`**:
    - Import the library: `import control as ct`.
    - Create the system object: `sys = ct.ss(A, B, C, D)`.

4.  **IO Selection (for MIMO systems)**:
    - Use `sys_siso = sys[output_idx, input_idx]` to select the desired input/output channel.

5.  **Plotting and Analysis**:
    - Generate the Bode plot: `ct.bode_plot(sys_siso, ...)`.
    - Utilize flags such as `Hz=True`, `dB=True`, and `deg=True`.
    - Check stability if necessary via `sys.poles()`.

## Precautions
- In systems including inverted pendulums, such as the KAGRA top stage, open-loop poles may exist in the unstable region before applying stabilization control.
- Ensure frequency ranges are specified in angular frequency (rad/s) such as `np.logspace(np.log10(start_hz * 2*np.pi), np.log10(end_hz * 2*np.pi), n_points)`, while specifying `Hz=True` in `bode_plot`.
