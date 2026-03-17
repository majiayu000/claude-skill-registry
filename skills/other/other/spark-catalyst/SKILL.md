---
name: Apache Spark Catalyst API
description: Expert guidance for working with the Apache Spark Catalyst query optimisation framework. Use this skill when working with Spark SQL internals, creating custom expressions, implementing query optimisations, working with logical/physical plans, or extending Catalyst. Trigger keywords include "catalyst", "spark sql", "expression", "logical plan", "physical plan", "tree node", "query optimisation", "rule executor", "analyzer", "optimizer", "code generation".
---

You are an expert in the Apache Spark Catalyst query optimisation framework. This skill provides comprehensive guidance on using the Catalyst API for query processing, optimisation, and code generation.

## Overview of Catalyst

Apache Spark Catalyst is a query optimisation framework that powers Spark SQL and DataFrames. It provides:

- **Extensible query optimiser** based on functional programming constructs
- **Tree-based representation** of query plans and expressions
- **Rule-based transformations** for query optimisation
- **Code generation** for high-performance query execution
- **Cost-based optimisation** for join reordering and other decisions

## Core Architecture

### Module Structure

The Catalyst module is located at `sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/` and contains:

```
catalyst/
├── analysis/           # Query analysis and resolution
├── catalog/           # Catalog management and metadata
├── expressions/       # Expression definitions and evaluation
├── optimizer/         # Query optimisation rules
├── parser/            # SQL parsing
├── planning/          # Query planning strategies
├── plans/             # Query plan representations
│   ├── logical/       # Logical plan operators
│   └── physical/      # Physical plan operators
├── rules/             # Rule execution framework
├── trees/             # Tree node infrastructure
├── types/             # Data type utilities
└── util/              # Utility classes
```

## Fundamental Concepts

### 1. TreeNode

`TreeNode` is the base class for all tree structures in Catalyst, including expressions and query plans.

#### Key Concepts

```scala
abstract class TreeNode[BaseType <: TreeNode[BaseType]] extends Product {
  // Children of this node.
  def children: Seq[BaseType]

  // Transform this tree by applying a function to all nodes.
  def transform(rule: PartialFunction[BaseType, BaseType]): BaseType

  // Transform all nodes bottom-up.
  def transformDown(rule: PartialFunction[BaseType, BaseType]): BaseType

  // Transform all nodes top-down.
  def transformUp(rule: PartialFunction[BaseType, BaseType]): BaseType

  // Fast equality check.
  def fastEquals(other: TreeNode[_]): Boolean

  // Tree pattern matching for efficient traversal.
  def treePatternBits: BitSet
}
```

#### Tree Transformation Patterns

**Bottom-up transformation:**

```scala
plan.transformUp {
  case Filter(condition, child) if isAlwaysTrue(condition) =>
    child
}
```

**Top-down transformation:**

```scala
plan.transformDown {
  case Project(projectList, child) =>
    // Transform project first, then children
    optimiseProject(projectList, child)
}
```

**Collect nodes matching a pattern:**

```scala
val filters = plan.collect {
  case f @ Filter(_, _) => f
}
```

### 2. Expression

`Expression` is the base class for all expression trees in Catalyst.

#### Expression Hierarchy

- **LeafExpression**: No children (e.g., `Literal`, `AttributeReference`)
- **UnaryExpression**: One child (e.g., `Cast`, `Not`, `IsNull`)
- **BinaryExpression**: Two children (e.g., `Add`, `EqualTo`, `And`)
- **TernaryExpression**: Three children (e.g., `If`, `Substring`)
- **QuaternaryExpression**: Four children

#### Key Properties

```scala
abstract class Expression extends TreeNode[Expression] {
  // Can this expression be evaluated at query planning time?
  def foldable: Boolean

  // Does this expression always return the same result for fixed inputs?
  def deterministic: Boolean

  // Can this expression evaluate to null?
  def nullable: Boolean

  // Data type of the expression result.
  def dataType: DataType

  // Evaluate this expression given an input row.
  def eval(input: InternalRow): Any

  // Generate code for this expression.
  def doGenCode(ctx: CodegenContext, ev: ExprCode): ExprCode

  // Attributes referenced by this expression.
  def references: AttributeSet
}
```

#### Common Expression Types

**Literal values:**

```scala
Literal(42)                    // Integer literal
Literal("hello")               // String literal
Literal(null, StringType)      // Null literal
```

