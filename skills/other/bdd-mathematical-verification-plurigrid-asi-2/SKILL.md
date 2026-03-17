---
name: bdd-mathematical-verification
description: 'BDD-Driven Mathematical Content Verification Skill


  Combines Behavior-Driven Development with mathematical formula extraction,

  verification, and transformation using:

  - Cucumber/Gherkin for specification

  - RSpec for implementation verification

  - mathpix-gem for LaTeX/mathematical content extraction

  - Pattern matching on syntax trees for formula validation


  Enables iterative discovery and verification of mathematical properties

  through executable specifications.

  '
metadata:
  trit: 0
  version: 1.0.0
  author: Claude Code + TegLon Labs mathpix-gem integration
  tags:
  - bdd
  - mathematics
  - gherkin
  - rspec
  - mathpix
  - verification
  - pattern-matching
  dependencies:
  - rspec: ~> 3.12
  - cucumber: ~> 8.0
  - mathpix: ~> 0.1.2
  - parslet: ~> 2.0
  - mathn: ~> 0.1.0
  features:
  - extract_mathematics: "Transform mathematical images/documents to LaTeX via Mathpix\
      \ API\nFeatures:\n  • Image to LaTeX conversion\n  • Document to Markdown parsing\n\
      \  • Chemistry structure to SMILES\n  • Batch processing with caching\n"
  - verify_formulas: "BDD-driven mathematical formula verification\nFeatures:\n  •\
      \ Syntax tree pattern matching\n  • Algebraic equivalence checking\n  • Form\
      \ verification (expanded/factored/simplified)\n  • Symbolic simplification validation\n"
  - scenario_driven_discovery: "Use Gherkin scenarios to discover mathematical properties\
      \ iteratively\nFeatures:\n  • Given-When-Then mathematical steps\n  • Parameterized\
      \ examples for multiple test cases\n  • Property-based testing integration\n\
      \  • Scenario outlines for formula families\n"
  - integration_with_content: "Connect extracted formulas to Music-Topos system\n\
      Features:\n  • Register verified formulas as artifacts\n  • Map formulas to\
      \ GaySeed colors\n  • Create provenance records in DuckDB\n  • Enable formula\
      \ search via retromap\n"
---

# BDD Mathematical Verification Skill

## Overview

This skill enables **Behavior-Driven Development (BDD)** workflows for mathematics, combining:

1. **Gherkin Specifications**: Plain-text scenario definitions
2. **RSpec Implementation**: Executable Ruby verification code
3. **mathpix-gem Integration**: Automatic LaTeX extraction from images
4. **Pattern Matching**: Syntax-tree validation for mathematical expressions
5. **Iterative Discovery**: Cucumber features guide formula exploration

## Core Components

### 1. Feature Specifications (Gherkin)

```gherkin
Feature: Mathematical Formula Extraction and Verification

  Scenario: Extract LaTeX from mathematical image
    Given I have a mathematical image file "quadratic.png"
    When I extract LaTeX using Mathpix
    Then I should get a LaTeX formula matching the pattern "ax^2 + bx + c"
    And the formula should be registered as an artifact

  Scenario: Verify quadratic formula in standard form
    Given a quadratic formula "x^2 - 5*x + 6"
    When I verify it is in standard form
    Then the coefficients should be [1, -5, 6]
    And it should be factorable as "(x - 2)(x - 3)"

  Scenario Outline: Verify binomial expansion
    Given a binomial expression "<binomial>"
    When I expand it using binomial theorem
    Then the result should match "<expanded>"
    And all terms should be present with correct signs

    Examples:
      | binomial  | expanded                    |
      | (x + 1)^2 | x^2 + 2*x + 1              |
      | (a - b)^3 | a^3 - 3*a^2*b + 3*a*b^2 - b^3 |
      | (2*x + 3)^2 | 4*x^2 + 12*x + 9         |
```

### 2. RSpec Implementation Blocks

