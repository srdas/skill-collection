---
name: good-research
description: Evaluate research ideas using the FINER criteria and ROI framework (Rigor, Originality, Impact) to ensure research questions are feasible, novel, and impactful
---

# What Is Good Research?

## Trigger

Activate when the user asks to:
- Evaluate whether a research idea or question is good
- Improve or refine a research question
- Assess the feasibility, novelty, or impact of a proposed study
- Apply the FINER criteria or ROI framework to a research plan
- "Is this a good research question?"
- "How can I make this research idea stronger?"

Also invocable manually with `/good-research`.

## Behavior

When the user presents a research idea, question, or plan, evaluate it against two complementary frameworks and provide actionable feedback.

### Framework 1: The FINER Criteria

Assess the research idea against each criterion:

| Criterion | Question to Ask |
| --- | --- |
| **Feasible** | Do you have the time, money, equipment, and technical expertise to pull it off? |
| **Interesting** | Does it pique the interest of the researcher and the broader peer community? |
| **Novel** | Does it provide new findings, confirm/refute previous findings, or extend current knowledge? |
| **Ethical** | Can it be cleared by review boards without harm to participants? |
| **Relevant** | Does it matter to the field, policy-makers, or future research? |

### Framework 2: The ROI of Research (Rigor, Originality, Impact)

Evaluate the idea across three dimensions that together produce seminal work:

#### Rigor (The "Trust" Factor)

Methodological integrity that makes results credible:
- **Internal Validity** -- Are the tools actually measuring what they claim to measure?
- **Reproducibility** -- Can someone follow the method and get the same results?
- **Transparency** -- Does the idea account for its own biases and limitations?

Risk: An idea that is original and impactful but lacks rigor will be debunked or retracted.

#### Originality (The "Discovery" Factor)

The newness of the contribution, which keeps the field moving forward:
- **Conceptual Originality** -- Using a new theory to explain an old phenomenon.
- **Empirical Originality** -- Testing something that has never been tested.
- **Methodological Originality** -- Using a new technique to look at data in a way nobody has before.

Risk: An idea that is rigorous and impactful but lacks originality feels like maintenance rather than innovation.

#### Impact (The "Value" Factor)

The magnitude of change the research causes:
- **Academic Impact** -- Does it change the way other scientists think?
- **Societal/Economic Impact** -- Does it save lives, save money, or change policy?

Risk: An idea that is rigorous and original but has zero impact becomes ivory tower trivia.

#### The ROI Interplay

The three dimensions interact as a Venn diagram:

| Intersection | Resulting Outcome |
| --- | --- |
| Rigor + Originality | A brilliant, technical paper that nobody cites because it doesn't solve a relevant problem. |
| Originality + Impact | A viral study that makes headlines but collapses under scrutiny due to sloppy methods. |
| Rigor + Impact | Solid, useful work that feels incremental because it doesn't break new ground. |
| **Rigor + Originality + Impact** | **The sweet spot -- seminal work that defines a career.** |

### Additional Quality Checks

#### The "Goldilocks" Scope Test

Reject ideas that are too broad or too narrow:
- **Too broad** (e.g., "How does climate change affect the world?") leads to shallow analysis.
- **Too narrow** (e.g., "The impact of rain on a specific 2-inch patch of grass in my backyard") lacks data or impact.
- **The sweet spot**: A specific, focused question that allows for deep, rigorous investigation.

#### The "Gap" Test

A good research idea identifies a knowledge gap in the existing literature:
1. Find a hole in the existing body of knowledge.
2. Propose a way to fill it.
3. Explain why that specific piece matters to the rest of the picture.

#### The "So What?" Test

If a colleague's response to the idea is "So what?", it isn't ready. Evaluate across three impact dimensions:

| Aspect | What to Ask |
| --- | --- |
| Theoretical Impact | Does this change how we understand a concept? |
| Practical Impact | Can this be used to fix a real-world problem? |
| Methodological Impact | Does this introduce a new way of measuring or testing something? |

#### Personal Resonance

Research is a marathon. A good idea is one the researcher is genuinely curious about. Without that curiosity, burnout is likely before the analysis phase.

**Pro tip:** Look for tensions or contradictions in the field. If Study A says "X causes Y" and Study B says "X prevents Y," there is a great research idea hidden in that disagreement.

## Output Format

Present the evaluation as a structured assessment:

```
## Research Idea Assessment

### Summary
[One-sentence restatement of the proposed research idea]

### FINER Evaluation
- **Feasible**: [Pass/Concern/Fail] -- [brief explanation]
- **Interesting**: [Pass/Concern/Fail] -- [brief explanation]
- **Novel**: [Pass/Concern/Fail] -- [brief explanation]
- **Ethical**: [Pass/Concern/Fail] -- [brief explanation]
- **Relevant**: [Pass/Concern/Fail] -- [brief explanation]

### ROI Assessment
- **Rigor**: [High/Medium/Low] -- [what strengthens or weakens it]
- **Originality**: [High/Medium/Low] -- [what's new vs. derivative]
- **Impact**: [High/Medium/Low] -- [who benefits and how]

### Scope Check
[Is the scope appropriately sized? Too broad or too narrow?]

### Gap and "So What?" Analysis
[What knowledge gap does this fill? Why does it matter?]

### Recommendations
[Specific, actionable suggestions to strengthen the idea]

### Overall Verdict
[Strong / Promising with revisions / Needs rethinking]
```

## Constraints

- Always ground feedback in the specific details of the user's idea -- do not give generic advice.
- Be honest but constructive. If an idea has fundamental problems, say so and suggest a pivot rather than just listing weaknesses.
- When the user's idea scores low on one ROI dimension, suggest concrete ways to strengthen it.
- Do not dismiss incremental research. Replication and extension studies are valuable when done rigorously.
- If the user provides data or documents alongside the idea, use the `/researcher` skill to analyze them and inform the evaluation.

## Examples

**Evaluating a proposed study:**
```
/good-research "I want to study whether remote work improves productivity"
```
--> Assesses scope (too broad as stated), suggests narrowing to a specific industry or metric, evaluates feasibility of data collection, and rates ROI dimensions.

**Refining a research question:**
```
/good-research "Does social media usage correlate with anxiety in teenagers aged 13-17 in urban areas?"
```
--> Evaluates FINER criteria, notes the scope is well-sized, flags ethical considerations for studying minors, and suggests methodological approaches that improve rigor.

**Comparing research directions:**
```
/good-research "I'm torn between studying X and Y -- which is a stronger research idea?"
```
--> Applies both frameworks to each idea and presents a side-by-side comparison with a recommendation.
