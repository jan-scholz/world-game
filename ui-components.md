# UI Components

Visual inventory of every major UI element — appearance, positioning, and mobile adaptations.

---

## Global Styling

- **Background:** Light blue-grey (`#e8f4f8`)
- **Font:** Inter (Google Fonts), fallback to `system-ui, sans-serif`
- **Overflow:** Hidden on `html` and `body` — no page-level scrolling
- **Shared panel style:** White semi-transparent (`rgba(255,255,255,0.95)`), 8px backdrop blur, 16px border radius, drop shadow (`0 4px 24px rgba(0,0,0,0.18)`), 16px/20px padding

---

## 1. SVG Map (`#map`)

- **Size:** Full viewport (`100vw × 100vh`), fills entire background
- **Projection:** D3 Natural Earth — centered in viewport, scale = `width / 6.3`
- **Country paths (`.country`):**
  - Default: grey fill (`#ccc`), dark grey stroke (`#666`, 0.5px)
  - Hover/tap in explore (`.highlighted`): orange fill (`#f90`), red stroke (`#c00`, 1.5px)
  - Quiz target (`.target`): blue fill (`#4a90d9`), dark blue stroke (`#1a5fa0`, 2px)
  - Wrong click (`.wrong-guess`): red fill (`#e05555`), dark red stroke (`#a02020`, 1.5px) — flashes for 600ms
  - Cursor: pointer on all countries
- **Zoom:** Scroll-wheel and drag, 1×–24× scale range, applied as CSS transform on inner `<g>`. Stroke widths are divided by the current zoom scale (`--zoom-k` CSS custom property) so borders remain a constant pixel width at all zoom levels.
- **Touch interaction (explore):** Tap a country to highlight it and show its info panel (equivalent to hover). Tap a different country to switch. Tap the same country or empty area to dismiss.

---

## 2. Overlay Screens

Shared container (`.overlay-screen`): full-viewport fixed overlay, dark translucent background (`rgba(20,40,60,0.72)`) with 4px backdrop blur, `z-index: 100`, flexbox centered content. Hidden by default (`display: none`), shown via `data-screen` attribute on `<body>` (e.g. `[data-screen="select"] #screen-select { display: flex }`).

### 2a. Mode Selection (`#screen-select`)

- **Card (`.overlay-card`):** White (`rgba(255,255,255,0.97)`), 20px border radius, 36px/40px padding, max-width 760px, heavy drop shadow
- **Title:** "World Map Quiz" — 1.6rem, bold 700, dark text, centered, 24px bottom margin
- **Mode cards grid (`.mode-cards`):** 2×2 grid, 16px gap
- **Each mode card (`.mode-card`):** Column flex layout, left-aligned text, light blue-grey background (`#f4f8fc`), 2px border (`#dde6f0`), 12px border radius, 20px padding. Hover: blue tint background (`#e6f0fa`), blue border (`#4a90d9`)
  - **Icon (`.mode-icon`):** Emoji, 1.8rem
  - **Name (`.mode-name`):** 1rem, bold 700, dark text
  - **Description (`.mode-desc`):** 0.82rem, grey text (`#666`)

**Mobile (≤600px):** Mode cards stack to single column. Card padding shrinks to 24px/20px. Title to 1.3rem.

### 2b. Settings Screen (`#screen-settings`)

- **Card:** Same as above but narrow variant (`.overlay-card--narrow`, max-width 420px)
- **Title:** Mode name (e.g. "Find the Country") — same styling as overlay title
- **Settings rows (`.settings-row`):** Flex row, space-between, 12px vertical padding, 1px bottom border (`#eee`)
  - **Label (`.settings-label`):** 0.95rem, bold 600, dark grey (`#333`)
  - **Stepper (`.stepper`):** Flex row with 12px gap
    - **Buttons (`.stepper-btn`):** 32×32px, 8px border radius, grey background (`#f0f0f0`), 1px border, centered text. Hover: darker grey (`#ddd`)
    - **Value (`.stepper-val`):** 1rem, bold 700, min-width 28px, centered
  - **Toggle (`.toggle`):** 44×24px inline-block, custom checkbox
    - **Track (`.toggle-track`):** Full-size, grey (`#ccc`) background, 24px border radius. Checked: blue (`#3a7bd5`)
    - **Knob (`.toggle-track::after`):** 18×18px white circle, 3px inset, slides 20px right when checked. Both transitions: 0.2s
- **Actions (`.settings-actions`):** Flex row, right-aligned, 12px gap, 24px top margin
  - "Back" button (secondary style)
  - "Start Game" button (primary style)

### 2c. Stats Screen (`#screen-stats`)

- **Card:** Narrow variant (max-width 420px)
- **Title:** "Game Over"
- **Stats grid (`.stats-grid`):** 24px bottom margin
  - **Rows (`.stat-row`):** Flex row, space-between, 10px padding, 1px bottom border
    - **Label (`.stat-label`):** Grey (`#555`)
    - **Value (`.stat-value`):** Dark text, bold 600
  - **Score row (`.stat-row--score`):** Larger (1.2rem), bold 700, no bottom border, extra top padding (16px)
- **"Back to Menu" button:** Primary style, full width

---

## 3. Game Panel (`#game-panel`)