```ruby
describe "Mathematical Formula Verification" do

  describe "Formula Extraction" do
    context "with valid mathematical image" do
      it "extracts LaTeX representation" do
        # Extraction step
      end

      it "normalizes notation to standard form" do
        # Normalization step
      end
    end

    context "with multi-page document" do
      it "extracts all formulas in order" do
        # Batch processing
      end
    end
  end

  describe "Formula Verification" do
    context "with polynomial expressions" do
      it "matches pattern against syntax tree" do
        # Pattern matching verification
      end

      it "verifies algebraic equivalence" do
        # Equivalence checking
      end
    end

    context "with nested/complex expressions" do
      it "validates form requirement" do
        # Form verification (expanded/factored/etc)
      end
    end
  end

  describe "Scenario-Driven Discovery" do
    context "with parameterized examples" do
      it "verifies all example variations" do
        # Parameterized testing
      end
    end
  end
end
```

### 3. Pattern Matching on Syntax Trees

```ruby
module MathematicalPatternMatching
  # Pattern: ax^n + bx^(n-1) + ... + c (polynomial)
  POLYNOMIAL_PATTERN = /^([^+\-]+)([\+\-][^+\-]+)*$/

  # Pattern: (expression)^exponent
  POWER_PATTERN = /^\(([^)]+)\)\^(\d+)$/

  # Match polynomial coefficients
  # In: "3*x^2 + 2*x + 1"
  # Out: {degree: 2, coefficients: [3, 2, 1], terms: [...]}

  def parse_polynomial(formula_str)
    # Returns AST (Abstract Syntax Tree)
    # Each node: {type: :term, coefficient: n, variable: 'x', exponent: m}
  end

  def verify_form(formula_ast, required_form)
    # required_form: :expanded, :factored, :simplified
    case required_form
    when :expanded
      all_terms_distributed?(formula_ast)
    when :factored
      has_minimal_complexity?(formula_ast)
    when :simplified
      no_like_terms_combinable?(formula_ast)
    end
  end
end
```

### 4. mathpix-gem Integration

```ruby
require 'mathpix'

class MathematicalContentExtractor
  def initialize(api_key: ENV['MATHPIX_API_KEY'])
    @client = Mathpix::Client.new(api_key: api_key)
  end

  # Image → LaTeX
  def extract_from_image(image_path)
    result = @client.process_image(
      image_path: image_path,
      output_format: :latex
    )
    {
      latex: result.latex,
      confidence: result.confidence,
      format: :latex
    }
  end

  # Document → Markdown with embedded LaTeX
  def extract_from_document(pdf_path)
    result = @client.process_document(
      document_path: pdf_path,
      output_format: :markdown
    )
    {
      content: result.markdown,
      formulas: extract_formulas(result.markdown),
      format: :markdown
    }
  end

  # Chemistry → SMILES
  def extract_from_chemistry(image_path)
    result = @client.process_image(
      image_path: image_path,
      output_format: :smiles
    )
    {
      smiles: result.smiles,
      format: :smiles
    }
  end

  private

  def extract_formulas(markdown_content)
    # Extract all $...$ and $$...$$ blocks
    formulas = []
    markdown_content.scan(/\$\$?([^\$]+)\$\$?/) do |match|
      formulas << {latex: match[0], inline: match[0].include?('\$')}
    end
    formulas
  end
end
```

### 5. Cucumber Step Definitions

```ruby
# features/step_definitions/mathematical_steps.rb

Given('a mathematical formula {string}') do |formula_str|
  @formula = formula_str
  @ast = MathematicalPatternMatching.parse_polynomial(@formula)
end

When('I extract LaTeX using Mathpix') do
  extractor = MathematicalContentExtractor.new
  @extracted = extractor.extract_from_image(@image_path)
end

When('I verify it is in {word} form') do |form|
  @form = form.to_sym
  @is_valid_form = MathematicalPatternMatching.verify_form(@ast, @form)
end

Then('the coefficients should be {brackets}') do |coefficients_str|
  coefficients = JSON.parse(coefficients_str.gsub('=>', ':'))
  extracted_coeffs = @ast[:coefficients]
  expect(extracted_coeffs).to eq(coefficients)
end

Then('it should be factorable as {string}') do |factored_form|
  factorization = @ast.factorize
  expect(factorization).to match_polynomial_pattern(factored_form)
end

Then('I should get a LaTeX formula matching the pattern {string}') do |pattern|
  expect(@extracted[:latex]).to match_latex_pattern(pattern)
end
```

### 6. RSpec Matchers for Mathematics

