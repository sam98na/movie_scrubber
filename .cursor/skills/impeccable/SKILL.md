---
name: impeccable
description: "Create distinctive, production-grade frontend interfaces with high design quality. Generates creative, polished code that avoids generic AI aesthetics. Use when the user asks to build web components, pages, artifacts, posters, or applications, or when any design skill requires project context."
license: Apache 2.0. Based on Anthropic's frontend-design skill. See https://github.com/pbakaus/impeccable for attribution.
source: pbakaus/impeccable (https://github.com/pbakaus/impeccable)
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

## Context Gathering Protocol

Design skills produce generic output without project context. You MUST have confirmed design context before doing any design work.

**Required context** (every design skill needs at minimum):
- **Target audience**: Who uses this product and in what context?
- **Use cases**: What jobs are they trying to get done?
- **Brand personality/tone**: How should the interface feel?

**CRITICAL**: You cannot infer this context by reading the codebase. Code tells you what was built, not who it's for or what it should feel like. Only the creator can provide this context.

**Gathering order:**
1. **Check current instructions (instant)**: If your loaded instructions already contain a **Design Context** section, proceed immediately.
2. **Check `.impeccable.md` (fast)**: If not in instructions, read `.impeccable.md` from the project root. If it exists and contains the required context, proceed.
3. **Ask the user**: If neither source has context, ask 3-5 focused UX questions before doing anything else. Do NOT attempt to infer context from the codebase instead.

---

## Design Direction

Commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work. The key is intentionality, not intensity.

Then implement working code that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail

## Frontend Aesthetics Guidelines

### Typography

Choose fonts that are beautiful, unique, and interesting. Pair a distinctive display font with a refined body font.

Always apply these:

- Use a modular type scale with fluid sizing (`clamp`) for headings on marketing/content pages. Use fixed `rem` scales for app UIs and dashboards.
- Use fewer sizes with more contrast. A 5-step scale with at least a 1.25 ratio between steps creates clearer hierarchy than 8 sizes that are 1.1× apart.
- Line-height scales inversely with line length. Narrow columns want tighter leading, wide columns want more. For light text on dark backgrounds, ADD 0.05–0.1 to your normal line-height.
- Cap line length at ~65–75ch.

DO NOT use overused fonts like **Inter, Roboto, Arial, Open Sans**, or system defaults. Also reject the model's reflex defaults: **Fraunces, Newsreader, Lora, Crimson, Crimson Pro, Crimson Text, Playfair Display, Cormorant, Cormorant Garamond, Syne, IBM Plex Mono/Sans/Serif, Space Mono, Space Grotesk, DM Sans, DM Serif Display, DM Serif Text, Outfit, Plus Jakarta Sans, Instrument Sans, Instrument Serif**. Look further.

DO NOT use monospace as lazy shorthand for "technical". DO NOT put large rounded icons above every heading. DO NOT use only one font family. DO NOT use a flat hierarchy where sizes are too close together. DO NOT set long body passages in uppercase.

### Color & Theme

- Use OKLCH, not HSL. As you move toward white or black, REDUCE chroma — high chroma at extreme lightness looks garish.
- Tint your neutrals toward your brand hue (chroma of 0.005–0.01 is perceptible and creates subconscious cohesion).
- 60-30-10 by visual weight, not pixel count. 60% neutral / surface, 30% secondary text and borders, 10% accent.
- Theme (light vs dark) should be DERIVED from audience and viewing context, not picked from a default.

DO NOT use pure black (#000) or pure white (#fff). Always tint.
DO NOT use the AI color palette: cyan-on-dark, purple-to-blue gradients, neon accents on dark backgrounds.
DO NOT use gradient text. Solid colors only for text.
DO NOT default to dark mode with glowing accents.

### Layout & Space

- 4pt spacing scale with semantic token names (`--space-sm`, `--space-md`).
- Use `gap` instead of margins for sibling spacing.
- Vary spacing for hierarchy.
- Self-adjusting grid: `grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))`.
- Container queries for components, viewport queries for page layout.

DO create visual rhythm through varied spacing.
DO use asymmetry and unexpected compositions.

DO NOT wrap everything in cards. Not everything needs a container.
DO NOT nest cards inside cards. Visual noise; flatten the hierarchy.
DO NOT use identical card grids.
DO NOT center everything.
DO NOT let body text wrap beyond ~80 characters per line.

### Visual Details — bans

These CSS patterns are NEVER acceptable. They are the most recognizable AI design tells.

**BAN 1: Side-stripe borders on cards/list items/callouts/alerts.** Pattern: `border-left:` or `border-right:` with width greater than 1px. Includes any color or variable. Rewrite with full borders, background tints, leading numbers/icons, or no visual indicator at all.

**BAN 2: Gradient text.** Pattern: `background-clip: text` (or `-webkit-background-clip: text`) combined with a gradient background. Use a single solid color for text. Use weight or size for emphasis instead of gradient fill.

DO NOT: Use glassmorphism everywhere (blur effects, glass cards, glow borders used decoratively rather than purposefully).
DO NOT: Use sparklines as decoration.
DO NOT: Use rounded rectangles with generic drop shadows.
DO NOT: Use modals unless there's truly no better alternative.

### Motion

- Use motion to convey state changes: entrances, exits, feedback.
- Exponential easing (ease-out-quart/quint/expo) for natural deceleration.
- For height animations, use `grid-template-rows` transitions instead of animating height directly.
- Animate transform and opacity only.
- DO NOT use bounce or elastic easing.

### Interaction

- Use progressive disclosure. Start simple, reveal sophistication through interaction.
- Empty states should teach the interface, not just say "nothing here".
- DO NOT make every button primary. Use ghost buttons, text links, secondary styles.

### Responsive

- Container queries for component-level responsiveness.
- Adapt the interface for different contexts; don't just shrink it.

### UX Writing

- Make every word earn its place.
- Don't repeat information users can already see.

---

## The AI Slop Test

**Critical quality check**: If you showed this interface to someone and said "AI made this," would they believe you immediately? If yes, that's the problem.

A distinctive interface should make someone ask "how was this made?" not "which AI made this?"

---

## Implementation Principles

Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices across generations.