- **Position:** Fixed, top 16px, horizontally centered, max-width 860px, `z-index: 10`
- **Layout:** CSS grid — three columns: `auto 1fr auto`, areas: `flag | identity | hud`
- **Padding:** 12px/20px (slightly smaller than info panel)
- **Visibility:** Shown when `data-phase="playing"` or `data-phase="feedback"` on `<body>`, hidden otherwise via CSS.
- **Progress bar (`.game-progress`):** Horizontal bar pinned to the bottom edge of the game panel, inside the border radius. Height ~3px, blue fill (matches primary color), width = `(currentRound / totalRounds) * 100%`. Subtle, does not take up layout space (absolutely positioned). Updates at the start of each round.
- **Contents:**
  - **Flag area (`.panel-flag`, `#game-flag-wrap`):** Auto-width column. Contains `<img>` (64×42px, object-fit cover, 4px border radius, 1px grey border). Hidden via CSS when `data-mode="name-capital"`.
  - **Identity area (`.panel-identity`):** Country name (`#game-prompt`) — 1.1rem, bold 700, dark text. Hidden via CSS when `data-mode="name-country"`.
  - **HUD area (`.game-hud`):** Flex row, 12px gap, nowrap
    - Score and guesses counters (`.hud-item`): 0.9rem, dark grey, value in `<strong>`
    - "Skip" button (secondary small)
    - "Quit" button (danger small)

**Mobile (≤600px):** Snaps to full width, top 0, no transform, flat bottom corners (0 0 16px 16px border radius). Grid collapses to `1fr auto` — flag column hidden entirely. HUD wraps with 8px gap, right-aligned.

---

## 4. Bottom Panel Stack (`.bottom-panels`)

- **Position:** Fixed, bottom 16px, horizontally centered, max-width 860px
- **Layout:** Flex column, 8px gap — feedback bar stacks above whichever content panel is active

### 4a. Feedback Bar (`#feedback-bar`)

- **Style:** Same shared panel transparency (`rgba(255,255,255,0.95)`), 8px backdrop blur, 12px border radius, lighter shadow than panels
- **Layout:** Flex row, space-between, 10px/20px padding, 12px gap
- **Text:** 0.95rem, bold 600, nowrap
  - Correct (`.feedback-bar--correct`): green text (`#1a7a3a`)
  - Wrong (`.feedback-bar--wrong`): red text (`#c03030`)
- **"Next →" button:** Primary small style, right side. Hidden when auto-advance is enabled.
- **Visibility:** Shown when `data-phase="feedback"` on `<body>`, hidden otherwise via CSS.

### 4b. Country Info Panel (`#country-panel`)

- **Layout:** CSS grid — three columns: `auto 1fr 2fr`, areas: `flag | identity | facts`
- **Visibility:** In explore mode, shown/hidden by JS toggling a class when the user hovers/taps a country (no phase change). In quiz modes, shown when `data-phase="feedback"` via CSS.
- **Contents:**
  - **Flag:** 64×42px image, same styling as game panel flag
  - **Identity:**
    - Country name (`.panel-name`): 1.1rem, bold 700, dark
    - Capital (`.panel-capital`): 0.9rem, grey (`#555`), 2px top margin
  - **Facts grid (`.panel-facts`):** 2-column sub-grid, 4px/16px gap
    - Each fact (`.fact`): flex row, space-between, 0.85rem
    - Label (`.fact-label`): grey, nowrap, colon appended via `::after`
    - Value (`.fact-value`): dark, bold 600, right-aligned, nowrap
    - Fields: Area (km²), Population, Highest Point (m), Neighbours (count)

**Mobile (≤600px):** Bottom panels snap to edges (`bottom: 0`, `left/right: 16px`, no centering transform). Country panel stacks to single column: identity → flag → facts. Flag centered, identity centered, facts to single column. Top corners rounded (16px 16px 0 0), bottom corners flat.

### 4c. Text Input Panel (`#input-panel`)

- **Layout:** Flex column, 8px gap
- **Visibility:** Shown when `data-phase="playing"` and mode is `name-country` or `name-capital` via CSS (e.g. `[data-phase="playing"][data-mode="name-country"]`). Hidden otherwise.
- **Contents:**
  - **Inline feedback (`#input-feedback`):** 0.88rem, min-height 1.2em, red text (`#c03030`), bold 600. Shows "Wrong — N guess(es) left" messages.
  - **Input row (`.input-row`):** Flex row, 10px gap, vertically centered
    - **Text input (`.guess-input`):** Flex-grow, 10px/14px padding, 8px border radius, 1.5px grey border, white background, 1rem font. Focus: blue border (`#4a90d9`). Autocomplete/spellcheck disabled.
    - **"Submit" button:** Primary style

**Mobile (≤600px):** Top corners rounded (16px 16px 0 0), bottom flat (sits at screen edge).

---

## 5. Explore Quit Button (`#btn-menu`)

- **Position:** Fixed, top 16px, right 16px, `z-index: 10`
- **Style:** Danger small button (red background, white text, 0.82rem, 6px/12px padding), with drop shadow (`0 2px 8px rgba(0,0,0,0.15)`)
- **Label:** "Quit"
- **Visibility:** Shown when `data-mode="explore"` and `data-phase="idle"` via CSS. Hidden otherwise.

---

## 6. Buttons (`.btn`)

Shared across all UI:

| Variant | Background | Text | Hover |
|---|---|---|---|
| `.btn-primary` | Blue (`#4a90d9`) | White | Darker blue (`#2f72b8`) |
| `.btn-secondary` | Light grey-blue (`#e0e8f0`) | Dark (`#333`) | Darker grey (`#c8d8e8`) |
| `.btn-danger` | Red (`#e05555`) | White | Darker red (`#c03030`) |

- **Base:** No border, 8px border radius, 9px/18px padding, bold 600, 0.9rem, pointer cursor, 0.15s background transition
- **Small (`.btn-sm`):** 0.82rem, 6px/12px padding