```ruby
module RSpec
  module Matchers
    # Match LaTeX pattern: "ax^2 + bx + c"
    matcher :match_latex_pattern do |expected_pattern|
      match do |actual|
        # Parse both patterns, compare syntactic structure
        actual_normalized = normalize_latex(actual)
        expected_normalized = normalize_latex(expected_pattern)
        structure_matches?(actual_normalized, expected_normalized)
      end
    end

    # Verify algebraic equivalence
    matcher :be_algebraically_equivalent_to do |expected|
      match do |actual|
        # Simplify both, compare canonical form
        actual_canonical = canonicalize_polynomial(actual)
        expected_canonical = canonicalize_polynomial(expected)
        actual_canonical == expected_canonical
      end
    end

    # Verify formula is in expanded form
    matcher :be_in_expanded_form do
      match do |formula_ast|
        # Check all products are distributed
        has_no_nested_products?(formula_ast) &&
        all_terms_separated?(formula_ast)
      end
    end
  end
end
```

### 7. Integration with Music-Topos

```ruby
class MathematicalArtifactRegistration
  def initialize(provenance_db: DuckDB.new)
    @db = provenance_db
  end

  def register_verified_formula(formula_ast, extraction_method, scenario_name)
    artifact_id = generate_artifact_id(formula_ast)

    # Register in provenance database
    @db.execute(
      "INSERT INTO artifacts (id, content, type, metadata)
       VALUES (?, ?, 'formula', ?)",
      [
        artifact_id,
        formula_ast.to_json,
        {
          latex: formula_ast.to_latex,
          verified: true,
          verification_scenario: scenario_name,
          extraction_method: extraction_method,
          timestamp: Time.now.iso8601,
          gayseed_color: assign_color(formula_ast)
        }.to_json
      ]
    )

    artifact_id
  end

  private

  def generate_artifact_id(formula_ast)
    content_hash = Digest::SHA256.hexdigest(formula_ast.canonical_form)
    "formula-#{content_hash[0..15]}"
  end

  def assign_color(formula_ast)
    gayseed_index = GaySeed.hash_to_index(formula_ast.canonical_form)
    GaySeed::PALETTE[gayseed_index]
  end
end
```

## Usage Examples

### Example 1: BDD Workflow - Polynomial Verification

```bash
# 1. Write feature file
cat > features/polynomial_verification.feature << 'EOF'
Feature: Verify polynomial in standard form

  Scenario: Extract and verify quadratic
    Given a mathematical image file "quadratic_equation.png"
    When I extract LaTeX using Mathpix
    And I parse the extracted formula
    Then the formula should match pattern "ax^2 + bx + c"
    And it should have exactly 3 terms
    And it should register as verified artifact
EOF

# 2. Run Cucumber to generate step definitions
cucumber --dry-run features/polynomial_verification.feature

# 3. Implement step definitions in features/step_definitions/

# 4. Run full BDD verification
cucumber features/polynomial_verification.feature

# 5. Verify with RSpec
rspec spec/mathematical_formula_spec.rb
```

### Example 2: Scenario Outline - Formula Family Testing

```gherkin
Feature: Binomial Expansion Verification

  Scenario Outline: Verify binomial theorem for various exponents
    Given a binomial expression "<binomial>"
    When I apply binomial theorem
    Then the expanded form should be "<expanded>"
    And each term should verify against the pattern

    Examples: Basic binomials
      | binomial  | expanded                        |
      | (x + 1)^2 | x^2 + 2*x + 1                  |
      | (x - 1)^2 | x^2 - 2*x + 1                  |
      | (x + 2)^2 | x^2 + 4*x + 4                  |

    Examples: Coefficient variations
      | binomial    | expanded                      |
      | (2*x + 1)^2 | 4*x^2 + 4*x + 1              |
      | (x + 3)^2   | x^2 + 6*x + 9                |
      | (3*x - 2)^2 | 9*x^2 - 12*x + 4             |
```

### Example 3: RSpec + Pattern Matching

