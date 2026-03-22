# Basketball Cinematic - Project Memory

## Architecture: "Frozen Frame + Transition Video"

### Core Concept
- Each player scene = **first frame of a video, frozen** (paused at currentTime=0)
- Click right = **video plays** (showing cinematic transition like a ball pass)
- Video ends = **next player's info appears** (2 seconds before video ends)
- Click left = **reverse video plays** (separate MP4, not browser reverse)

### Key Technical Decisions

#### 1. Video as Background (not separate layer)
- Single `<video id="bg-video">` element, always visible, `object-fit: cover`
- `src` set directly in HTML for first player (avoids race condition with JS `load()`)
- `preload="auto"` ensures first frame shows immediately
- Bokeh canvas behind video as fallback when no video loaded

#### 2. Transition System
- `transitions` object maps `"FROM-TO"` keys to video paths
- Forward: `"0-1": "videos/present1123-1.mp4"`
- Reverse: `"1-0": "videos/labron dani reverse.mp4"`
- If no transition video exists, falls back to GSAP slide animation

#### 3. Video End Detection (Polling, not events)
- `onended` event is unreliable in some browsers/environments
- Solution: `pollForEnd()` checks every 100ms if `currentTime >= duration - 0.1`
- When detected: pause video, cleanup state

#### 4. Early Info Display (2s before end)
- `showPlayerInfoEarly()` uses `setTimeout` based on `(duration - 2) * 1000`
- Player info animates in with staggered GSAP:
  - Content container: fade + slide up (0.7s)
  - Player name: fade + slide from left (0.6s, delay 0.1)
  - Team badge: fade + scale bounce (0.4s, delay 0.2)
  - Accent line: width grow from 0 (0.5s, delay 0.25)
  - Position: fade in (0.4s, delay 0.35)

### Critical Bugs Fixed

#### Bug 1: Video not showing on init
- **Cause**: Setting `bgVideo.src` via JS after page load had race condition
- **Fix**: Put `src` directly in HTML `<video>` tag

#### Bug 2: `finishTransition` crashing silently
- **Cause**: `targetPrimary` (bokeh variable) declared with `let` AFTER `setColors` was called
- **Error**: `Cannot access 'targetPrimary' before initialization` (TDZ)
- **Fix**: Move bokeh color state (`primaryRGB`, `targetPrimary`, `hexToRgb`, etc.) to TOP of script, before any function calls
- **Why it wasn't obvious**: Initial HTML had LeBron's data hardcoded, so page looked fine even when INIT crashed

#### Bug 3: GSAP animation conflicts
- **Cause**: `gsap.to(content, { opacity: 0 })` conflicted with `gsap.fromTo(content, { opacity: 1 })`
- **Fix**: Use `gsap.killTweensOf(content)` before new animations, or use `content.style.opacity` directly

#### Bug 4: play().catch() calling playFallback
- **Cause**: When video autoplay failed, `playFallback` started a GSAP timeline that conflicted with `finishTransition`
- **Fix**: In catch, call `finishTransition()` directly instead of `playFallback()`

### File Structure
```
basketball-cinematic/
  index.html                          # Single-file app (HTML + CSS + JS)
  videos/
    present1123-1.mp4                 # LeBron -> Deni (forward transition)
    labron dani reverse.mp4           # Deni -> LeBron (reverse transition)
    [future] deni-to-curry.mp4
    [future] curry-to-deni-reverse.mp4
    [future] curry-to-lebron.mp4
    [future] lebron-to-curry-reverse.mp4
  PROMPTS.md                          # Kling/ComfyUI prompts for video creation
  .claude/
    MEMORY.md                         # This file
```

### Video Creation Workflow (Kling 3.0)
1. Create **Start Frame** image (player A in team uniform, holding ball)
2. Create **End Frame** image (player B in their uniform, receiving ball)
3. Feed to Kling: Start → End, 5 seconds, 24fps
4. Export from CapCut: H.264, 1080p, 24fps, 4-6Mbps, MP4
5. Target: each video < 8MB

### Player Data
| # | Player | Team | Number | Primary | Secondary |
|---|--------|------|--------|---------|-----------|
| 0 | LeBron James | LA Lakers | 23 | #3a1462 | #FDB927 |
| 1 | Deni Avdija | Portland Trail Blazers | 8 | #5a0a0a | #E03A3E |
| 2 | Stephen Curry | Golden State Warriors | 30 | #0d2b6b | #FFC72C |

### Future: Converting to Skill
This project should become a reusable skill that:
1. Accepts a THEME (basketball, cars, fashion, etc.)
2. Accepts ITEMS (players, cars, outfits) with name, subtitle, colors
3. Generates the HTML with transition architecture
4. Generates Kling prompts for transition videos
5. Handles forward + reverse videos
6. Early info display with staggered GSAP animations