**Attribute references:**

```scala
AttributeReference("name", StringType, nullable = true)()
AttributeReference("age", IntegerType, nullable = false)()
```

**Predicates:**

```scala
EqualTo(left, right)           // left = right
GreaterThan(left, right)       // left > right
LessThanOrEqual(left, right)   // left <= right
And(left, right)               // left AND right
Or(left, right)                // left OR right
Not(child)                     // NOT child
```

**Arithmetic:**

```scala
Add(left, right)               // left + right
Subtract(left, right)          // left - right
Multiply(left, right)          // left * right
Divide(left, right)            // left / right
```

**String operations:**

```scala
Substring(str, pos, len)       // substring(str, pos, len)
Upper(child)                   // upper(child)
Lower(child)                   // lower(child)
Concat(children)               // concat(child1, child2, ...)
```

**Type conversion:**

```scala
Cast(child, targetType)        // cast(child as targetType)
```

### 3. QueryPlan

`QueryPlan` is the base class for both logical and physical query plans.

#### Key Properties

```scala
abstract class QueryPlan[PlanType <: QueryPlan[PlanType]]
  extends TreeNode[PlanType] {

  // Output schema of this plan node.
  def output: Seq[Attribute]

  // Set of output attributes.
  def outputSet: AttributeSet

  // Set of attributes from all children.
  def inputSet: AttributeSet

  // Attributes produced by this node.
  def producedAttributes: AttributeSet

  // Attributes referenced by expressions.
  def references: AttributeSet

  // Attributes referenced but not provided by children.
  def missingInput: AttributeSet

  // All expressions in this plan node.
  def expressions: Seq[Expression]

  // Transform expressions in this plan.
  def transformExpressions(rule: PartialFunction[Expression, Expression]): PlanType
}
```

### 4. LogicalPlan

Logical plans represent query semantics without execution strategy.

#### Common Logical Operators

**Data sources:**

```scala
// Read from a relation.
LogicalRelation(relation, output, catalogTable)

// Local in-memory data.
LocalRelation(output, data)

// Empty relation.
EmptyRelation(output)
```

**Projections and filters:**

```scala
// Project specific columns.
Project(projectList: Seq[NamedExpression], child: LogicalPlan)

// Filter rows.
Filter(condition: Expression, child: LogicalPlan)

// Select distinct rows.
Distinct(child: LogicalPlan)
```

**Aggregations:**

```scala
// Group by and aggregate.
Aggregate(
  groupingExpressions: Seq[Expression],
  aggregateExpressions: Seq[NamedExpression],
  child: LogicalPlan
)
```

**Joins:**

```scala
// Join two relations.
Join(
  left: LogicalPlan,
  right: LogicalPlan,
  joinType: JoinType,
  condition: Option[Expression],
  hint: JoinHint
)
```

**Sorting:**

```scala
// Sort rows.
Sort(
  order: Seq[SortOrder],
  global: Boolean,
  child: LogicalPlan
)
```

**Limits:**

```scala
// Limit number of rows.
Limit(limitExpr: Expression, child: LogicalPlan)
```

**Set operations:**

```scala
// Union of two relations.
Union(children: Seq[LogicalPlan])

// Intersection.
Intersect(left: LogicalPlan, right: LogicalPlan, isAll: Boolean)

// Difference.
Except(left: LogicalPlan, right: LogicalPlan, isAll: Boolean)
```

### 5. InternalRow

`InternalRow` is the internal representation of a row in Catalyst.

#### Key Methods

```scala
abstract class InternalRow extends SpecializedGetters {
  // Number of fields in this row.
  def numFields: Int

  // Check if field at ordinal is null.
  def isNullAt(ordinal: Int): Boolean

  // Get value at ordinal.
  def get(ordinal: Int, dataType: DataType): Any

  // Specialised getters for primitive types.
  def getBoolean(ordinal: Int): Boolean
  def getByte(ordinal: Int): Byte
  def getShort(ordinal: Int): Short
  def getInt(ordinal: Int): Int
  def getLong(ordinal: Int): Long
  def getFloat(ordinal: Int): Float
  def getDouble(ordinal: Int): Double
  def getDecimal(ordinal: Int, precision: Int, scale: Int): Decimal
  def getUTF8String(ordinal: Int): UTF8String

  // Update value at ordinal.
  def update(ordinal: Int, value: Any): Unit

  // Set field to null.
  def setNullAt(ordinal: Int): Unit

  // Create a copy of this row.
  def copy(): InternalRow

  // Convert to Scala sequence.
  def toSeq(schema: StructType): Seq[Any]
}
```

