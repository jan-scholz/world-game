# Game Flow

Detailed breakdown of user actions and information displayed at each stage.

---

## 1. Mode Selection Screen

**What the user sees:**
- Full-screen overlay with title "World Map Quiz"
- Four mode cards in a 2×2 grid (single column on mobile):

| Card | Icon | Label | Description |
|---|---|---|---|
| Explore | 🌍 | Explore | "Browse the map and discover facts" |
| Find | 🔍 | Find the Country | "Click the correct country on the map" |
| Name Country | ✏️ | Name the Country | "Type the name of the highlighted country" |
| Name Capital | 🏛️ | Name the Capital | "Type the capital of the shown country" |

**User actions:**
- Click **Explore** → overlays close, map becomes interactive, "Quit" button appears top-right
- Click any quiz mode → proceeds to Settings Screen

---

## 2. Explore Mode

**What the user sees:**
- Full interactive world map (pan & zoom enabled)
- "Quit" button fixed top-right

**User actions:**
- **Hover a country (desktop)** → country path turns orange (`.highlighted`), bottom info panel slides in showing:
  - Flag image (from flagcdn.com)
  - Country name
  - Capital city
  - Facts grid: Area (km²), Population, Highest Point (elevation m), Neighbours (count)
- **Mouse out (desktop)** → highlight removed, info panel hides
- **Tap a country (mobile/touch)** → same highlight and info panel as hover. Tapping a different country switches to it. Tapping the same country or empty area dismisses the panel.
- **Pan/zoom** → scroll wheel or drag to navigate (1×–12× scale)
- **Click "Quit"** → returns to Mode Selection Screen, map zoom resets

---

## 3. Settings Screen (Quiz Modes Only)

**What the user sees:**
- Overlay card titled with the chosen mode name (e.g. "Find the Country")
- Three configurable settings:

| Setting | Control | Range | Default |
|---|---|---|---|
| Rounds | Stepper (−/+) | 1–50 | 10 |
| Guesses per round | Stepper (−/+) | 1–10 | 3 |
| Auto-advance | Toggle switch | on/off | off |

- "Back" button (returns to Mode Selection)
- "Start Game" button

**User actions:**
- Adjust rounds/guesses with stepper buttons
- Toggle auto-advance (when on, rounds advance automatically after 1.8s feedback delay)
- Click **Back** → return to Mode Selection
- Click **Start Game** → overlays close, game begins

---

## 4. Quiz Gameplay — Find the Country

**Round start — what the user sees:**
- **Top game panel** showing:
  - Target country's flag
  - Target country's name
  - Score counter
  - Guesses remaining counter
  - Progress bar along bottom edge of panel (fills left-to-right as rounds complete)
  - "Skip" button
  - "Quit" button
- Map at default zoom (no zoom-to-target, no highlight — that would reveal the answer)

**User actions:**
- **Click a country on the map:**
  - **Correct** → score increments, transitions to Feedback phase
  - **Wrong** → guesses decrement, clicked country flashes red for 600ms (`.wrong-guess`)
  - **Last wrong guess** → transitions to Feedback phase (incorrect)
- **Click "Skip"** → skipped count increments, advances to next round (no feedback shown)
- **Click "Quit"** → immediately goes to Stats Screen

---

## 5. Quiz Gameplay — Name the Country

**Round start — what the user sees:**
- **Top game panel** showing:
  - Target country's flag
  - Country name is **hidden** (that's the answer)
  - Score counter, guesses remaining, progress bar, Skip, Quit
- Map **zooms to the target country** (750ms animation)
- Target country highlighted in blue (`.target`)
- **Bottom input panel** with:
  - Text input (placeholder: "Name the country…")
  - "Submit" button
  - Input auto-focuses after 800ms (waits for zoom animation)

**User actions:**
- **Type answer + press Enter or click Submit:**
  - Input is normalized (trimmed, lowercased, diacritics removed) and looked up in `aliases.json`
  - **Correct** → score increments, transitions to Feedback phase
  - **Wrong, guesses remaining** → red inline message "Wrong — N guess(es) left", input clears, re-focuses
  - **Wrong, no guesses left** → transitions to Feedback phase (incorrect)
- **Click "Skip"** → skipped count increments, advances to next round
- **Click "Quit"** → immediately goes to Stats Screen

---

## 6. Quiz Gameplay — Name the Capital

**Round start — what the user sees:**
- **Top game panel** showing:
  - Flag is **hidden** (flag area collapsed)
  - Target country's **name shown** (the prompt)
  - Score counter, guesses remaining, progress bar, Skip, Quit
- Map **zooms to the target country** (750ms animation)
- Target country highlighted in blue (`.target`)
- **Bottom input panel** with:
  - Text input (placeholder: "Name the capital…")
  - "Submit" button
  - Input auto-focuses after 800ms

**User actions:**
- **Type answer + press Enter or click Submit:**
  - Input is normalized and compared directly against `countries.json` capital field
  - **Correct** → score increments, transitions to Feedback phase
  - **Wrong, guesses remaining** → red inline message "Wrong — N guess(es) left", input clears, re-focuses
  - **Wrong, no guesses left** → transitions to Feedback phase (incorrect)
- **Click "Skip"** → skipped count increments, advances to next round
- **Click "Quit"** → immediately goes to Stats Screen

---

## 7. Feedback Phase (All Quiz Modes)

**What the user sees:**
- Input panel hides
- **Feedback bar** appears above country info panel:
  - Correct: green text "Correct!"
  - Wrong: red text "No more guesses — the answer was {answer}"
    - For Name Capital: answer = capital name
    - For Find/Name Country: answer = country name
- **Country info panel** shows full details (flag, name, capital, area, population, highest point, neighbours)
- Target country highlighted on map (`.target`) and zoomed to — in all modes including Find, so the user sees the country's location

**User actions (auto-advance OFF):**
- **"Next →" button** appears in feedback bar → click to advance to next round
- Button auto-focuses for keyboard accessibility

**Behavior (auto-advance ON):**
- No user action needed — automatically advances after 1.8 seconds
- **"Next →" button** is omitted from feedback bar

**End of rounds:** after the last round's feedback, transitions to Stats Screen instead of next round.

---

## 8. Stats Screen (Game Over)

**What the user sees:**
- Full-screen overlay titled "Game Over"
- Stats summary:

| Stat | Value |
|---|---|
| Rounds played | Total rounds attempted |
| Correct | Number answered correctly |
| Skipped | Number skipped |
| Score | Correct / Rounds played as percentage |

- "Back to Menu" button (full-width)
- Map zoom resets in background (300ms)

**User actions:**
- Click **Back to Menu** → returns to Mode Selection Screen

---

## State Machine Summary

```
Mode Selection ──→ Explore ──→ (Quit) ──→ Mode Selection
       │
       ├──→ Settings ──→ Start Game ──→ Playing ──→ Feedback ──→ Playing ...
       │        │                          │            │
       │        └── Back ──→ Mode Selection │            └── (last round) ──→ Stats
       │                                   │
       │                                   ├── Skip ──→ Playing / Stats
       │                                   └── Quit ──→ Stats
       │
       └── Stats ──→ (Back to Menu) ──→ Mode Selection
```

**Data attributes on `<body>` (drive CSS visibility):**
- `data-phase`: `idle` | `playing` | `feedback`
- `data-mode`: `explore` | `find` | `name-country` | `name-capital`
- `data-screen`: `select` | `settings` | `stats` | (absent — no overlay)

JS sets these attributes on state transitions. CSS attribute selectors determine which panels, overlays, and buttons are visible — no manual per-element show/hide calls needed.
