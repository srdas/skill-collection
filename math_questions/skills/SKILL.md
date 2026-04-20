---
name: math-questions
description: Generate and solve math questions that test deep conceptual understanding rather than mechanical computation
---

# Good Math Questions

## Purpose

Generate and solve math questions that test deep conceptual understanding rather than mechanical computation or memorized formulas. These questions should reward creativity, multi-perspective thinking, and the ability to connect seemingly unrelated ideas.

## Invocation

When asked to generate a math question, solve a math question in this style, or evaluate whether a question meets these standards, follow the principles and structure below.

## Core Principles

### What a Good Math Question Is

1. **Conceptually challenging, not computationally heavy.** If you see it the right way, the problem falls apart quickly. Avoid problems that take long to calculate.
2. **Requires multiple perspectives.** The solver must combine algebraic, geometric, physical, or numerical viewpoints to reach the answer.
3. **Connects seemingly unrelated ideas.** The solver must recognize which tools apply when it is not immediately obvious, or must sequence techniques from different topics.
4. **Novel application of known concepts.** The problem should not resemble standard textbook exercises. It applies familiar ideas to unfamiliar situations.
5. **Beautiful once solved.** The solution should produce a moment of clarity or elegance that deepens understanding of the underlying mathematics.
6. **Rewards depth over breadth.** A student who truly understands the central concepts will find the problem tractable; one who only memorized procedures will not.

### What a Good Math Question Is NOT

- An algorithm to mimic or a formula to regurgitate.
- A trick question that depends on obscure facts.
- A problem where brute-force computation is the only path.
- A problem that is hard solely because of algebraic complexity.
- A problem that is identical in structure to a homework exercise.

## Structure for Generating Questions

When generating a math question, produce the following sections:

### 1. Question

State the problem clearly and precisely. Include all necessary definitions. The problem should be self-contained.

### 2. Answer

Provide a complete, elegant solution. Emphasize the conceptual insight that unlocks the problem. Show how the right perspective makes the solution fall into place naturally.

### 3. Why This Is a Good Question

Explain which principles from the list above this question satisfies. Address:
- What conceptual understanding it tests
- Why a purely mechanical approach fails or is unnecessarily difficult
- What the "aha moment" is
- What multiple perspectives or connections are required
- Whether it has accessible entry points (partial credit opportunities) alongside deeper challenges

## Difficulty Calibration

Good questions often have these structural features:

- **Graduated difficulty.** An easy entry point (like part (a) of Example 2 in the source material) followed by a harder part that requires genuine insight.
- **Deceptive simplicity.** The problem looks simple to state but requires non-obvious reasoning (like Example 4, where the answer seems like it must be false but is actually true).
- **Multiple valid approaches.** The best approach is elegant and conceptual, but partial progress is possible through other means (like Example 1, where testing a specific function gives partial credit).
- **Forward connections.** The question introduces or foreshadows concepts from future courses while being solvable with current knowledge (like Example 6 introducing chi-squared).

## Guidelines for Solving Questions in This Style

When solving a problem that fits this paradigm:

1. **Resist computation first.** Before calculating anything, ask: what is this problem really about? What concept is at its heart?
2. **Draw from multiple viewpoints.** Consider the algebraic, geometric, physical, and numerical interpretations. Often the key insight comes from switching perspectives.
3. **Look for orthogonality, symmetry, and structure.** Many elegant solutions exploit structural properties (like orthogonality of radial fields to circular paths in Example 3).
4. **Use small cases to build intuition.** Experiment with 2x2 matrices, specific simple functions, or low-dimensional cases to see the pattern before proving the general result (as suggested in Example 4).
5. **Identify what makes this problem different from the standard case.** The novelty is usually where the insight lives (like the Ito calculus distinction in Example 5 where $d\ln S \neq \frac{dS}{S}$).
6. **Verify the solution is elegant.** If your answer requires pages of computation, you likely missed the intended insight. Step back and look for the conceptual shortcut.

## Topic-Specific Patterns

These patterns from the examples illustrate how good questions arise across mathematical areas:

| Pattern | Example |
|---------|---------|
| Test equivalence of two definitions by applying both simultaneously | Derivative as limit vs. slope of tangent line |
| Reinterpret an algebraic equation as a geometric object in parameter space | Dot product equation as a plane; cross product magnitude as a cylinder |
| Prove impossibility via contradiction using multiple theorems together | Conservative field + radial field + specific integrals yield contradiction |
| Show a surprising equivalence holds by examining what terms actually contribute | Any matrix can act as symmetric in a quadratic form |
| Reconcile two seemingly contradictory numerical results via theory | Ito vs. ordinary calculus giving different estimates of the same parameter |
| Apply a theorem in a non-obvious context by recognizing its prerequisites are met | Central Limit Theorem applied to chi-squared by recognizing it as a sum of iid variables |

## Quality Checklist

Before finalizing a generated question, verify:

- [ ] A student cannot solve it by pattern-matching to a textbook example
- [ ] The computational burden is low once the conceptual insight is found
- [ ] The problem is solvable with the stated prerequisite knowledge
- [ ] There is a clear "aha moment" in the solution
- [ ] The problem tests understanding from at least two different angles
- [ ] The statement is unambiguous and self-contained
- [ ] Partial credit pathways exist for students who understand some but not all aspects
- [ ] The solution, once seen, deepens appreciation for the underlying mathematics