## Rule-Based Transformation Framework

### 6. Rule and RuleExecutor

Rules define tree transformations, and RuleExecutor applies them in batches.

#### Defining Rules

```scala
// Basic rule.
object MyOptimisationRule extends Rule[LogicalPlan] {
  def apply(plan: LogicalPlan): LogicalPlan = plan.transformUp {
    case Filter(condition, child) if isAlwaysTrue(condition) =>
      child
  }
}

// Configurable rule.
case class MyParameterisedRule(conf: SQLConf) extends Rule[LogicalPlan] {
  def apply(plan: LogicalPlan): LogicalPlan = {
    if (conf.myFeatureEnabled) {
      optimisePlan(plan)
    } else {
      plan
    }
  }
}
```

#### Rule Execution Strategies

```scala
abstract class RuleExecutor[TreeType <: TreeNode[_]] {
  // Define batches of rules to execute.
  protected def batches: Seq[Batch]

  // Execute all batches on the plan.
  def execute(plan: TreeType): TreeType
}

// Batch execution strategies.
abstract class Strategy
case class Once extends Strategy
case class FixedPoint(maxIterations: Int) extends Strategy
```

#### Example RuleExecutor

```scala
object MyOptimiser extends RuleExecutor[LogicalPlan] {
  val batches = Seq(
    Batch("Normalisation", Once,
      EliminateSubqueryAliases,
      RemoveRedundantAliases
    ),
    Batch("Operator Optimisation", FixedPoint(100),
      PushDownPredicate,
      ConstantFolding,
      ColumnPruning
    ),
    Batch("Join Reordering", Once,
      CostBasedJoinReorder
    )
  )
}
```

### 7. Analyzer

The Analyzer resolves unresolved logical plans by binding attributes, functions, and tables.

#### Key Analysis Rules

- **ResolveReferences**: Bind attribute references to their sources
- **ResolveRelations**: Bind table references to catalog entries
- **ResolveFunctions**: Bind function calls to function implementations
- **TypeCoercion**: Insert implicit type casts
- **ResolveSubquery**: Analyse subquery expressions
- **CheckAnalysis**: Verify the plan is valid

#### Example Usage

```scala
val analyzer = new Analyzer(catalogManager)
val analysedPlan = analyzer.execute(unresolvedPlan)
```

### 8. Optimizer

The Optimizer transforms logical plans to improve query performance.

#### Key Optimisation Rules

**Predicate pushdown:**

```scala
// Push filters below projections.
PushDownPredicate

// Push filters into join conditions.
PushPredicateThroughJoin

// Push filters to data sources.
PushDownPredicates
```

**Projection pushdown:**

```scala
// Eliminate unnecessary columns.
ColumnPruning

// Combine adjacent projections.
CollapseProject
```

**Constant folding:**

```scala
// Evaluate constant expressions.
ConstantFolding

// Simplify expressions.
SimplifyConditionals
SimplifyCasts
```

**Join optimisation:**

```scala
// Reorder joins for better performance.
CostBasedJoinReorder

// Eliminate redundant joins.
EliminateOuterJoin
```

**Subquery optimisation:**

```scala
// Decorrelate correlated subqueries.
DecorrelateInnerQuery

// Merge scalar subqueries.
MergeScalarSubqueries
```

## Code Generation

### 9. CodeGen Framework

Catalyst generates optimised Java bytecode for query execution.

#### Key Components

**CodegenContext:**

Manages code generation state including variable declarations, functions, and class structure.

**ExprCode:**

Represents generated code for an expression evaluation.

```scala
case class ExprCode(
  code: Block,              // Generated code block
  isNull: ExprValue,        // Variable for null check
  value: ExprValue          // Variable for result value
)
```

#### Expression Code Generation

```scala
trait CodegenFallback extends Expression {
  // Fallback to interpreted evaluation.
  protected def doGenCode(ctx: CodegenContext, ev: ExprCode): ExprCode = {
    ctx.references += this
    val objectTerm = ctx.addReferenceObj("expression", this)
    ExprCode(
      code = code"""
        boolean ${ev.isNull} = true;
        ${CodeGenerator.javaType(dataType)} ${ev.value} =
          ${CodeGenerator.defaultValue(dataType)};
        Object result = $objectTerm.eval(${ctx.INPUT_ROW});
        if (result != null) {
          ${ev.isNull} = false;
          ${ev.value} = (${CodeGenerator.boxedType(dataType)}) result;
        }
      """,
      isNull = ev.isNull,
      value = ev.value
    )
  }
}
```

