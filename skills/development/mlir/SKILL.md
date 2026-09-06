---
name: mlir
description: 'Use when defining an MLIR dialect with ODS, writing a lowering with ConversionPattern, running mlir-opt pipelines down to the LLVM dialect, or importing models via Torch-MLIR or IREE.'
---

# MLIR

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A user builds a domain-specific compiler IR, lowers high-level ops toward LLVM or GPU dialects, writes a progressive lowering pipeline, defines ops in TableGen, or connects a PyTorch or ONNX model to an MLIR-based compiler. |
| Authority | Reversible local: writes only the dialect, pass, and test files the user names inside the project, plus generated `.inc` files and scratch `.mlir` outputs in the build directory; rollback is version control and deleting the build directory. No remote mutation. |
| Side effect | `mlir-tblgen` generates op code, the dialect and passes are built, and `mlir-opt` runs the pipeline on test IR with the verifier on. |
| Done | Test IR parses, the pipeline leaves no illegal op, the output translates to LLVM IR when the target is the LLVM dialect, and every custom op round-trips through its assembly format. |

## Inputs

1. The IR level to work at (required): existing dialects only, or a custom dialect with named ops.
2. Source and target dialects of the lowering (required when lowering): for example `linalg` on tensors down to the `llvm` dialect.
3. Test IR (required): one `.mlir` input per pipeline stage.
4. Installed MLIR (gathered by the skill): `mlir-opt --version`. Grounded current stable is LLVM/MLIR 23.1.0; pass names and TableGen directives below are confirmed against it.

## Procedure

1. Read the IR by its four nouns. A module holds operations; an operation such as `arith.addi` or `memref.load` produces SSA values and may hold regions; a region holds blocks; a block holds an ordered list of operations and ends in a terminator. Block arguments replace PHI nodes. A `func.func` is an operation with one region. Done when: the input is described in these terms and its dialects are listed.
2. Pick the built-in dialects that fit the level: `arith` for scalar arithmetic, `func` for functions and calls, `memref` for buffers with shape and stride, `tensor` for value-semantic arrays, `affine` for affine loop nests and maps, `linalg` for structured operations such as `linalg.matmul`, `scf` for structured `for` and `if`, `cf` for unstructured branches, `gpu` for kernel launches, `llvm` for the final form. A loop over buffers reads as:

   ```mlir
   func.func @add(%a: memref<4xf32>, %b: memref<4xf32>, %c: memref<4xf32>) {
     %c0 = arith.constant 0 : index
     %c1 = arith.constant 1 : index
     %c4 = arith.constant 4 : index
     scf.for %i = %c0 to %c4 step %c1 {
       %av = memref.load %a[%i] : memref<4xf32>
       %bv = memref.load %b[%i] : memref<4xf32>
       %sum = arith.addf %av, %bv : f32
       memref.store %sum, %c[%i] : memref<4xf32>
     }
     return
   }
   ```

   Done when: `mlir-opt example.mlir` parses and prints the file unchanged.
3. Drive lowering with `mlir-opt`, one stage per flag, and read the output between stages:

   ```bash
   mlir-opt example.mlir -canonicalize
   mlir-opt affine.mlir --lower-affine
   mlir-opt matmul.mlir --one-shot-bufferize="bufferize-function-boundaries" --convert-linalg-to-loops -o loops.mlir
   mlir-opt loops.mlir --convert-scf-to-cf --convert-arith-to-llvm --finalize-memref-to-llvm \
     --convert-cf-to-llvm --convert-func-to-llvm --reconcile-unrealized-casts -o llvm.mlir
   mlir-translate --mlir-to-llvmir llvm.mlir -o out.ll
   ```

   The path from a tensor-level `linalg.matmul` is: bufferize (tensors to memrefs), lower `linalg` to `scf` or `affine` loops, lower structured control flow to `cf`, then convert each remaining dialect to `llvm`, and finish with `--reconcile-unrealized-casts`. `--convert-to-llvm` runs the dialect-provided conversions in one step when every dialect in the input implements the interface. Done when: `mlir-translate --mlir-to-llvmir` emits a `define` for each function.
