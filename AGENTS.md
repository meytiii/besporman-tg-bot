# Workspace Agent Rules: Bespor Man (بسپر من)

Always adhere to the following rules when working in this repository:

1. **NO ZERO WIDTH NON-JOINER (ZWNJ / U+200C):**
   - Absolutely NEVER use `\u200c` (Persian half-space, Ctrl+Shift+2) in user-facing Persian text, button labels, templates, messages, DB content, or logs.
   - Use standard ordinary spaces instead (e.g., `می خواهم`, `بهترین ها`, `برنامه نویسی`, `می توانید`).
   - Automated checks must verify zero occurrences of `\u200c`.

2. **TELEGRAM ADMINISTRATOR IDENTIFIERS:**
   - Admin numeric Telegram IDs are `347382968` and `106629087`.
   - Never authenticate by username alone; always verify numeric user ID.

3. **TONE & HUMANIZER:**
   - Follow the `humanizer` skill: direct, natural, conversational Iranian Persian.
   - No generic AI marketing clichés ("cutting-edge", "tailored solutions", "transforming dreams").
   - Friendly, relaxed, confident, slightly mischievous developer humor, professional underneath.
   - Emojis used with restraint (1-2 contextual emojis).

4. **NO ARBITRARY DECISIONS:**
   - Do not assume, guess, or invent requirements.
   - Whenever an ambiguity or product decision arises, stop and present:
     1. What is unclear
     2. Why it matters
     3. Available options
     4. Recommended option
   - Wait for the user's approval.

5. **REAL CONTENT ONLY:**
   - No fake testimonials, fake portfolio projects, fake resumes, or fabricated developer identities.
   - Public team aliases: `م.خ` and `ط.ذ`.
   - Use clear placeholders where real assets are pending.

Refer to [PROJECT_NOTES.md](file:///c:/Users/Mahdi/Desktop/Stuf/Github/besporman-tg-bot/PROJECT_NOTES.md) for full project details.