#### Projection Generation

```scala
// Generate unsafe projection from expressions.
val projection = GenerateUnsafeProjection.generate(expressions)
val result = projection(inputRow)

// Generate mutable projection.
val mutableProjection = GenerateMutableProjection.generate(expressions)
val outputRow = mutableProjection(inputRow)

// Generate safe projection.
val safeProjection = GenerateSafeProjection.generate(expressions)
```

#### Predicate Generation

```scala
// Generate predicate for filter condition.
val predicate = GeneratePredicate.generate(condition)
val passes = predicate.eval(row)
```

#### Ordering Generation

```scala
// Generate row comparator.
val ordering = GenerateOrdering.generate(sortOrders)
val compareResult = ordering.compare(row1, row2)
```

## Working with Data Types

### 10. Catalyst Type System

#### Primitive Types

```scala
BooleanType
ByteType
ShortType
IntegerType
LongType
FloatType
DoubleType
StringType
BinaryType
DateType
TimestampType
TimestampNTZType
```

#### Complex Types

```scala
// Array type.
ArrayType(elementType: DataType, containsNull: Boolean)

// Map type.
MapType(keyType: DataType, valueType: DataType, valueContainsNull: Boolean)

// Struct type.
StructType(fields: Seq[StructField])

// Struct field.
StructField(name: String, dataType: DataType, nullable: Boolean, metadata: Metadata)
```

#### Decimal Types

```scala
DecimalType(precision: Int, scale: Int)
DecimalType.SYSTEM_DEFAULT  // Decimal(38, 18)
```

## Common Patterns and Best Practices

### Pattern 1: Creating Custom Expressions

```scala
case class MyCustomFunction(child: Expression) extends UnaryExpression {
  // Define output type.
  override def dataType: DataType = StringType

  // Can the result be null?
  override def nullable: Boolean = child.nullable

  // Evaluate the expression.
  override def eval(input: InternalRow): Any = {
    val value = child.eval(input)
    if (value == null) {
      null
    } else {
      // Custom logic here.
      UTF8String.fromString(value.toString.toUpperCase)
    }
  }

  // Generate code for this expression.
  override protected def doGenCode(
      ctx: CodegenContext,
      ev: ExprCode): ExprCode = {
    val childGen = child.genCode(ctx)
    ev.copy(code = code"""
      ${childGen.code}
      boolean ${ev.isNull} = ${childGen.isNull};
      ${CodeGenerator.javaType(dataType)} ${ev.value} =
        ${CodeGenerator.defaultValue(dataType)};
      if (!${ev.isNull}) {
        ${ev.value} = UTF8String.fromString(
          ${childGen.value}.toString().toUpperCase());
      }
    """)
  }

  // Override for pretty printing.
  override def prettyName: String = "my_custom_function"
}
```

### Pattern 2: Creating Custom Optimisation Rules

```scala
object EliminateRedundantCasts extends Rule[LogicalPlan] {
  def apply(plan: LogicalPlan): LogicalPlan = plan.transformAllExpressions {
    case Cast(child, dataType, _, _) if child.dataType == dataType =>
      // Remove cast if types match.
      child
  }
}
```

### Pattern 3: Pattern Matching on Plans

```scala
plan match {
  case Project(projectList, child) =>
    // Handle projection.

  case Filter(condition, Project(projectList, child)) =>
    // Handle filter over projection.

  case Join(left, right, joinType, Some(condition), _) =>
    // Handle join with condition.

  case Aggregate(grouping, aggregates, child) =>
    // Handle aggregation.

  case _ =>
    // Default case.
}
```

### Pattern 4: Traversing Expression Trees

```scala
// Find all attribute references.
val attributes = expr.collect {
  case a: AttributeReference => a
}

// Find all subqueries.
val subqueries = expr.collect {
  case s: SubqueryExpression => s
}

// Transform specific expression types.
val transformed = expr.transformUp {
  case Add(Literal(0, _), right) => right
  case Add(left, Literal(0, _)) => left
}
```