4. Define custom ops in ODS (TableGen). Include the side-effect interface for `Pure`, and either constrain operand types or make the assembly format name every type; with `AnyType` operands, `type($result)` alone cannot be parsed unless a trait ties the types together:

   ```tablegen
   include "mlir/IR/OpBase.td"
   include "mlir/Interfaces/SideEffectInterfaces.td"

   def My_Dialect : Dialect {
     let name = "my";
     let cppNamespace = "::my";
   }

   class My_Op<string mnemonic, list<Trait> traits = []> : Op<My_Dialect, mnemonic, traits>;

   def AddOp : My_Op<"add", [Pure, AllTypesMatch<["lhs", "rhs", "result"]>]> {
     let summary = "Add two values";
     let arguments = (ins AnyType:$lhs, AnyType:$rhs);
     let results = (outs AnyType:$result);
     let assemblyFormat = "$lhs `,` $rhs attr-dict `:` type($result)";
   }
   ```

   ```bash
   mlir-tblgen -gen-dialect-decls MyOps.td -I $(llvm-config --includedir) -o MyDialect.h.inc
   mlir-tblgen -gen-dialect-defs  MyOps.td -I $(llvm-config --includedir) -o MyDialect.cpp.inc
   mlir-tblgen -gen-op-decls      MyOps.td -I $(llvm-config --includedir) -o MyOps.h.inc
   mlir-tblgen -gen-op-defs       MyOps.td -I $(llvm-config --includedir) -o MyOps.cpp.inc
   ```

   Done when: all four generators run without a diagnostic.
5. Register the ops in the dialect's C++ initialization and include the generated definitions once:

   ```cpp
   #include "mlir/IR/DialectImplementation.h"
   #include "MyDialect.h"

   #define GET_OP_CLASSES
   #include "MyOps.cpp.inc"

   void my::MyDialect::initialize() {
     addOperations<
   #define GET_OP_LIST
   #include "MyOps.cpp.inc"
     >();
   }
   ```

   Every tool that parses the dialect must register it (`registry.insert<my::MyDialect>()`); an unregistered dialect fails at parse with "Dialect not found". Done when: `mlir-opt` built with the dialect parses a `my.add` op and prints it back.
6. Lower custom ops with the dialect conversion framework. A pattern rewrites one op; the target marks the source dialect illegal and the destination legal; partial conversion tolerates unrelated ops, full conversion fails on any illegal op left:

   ```cpp
   #include "mlir/Transforms/DialectConversion.h"

   struct AddOpLowering : mlir::OpConversionPattern<my::AddOp> {
     using OpConversionPattern::OpConversionPattern;
     mlir::LogicalResult matchAndRewrite(my::AddOp op, OpAdaptor adaptor,
                                         mlir::ConversionPatternRewriter &rewriter) const override {
       rewriter.replaceOpWithNewOp<mlir::arith::AddIOp>(op, adaptor.getLhs(), adaptor.getRhs());
       return mlir::success();
     }
   };

   void MyLoweringPass::runOnOperation() {
     mlir::ConversionTarget target(getContext());
     target.addIllegalDialect<my::MyDialect>();
     target.addLegalDialect<mlir::arith::ArithDialect>();
     mlir::RewritePatternSet patterns(&getContext());
     patterns.add<AddOpLowering>(&getContext());
     if (mlir::failed(mlir::applyPartialConversion(getOperation(), target, std::move(patterns))))
       signalPassFailure();
   }
   ```

   Use the adaptor's typed accessors for operands; they carry the already-converted values, while `op.getLhs()` still holds the old ones. Done when: the pass leaves no `my.` op in the output of the test input.
7. For ML front ends, import the model and hand the MLIR to the compiler. Torch-MLIR turns PyTorch or ONNX graphs into the `torch` dialect and lowers to `linalg`; IREE compiles MLIR to a deployable module and runs it. Use each project's current CLI as documented in its own repository; their command names and flags change between releases and are not pinned here. Done when: the imported module parses with the project's `mlir-opt` build and the lowering from step 3 applies.

## Failure and recovery

| Failure class | Behavior |
|---|---|
| `Dialect not found` at parse | The dialect is not registered in the tool. Register it in the tool's dialect registry or in the pass's `getDependentDialects`. |
| `mlir-tblgen` include error | The `-I` path does not reach `mlir/IR/OpBase.td`. Pass `$(llvm-config --includedir)`. |
| Type not buildable in assembly format | An `AnyType` operand has no type directive. Add a type-matching trait or name each `type($operand)` in the format. |
| Illegal ops remain after lowering | A pattern is missing. Run with `--mlir-print-ir-after-failure` to see the op left; add the pattern or mark the op legal. |
| `mlir-opt` crashes | Invalid IR between passes. Run with `--verify-each` (on by default) and `--mlir-print-ir-after-all` to find the pass that produced it. |
| `cf` ops rejected before LLVM translation | `--convert-cf-to-llvm` is missing. Add it after `--convert-scf-to-cf`. |

No partial result is claimed complete. If a step cannot finish, the report states which steps passed and which are blocked.

## Output

An MLIR delivery containing:
1. Files written: `.td`, dialect and pass sources, tests, and the generated `.inc` files.
2. Pipeline: the exact `mlir-opt` flag sequence and the per-stage output files.
3. Verification: parse round-trip of custom ops, absence of illegal ops after lowering, and the `mlir-translate` result.
4. Open items: any op left at a higher level with the reason.
