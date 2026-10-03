---
name: humanizer
description: Rewrites AI-generated text to sound natural and human by removing "AI-isms" (verbose, sycophantic, or formulaic patterns). Based on Wikipedia's AI cleanup guidelines. Adapted from the humanizer project by blader.
---

# Humanizer

This skill is designed to strip away the "fingerprints" of AI-generated writing. It transforms text from the typical verbose, sycophantic, and formulaic style of LLMs into a direct, natural, and "human" tone.

## The 24 Patterns to Eliminate

Rigorously audit and rewrite the input text to eliminate these specific "AI fingerprints":

### 1. Content & Logic
- **Significance Inflation:** Avoid "marking a pivotal moment" or "evolution of." Use direct facts.
- **Notability Name-dropping:** Don't just list sources (NYT, BBC). Integrate them naturally.
- **Superficial "-ing" Analyses:** Remove "symbolizing," "reflecting," or "showcasing" unless backed by specific data.
- **Promotional Language:** Remove "nestled within," "breathtaking," or "vibrant."
- **Vague Attributions:** Replace "Experts believe" with specific names or studies.
- **Formulaic Challenges:** Replace "Despite challenges... continues to thrive" with actual, specific obstacles.

### 2. Language & Vocabulary
- **AI Vocabulary:** Eliminate: *Additionally, testament, landscape, showcasing, underscore, pivotal, delve, tapestries.*
- **Copula Avoidance:** Replace "serves as," "features," or "boasts" with "is" or "has."
- **Negative Parallelisms:** Avoid "It's not just X, it's Y." State the point directly.
- **Rule of Three:** Break up forced triplets (e.g., "innovation, inspiration, and insights"). Use 2 or 4+ items if more natural.
- **Synonym Cycling:** Don't rotate through "protagonist, hero, central figure." Stick to the clearest term.
- **False Ranges:** Avoid "from the Big Bang to dark matter." List specific topics.

### 3. Style & Formatting
- **Em Dash Overuse:** Replace excessive dashes with commas or periods.
- **Boldface Overuse:** Remove unnecessary bolding of keywords.
- **Inline-header Lists:** Convert "Topic: Description" lists into flowing prose.
- **Title Case Headings:** Use sentence case for headings.
- **Emojis:** Remove all emojis.
- **Curly Quotes:** Convert “smart quotes” to "straight quotes".

### 4. Communication & Tone
- **Chatbot Artifacts:** Remove "I hope this helps!" or "Let me know if you need more."
- **Cutoff Disclaimers:** Remove "While details are limited..." or "As an AI..."
- **Sycophantic Tone:** Remove "Great question!" or "You're absolutely right!"
- **Filler Phrases:** Replace "In order to" with "To"; "Due to the fact that" with "Because."
- **Excessive Hedging:** Replace "could potentially possibly" with "may."
- **Generic Conclusions:** Replace "The future looks bright" with specific next steps.

## Mandatory Workflow

1. **Analyze:** Identify which of the 24 patterns are present in the text.
2. **First Rewrite:** Rewrite the text to eliminate all identified patterns. Use a direct, concise, and active voice.
3. **Audit Pass:** Review the draft for any remaining "AI-isms" or sycophancy.
4. **Final Polish:** If it still feels "bot-like," rewrite it again with a more opinionated or casual tone until it sounds human.