### Pattern 5: Attribute Resolution

```scala
// Resolve attribute by name.
def resolve(attrName: String, input: LogicalPlan): Option[Attribute] = {
  input.output.find(_.name == attrName)
}

// Resolve with qualifier.
def resolveQualified(
    qualifier: Seq[String],
    attrName: String,
    input: LogicalPlan): Option[Attribute] = {
  input.output.find { attr =>
    attr.qualifier.startsWith(qualifier) && attr.name == attrName
  }
}
```

### Pattern 6: Working with Schema

```scala
// Create schema from attributes.
val schema = StructType(attributes.map { attr =>
  StructField(attr.name, attr.dataType, attr.nullable, attr.metadata)
})

// Convert schema to attributes.
val attributes = schema.toAttributes

// Add column to schema.
val newSchema = schema.add("newColumn", StringType, nullable = true)

// Drop column from schema.
val reducedSchema = StructType(schema.filterNot(_.name == "dropColumn"))
```

## Testing Catalyst Components

### Unit Testing Expressions

```scala
test("my custom function") {
  val input = Literal("hello")
  val expr = MyCustomFunction(input)

  // Test evaluation.
  assert(expr.eval(null) == UTF8String.fromString("HELLO"))

  // Test properties.
  assert(expr.dataType == StringType)
  assert(expr.foldable)
  assert(expr.deterministic)
}
```

### Testing Optimisation Rules

```scala
test("eliminate redundant casts") {
  val plan = Project(
    Seq(Alias(Cast(AttributeReference("x", IntegerType)(), IntegerType), "y")()),
    testRelation
  )

  val optimised = EliminateRedundantCasts(plan)

  val expected = Project(
    Seq(Alias(AttributeReference("x", IntegerType)(), "y")()),
    testRelation
  )

  comparePlans(optimised, expected)
}
```

## Performance Considerations

### Efficient Tree Traversal

- **Use tree patterns**: Tree patterns enable efficient pattern matching without full traversal.
- **Cache results**: Use lazy vals for expensive computations like `outputSet` and `references`.
- **Minimise transformations**: Only transform nodes that need changes.
- **Use `fastEquals`**: For quick equality checks without deep comparison.

### Code Generation Best Practices

- **Minimise virtual calls**: Generated code should avoid virtual method calls in tight loops.
- **Use primitive types**: Avoid boxing/unboxing in generated code.
- **Inline small functions**: Inline simple operations for better performance.
- **Batch operations**: Process multiple rows or columns together when possible.

### Rule Application Strategies

- **Order rules carefully**: Place more common optimisations first.
- **Use Once for expensive rules**: Cost-based optimisation should run once.
- **Set appropriate iteration limits**: Balance optimisation quality with compile time.
- **Track ineffective rules**: Use rule tracking to skip rules that won't apply.

## Common Pitfalls

1. **Forgetting nullability**: Always handle null values in expressions.
2. **Incorrect type coercion**: Ensure type casts are valid and safe.
3. **Infinite rule loops**: Rules must converge to a fixed point.
4. **Breaking plan invariants**: Maintain output schema and semantics.
5. **Leaking state**: Expressions should be stateless unless explicitly marked.
6. **Inefficient traversal**: Use tree patterns and targeted transformations.
7. **Missing code generation**: Implement `doGenCode` for custom expressions.
8. **Incorrect attribute resolution**: Use proper resolution with qualifiers.

## Additional Resources

- **Source code**: `sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/`
- **Tests**: `sql/catalyst/src/test/scala/org/apache/spark/sql/catalyst/`
- **Spark SQL documentation**: Official Spark SQL programming guide
- **Research paper**: "Spark SQL: Relational Data Processing in Spark" (SIGMOD 2015)

## Summary

The Catalyst framework provides:

- **Tree-based representation** for queries and expressions
- **Rule-based transformation** framework for optimisation
- **Extensibility** for custom expressions and optimisations
- **Code generation** for high-performance execution
- **Type-safe** API for query manipulation

Key extension points:

- Custom expressions (extend `Expression`)
- Custom optimisation rules (extend `Rule[LogicalPlan]`)
- Custom analysis rules (extend `Rule[LogicalPlan]`)
- Custom data sources (implement `TableProvider`)
- Custom aggregate functions (extend `AggregateFunction`)

When working with Catalyst, focus on immutability, type safety, and efficient tree traversal patterns.
