---
name: mfe-structure
description: "Linear algebra and higher-dimensional thinking. Vectors, matrices, transformations — the architecture of mathematical space."
user-invocable: false
allowed-tools: Read Grep Glob
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-26"
      triggers:
        intents:
          - "vector"
          - "matrix"
          - "linear"
          - "space"
          - "dimension"
          - "basis"
          - "eigenvalue"
          - "transformation"
          - "determinant"
        contexts:
          - "mathematical problem solving"
          - "math reasoning"
---

# Structure

## Summary

**Structure** (Part IV: Expanding)
Chapters: 11, 12, 13, 14
Plane Position: (-0.3, 0.5) radius 0.4
Primitives: 51

Linear algebra and higher-dimensional thinking. Vectors, matrices, transformations — the architecture of mathematical space.

**Key Concepts:** Vector Definition, Vector Space Axioms, Dot Product (Inner Product), Matrix Definition and Operations, Linear Transformation

## Key Primitives



**Vector Definition** (definition): A vector v in R^n is an ordered n-tuple v = (v_1, v_2, ..., v_n) where each v_i is a real number. Vectors represent both magnitude and direction in n-dimensional space.
  - I need to represent a quantity with both magnitude and direction
  - How do I work with points or directions in multiple dimensions
  - Describe a displacement or velocity in n-dimensional space

**Vector Space Axioms** (axiom): A vector space V over a field F is a set with two operations (addition, scalar multiplication) satisfying 8 axioms: closure under addition and scalar multiplication, commutativity and associativity of addition, existence of zero vector and additive inverses, and distributive laws connecting addition with scalar multiplication.
  - Is this set a vector space
  - Verify the axioms for a proposed vector space structure
  - What properties must a space have to support linear algebra

**Dot Product (Inner Product)** (definition): The dot product of u, v in R^n is u . v = sum_{i=1}^{n} u_i * v_i. Geometrically, u . v = ||u|| ||v|| cos(theta) where theta is the angle between u and v.
  - Find the angle between two vectors
  - Compute the projection of one vector onto another
  - Check if two vectors are perpendicular

**Matrix Definition and Operations** (definition): An m x n matrix A is a rectangular array of scalars with m rows and n columns: A = [a_{ij}] where 1 <= i <= m, 1 <= j <= n. Matrix addition is componentwise; scalar multiplication scales all entries.
  - Represent a linear system of equations in compact form
  - Store and manipulate tabular numerical data
  - Encode a linear transformation as a matrix

**Linear Transformation** (definition): A function T: V -> W between vector spaces is a linear transformation if T(u+v) = T(u)+T(v) and T(cv) = cT(v) for all u,v in V and scalars c. Equivalently, T(c_1*v_1 + c_2*v_2) = c_1*T(v_1) + c_2*T(v_2).
  - Define a function that preserves vector space structure
  - Represent a geometric transformation as a matrix
  - Map between different vector spaces while preserving linearity

**Eigenvalue and Eigenvector** (definition): A scalar lambda is an eigenvalue of a square matrix A if there exists a nonzero vector v such that Av = lambda*v. The vector v is the corresponding eigenvector. The set of all eigenvectors for lambda (plus 0) is the eigenspace E_lambda = ker(A - lambda*I).
  - Find the directions that a transformation merely scales
  - Analyze the long-term behavior of a dynamical system
  - Diagonalize a matrix for easier computation

**Gradient** (definition): The gradient of a scalar field f: R^n -> R is the vector of partial derivatives: grad(f) = nabla f = (df/dx_1, df/dx_2, ..., df/dx_n). It points in the direction of steepest ascent and its magnitude is the rate of maximum increase.
  - Find the direction of steepest increase of a function
  - Compute the rate of change in an arbitrary direction via directional derivative
  - Set up optimization conditions: critical points where nabla f = 0

**Analyticity (Holomorphic Function)** (definition): A complex function f is analytic (holomorphic) at z_0 if f'(z_0) = lim_{h->0} (f(z_0+h)-f(z_0))/h exists, where h approaches 0 through complex values. f is entire if analytic on all of C. Analytic implies infinitely differentiable and equals its Taylor series.
  - Determine if a complex function is differentiable in the complex sense
  - Identify functions that have power series representations
  - Apply the powerful theorems of complex analysis to a function

**Vector Addition and Scalar Multiplication** (definition): For vectors u, v in R^n and scalar c in R: (u+v)_i = u_i + v_i (componentwise addition) and (cv)_i = c * v_i (scalar multiplication). These operations satisfy closure, commutativity, associativity, and distributivity.
  - How do I add or scale vectors
  - Combine forces or velocities acting on an object
  - Compute a linear combination of vectors

**Vector Norm (Magnitude)** (definition): The Euclidean norm of v in R^n is ||v|| = sqrt(v . v) = sqrt(sum_{i=1}^{n} v_i^2). It measures the length (magnitude) of the vector. A unit vector has ||v|| = 1.
  - Find the length or magnitude of a vector
  - Normalize a vector to unit length
  - Compute distance between two points in R^n

## Composition Patterns

- Vector Definition + structure-vector-addition -> Vector arithmetic in R^n (sequential)
- Vector Addition and Scalar Multiplication + structure-vector-definition -> Complete vector arithmetic system (parallel)
- Vector Space Axioms + structure-linear-transformation -> Theory of linear maps between vector spaces (sequential)
- Dot Product (Inner Product) + structure-vector-norm -> Angle measurement between vectors: cos(theta) = (u.v)/(||u|| ||v||) (sequential)
- Cross Product + structure-dot-product -> Scalar triple product: u . (v x w) = volume of parallelepiped (sequential)
- Vector Norm (Magnitude) + structure-vector-definition -> Distance metric in R^n: d(u,v) = ||u-v|| (sequential)
- Orthogonality and Projection + structure-span-basis -> Gram-Schmidt orthogonalization: convert any basis to orthogonal basis (sequential)
- Linear Independence + structure-span-basis -> Dimension of a vector space: size of any basis (sequential)
- Span and Basis + structure-linear-transformation -> Matrix representation of a linear map with respect to chosen bases (sequential)
- Triangle Inequality for Vectors + structure-vector-norm -> Metric space structure on R^n with triangle inequality as key axiom (parallel)

## Cross-Domain Links

- **perception**: Compatible domain for composition and cross-referencing
- **change**: Compatible domain for composition and cross-referencing
- **reality**: Compatible domain for composition and cross-referencing
- **foundations**: Compatible domain for composition and cross-referencing
- **mapping**: Compatible domain for composition and cross-referencing
- **synthesis**: Compatible domain for composition and cross-referencing

## Activation Patterns

- vector
- matrix
- linear
- space
- dimension
- basis
- eigenvalue
- transformation
- determinant
