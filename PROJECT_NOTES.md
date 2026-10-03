# BESPOR MAN (بسپر من) — CRITICAL PROJECT NOTES & INSTRUCTIONS

## 1. Project Overview & Identity
- **Brand Name:** بسپر من (Bespor Man)
- **Role:** Interactive lead-generation, project intake, portfolio showcase, customer satisfaction showcase, team/resume, and admin ↔ client communication bridge Telegram bot for a software development team.
- **Core Message:** "You have a software project. Give it to us. We will handle the technical side." (Client ↔ Bespor Man ↔ Development Team).
- **Core Capabilities:** Web development, Windows desktop applications, CRM systems, Telegram bots, administrative/organizational software, SEO, custom software systems.

---

## 2. ABSOLUTE ZERO ZWNJ / HALF-SPACE RULE (NO U+200C)
- **STRICT MANDATE:** NEVER include Zero Width Non-Joiner (`\u200c`, U+200C, Persian half-space / Ctrl+Shift+2) anywhere in user-facing Persian text, button labels, templates, messages, DB content, or logs.
- **Standard Spacing:** Use ordinary spaces instead.
  - WRONG: `میخواهیم`, `بهترینها`, `برنامهنویسی`, `میتوانید`
  - CORRECT: `می خواهیم`, `بهترین ها`, `برنامه نویسی`, `می توانید`
- **Validation:** Every Persian string and file must be strictly scanned and tested to ensure zero occurrences of `\u200c`.

---

## 3. Authorized Telegram Administrators
- **Admin IDs (Numeric Telegram User IDs):**
  - `347382968`
  - `106629087`
- Authorization must always check the numeric user ID on every administrative request. Never rely only on usernames.
- Multi-admin concurrency and audit logs must track which admin took each action.

---

## 4. Voice, Tone & Humanizer Guidelines
- **Personality:** Friendly, human, relaxed, confident, approachable, slightly mischievous, natural Iranian developer humor, professional underneath.
- **No AI Slop / Clichés:** Strip out all corporate marketing phrases ("cutting-edge", "tailored solutions", "transforming dreams into reality", "we are thrilled to").
- **Natural Iranian Persian:** Conversational, fluent, easy to understand.
- **Minimal & Intentional Emojis:** 1-2 contextual emojis max; no excessive strings of emojis (`🔥🔥🔥`, `😂😂😂😂`).
- **Humanizer & Caveman Skills:**
  - `humanizer`: strip verbose, formulaic, sycophantic LLM patterns.
  - `caveman`: ultra-terse responses when compressed mode is invoked.

---

## 5. Absolute Rule: No Arbitrary Decisions & Question Protocol
- Do NOT guess, fabricate, or silently make architectural or product decisions.
- When an ambiguity or decision arises, stop and present:
  1. What is unclear
  2. Why it matters
  3. Available options
  4. Recommended option
- Wait for user decision before proceeding.

---

## 6. Content Integrity: No Fake Content
- Never fabricate testimonials, clients, portfolio items, developer resumes, or pricing.
- Use clean, clearly marked placeholders with exact instructions for replacement.
- Developer aliases: `م.خ` and `ط.ذ`. Never reveal real identities unless approved.

---

## 7. Key Architecture & Features
- **Order Flow:** Free-form project description stage first. Generates unique order number (e.g. `#1001`). State machine: `NEW`, `UNDER_REVIEW`, `WAITING_FOR_CLIENT`, `NEGOTIATING`, `ACCEPTED`, `REJECTED`, `CLOSED`.
- **Admin ↔ Client Bridge:** Bot is intermediary. Admin messages appear as "بسپر من". Client never sees admin ID. Admin can request info or reply directly to orders.
- **Support & Profanity Filter:** Natural, intelligent profanity/inappropriate filter handling Persian/Arabic character variations, repetitions, and spaces without naive false positives.
- **Portfolio & Testimonials:** Inline buttons, detail views, multi-image support, random testimonial viewer, "Start Similar Order" CTA.
- **Navigation:** Clear back (`🔙 بازگشت`) and cancel (`❌ لغو`) buttons at all steps. No dead-ends.
- **Security & Reliability:** Rate limiting, flood prevention, callback safety, idempotency on webhooks/updates, environment-based configuration (`.env`).