```ruby
describe "Mathematical Formula Pattern Matching" do
  let(:extractor) { MathematicalContentExtractor.new }

  describe "Polynomial degree detection" do
    context "with valid polynomial" do
      it "identifies degree from syntax tree" do
        formula = "3*x^4 + 2*x^2 + 1"
        ast = MathematicalPatternMatching.parse_polynomial(formula)
        expect(ast.degree).to eq(4)
      end
    end
  end

  describe "Algebraic equivalence" do
    it "verifies (x+1)^2 ≡ x^2 + 2x + 1" do
      f1 = "(x + 1)^2"
      f2 = "x^2 + 2*x + 1"
      expect(f1).to be_algebraically_equivalent_to(f2)
    end
  end

  describe "Form verification" do
    it "validates formula is in expanded form" do
      formula_ast = parse_as_ast("x^2 + 2*x + 1")
      expect(formula_ast).to be_in_expanded_form
    end

    it "rejects non-expanded formulas" do
      formula_ast = parse_as_ast("(x + 1)^2")
      expect(formula_ast).not_to be_in_expanded_form
    end
  end
end
```

## Iterative Discovery Process

### Phase 1: Feature Definition
- Write Gherkin scenarios describing mathematical behavior
- Parameterize examples for formula families
- Use natural language for accessibility

### Phase 2: Step Implementation
- Implement each Given/When/Then step
- Create RSpec matchers for assertions
- Define pattern matching rules

### Phase 3: mathpix-gem Integration
- Extract real content from images/documents
- Normalize extracted LaTeX to standard forms
- Create parsing pipeline

### Phase 4: Verification
- Run Cucumber features to validate specifications
- Run RSpec for detailed unit verification
- Register verified formulas as artifacts

### Phase 5: Artifact Integration
- Store formulas in DuckDB provenance database
- Assign deterministic GaySeed colors
- Create retromap entries for temporal tracking

## Testing the Skill

```bash
# Run all BDD tests
cucumber features/

# Run RSpec tests
rspec spec/

# Run with coverage
rspec --format documentation --require spec_helper spec/

# Run specific feature
cucumber features/polynomial_verification.feature -t @focus

# Integration test with Music-Topos
rspec spec/music_topos_integration_spec.rb
```

## Configuration

```ruby
# config/bdd_mathematical_verification.rb

BddMathematicalVerification.configure do |config|
  # Mathpix API configuration
  config.mathpix_api_key = ENV['MATHPIX_API_KEY']
  config.mathpix_timeout = 30
  config.mathpix_batch_size = 10

  # Pattern matching configuration
  config.polynomial_degree_limit = 10
  config.expression_complexity_limit = 50

  # Verification configuration
  config.enable_symbolic_simplification = true
  config.algebraic_equivalence_method = :canonical_form

  # Artifact registration
  config.register_to_provenance = true
  config.provenance_database = DuckDB.new('data/provenance/provenance.duckdb')
end
```

## Dependencies

- **rspec** (3.12+): Executable specification framework
- **cucumber** (8.0+): Gherkin scenario runner
- **mathpix** (0.1.2+): LaTeX extraction from images
- **parslet** (2.0+): Parser combinator for syntax trees
- **mathn** (0.1.0+): Mathematical operations in pure Ruby

## Integration Points

### With Music-Topos
- Register verified formulas as artifacts
- Assign GaySeed colors deterministically
- Create provenance records with timestamps
- Enable formula search via DuckDB retromap

### With Glass-Bead-Game Skill
- Create Badiou triangles from formula domains
- Link mathematical concepts to philosophical structures
- Generate synthesis insights through formula relationships

### With Bisimulation-Game Skill
- Verify observational equivalence of formulas
- Test semantic preservation through transformations
- Validate GF(3) conservation in algebraic operations

## Future Enhancements

1. **Interactive Mode**: Real-time formula input and verification
2. **Proof Generation**: Automatic proof verification for theorems
3. **LaTeX Optimization**: Convert extracted LaTeX to canonical forms
4. **Machine Learning**: Learn formula patterns from verified examples
5. **Symbolic Computation**: Integration with SymPy or Sage
6. **Distributed Testing**: Parallel scenario execution across agents

## References

- **Mathpix API**: https://docs.mathpix.com/
- **Cucumber Gherkin**: https://cucumber.io/docs/gherkin/
- **RSpec**: https://rspec.info/
- **Ruby Pattern Matching**: https://docs.ruby-lang.org/
- **Numbas Pattern Matching**: http://numbas.org.uk/

---

**Status**: ✓ Ready for iterative BDD-driven mathematical discovery
**Last Updated**: December 21, 2025
