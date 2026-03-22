# 🏀 Basketball Cinematic — AI Generation Prompts

> תהליך: תמונה (start frame) → תמונה (end frame) → וידאו בKling 3.0
> כל שחקן = 2 תמונות + וידאו אחד של 5-6 שניות

---

## ⚙️ הגדרות אחידות לכל התמונות (NanoBanana / ComfyUI / Gemini)

```
Style: Cinematic NBA photography, ultra-realistic, shot on RED camera
Lighting: Dramatic single spotlight from above-front, deep shadows, volumetric light rays in arena smoke
Background: Blurred NBA arena bokeh, out-of-focus crowd lights, atmospheric haze
Shot type: Full body, low angle (shooting from knee height), slight dutch tilt 3°
Color grading: Dark and moody, deep shadows, high contrast, desaturated midtones
Resolution: 1920x1080 (16:9 landscape)
Negative prompt: cartoon, illustration, anime, text, watermark, logo, blurry face, multiple players
```

---

## 🟡🟣 Player 1 — LeBron James (Lakers)

**Colors:** Deep purple `#3a1462` + Gold `#FDB927`

### 📸 Start Frame (static pose)
```
Ultra-realistic NBA player wearing Los Angeles Lakers purple and gold uniform #23,
standing tall with ball in right hand held at chest height,
powerful athletic build, intense focused expression looking forward,
dramatic spotlight from above casting strong shadows,
dark purple and gold bokeh arena background,
cinematic color grade — deep shadows, warm gold rim light from behind,
low angle full body shot, slight dutch tilt,
photorealistic, 8K detail, shot on RED camera, f/2.8 shallow depth of field
```

### 📸 End Frame (action pose)
```
Ultra-realistic NBA player wearing Los Angeles Lakers purple and gold uniform #23,
mid-air dunking motion — right arm fully extended above the rim,
body slightly twisted, explosive athletic power,
dramatic motion blur on crowd background,
golden rim light from behind creating silhouette halo effect,
dark purple arena atmosphere, smoke particles in spotlight beam,
low angle full body shot looking up at player,
photorealistic, 8K detail, shot on RED camera
```

### 🎬 Kling 3.0 Video Prompt
```
Slow motion cinematic NBA dunk sequence:
Player in Lakers purple #23 starts at left edge of frame holding ball,
takes one explosive step forward, rises off the ground in powerful slow motion,
arm reaches up toward imaginary rim at top right of frame,
spotlight follows the motion, gold rim light glows behind,
deep purple smoke and bokeh arena in background,
camera stays LOW AND FIXED — player moves left to right through frame,
5 seconds duration, 24fps cinematic look, no camera movement,
end on peak of dunk with arm fully extended
```

---

## 💛🔵 Player 2 — Stephen Curry (Warriors)

**Colors:** Navy blue `#0d2b6b` + Gold `#FFC72C`

### 📸 Start Frame
```
Ultra-realistic NBA player wearing Golden State Warriors blue and gold uniform #30,
crouched in triple-threat position, ball in both hands near right hip,
sharp focused eyes, slight smirk of confidence,
dramatic spotlight from above, deep blue arena atmosphere,
navy and gold bokeh background with distant crowd lights,
cinematic color grade — cold blue shadows, warm yellow-gold accents,
low angle full body shot, photorealistic, 8K, shot on RED camera
```

### 📸 End Frame
```
Ultra-realistic NBA player wearing Golden State Warriors blue and gold uniform #30,
follow-through pose after releasing 3-point shot — right arm extended upward,
wrist snapped down, fingers spread, head tilted back watching the shot,
confident triumphant expression,
arena lights creating golden halo around silhouette,
navy blue bokeh crowd background, warm spotlight beam,
low angle full body shot, photorealistic, 8K, shot on RED camera
```

### 🎬 Kling 3.0 Video Prompt
```
Slow motion cinematic 3-point shot sequence:
Warriors player #30 in blue and gold starts at left of frame in shooting stance,
rises up in fluid slow motion — ball travels from hip to above head,
wrist flicks at peak, perfect shooting form,
spotlight creates golden halo as arm reaches highest point,
navy blue arena fades in background, subtle crowd motion blur,
camera stays LOW AND FIXED — motion flows left to right,
5-6 seconds duration, 24fps cinematic grade,
end on full follow-through pose held for 1 second
```

---

## 🟢⚪ Player 3 — Jayson Tatum (Celtics)

**Colors:** Forest green `#003d1a` + Light green `#A8D08D`

### 📸 Start Frame
```
Ultra-realistic NBA player wearing Boston Celtics green and white uniform #0,
standing in low defensive stance, knees bent, arms wide, intense concentration,
deep forest green arena atmosphere, dramatic overhead spotlight,
green-tinted bokeh arena background, faint crowd lights,
cinematic color grade — cold deep greens, high contrast,
low angle full body shot, photorealistic, 8K, shot on RED camera
```

### 📸 End Frame
```
Ultra-realistic NBA player wearing Boston Celtics green and white uniform #0,
explosive crossover step — body leaning hard left, ball switching hands near floor,
one foot planted, other lifting, athletic power motion,
green arena lighting, spotlight beam highlights face and shoulders,
bokeh crowd background with green-tinted arena glow,
motion energy in the frame, low angle full body,
photorealistic, 8K, shot on RED camera, slight motion blur on extremities
```

### 🎬 Kling 3.0 Video Prompt
```
Slow motion cinematic crossover drive sequence:
Celtics player #0 in green and white starts at left frame facing forward,
explosive crossover dribble — ball drops low, body shifts with power,
drives forward and right in one fluid athletic motion,
deep green spotlights illuminate the move, dramatic shadows,
arena atmosphere fades dark in background,
camera stays LOW AND FIXED — player explodes from left to right,
5-6 seconds duration, 24fps cinematic grade,
slow motion 40% speed, end on mid-drive stride pose
```

---

## 📐 הגדרות וידאו לעריכה ב-CapCut

```
Resolution: 1920x1080
Frame rate: 24fps (cinematic look)
Duration per clip: 5-6 seconds
Bitrate: Medium (5-8 Mbps) — balance quality/performance for web
Format: MP4, H.264
Color space: Rec.709
No audio needed (site has ambient feel)
```

### שמות קבצים לאתר:
```
videos/lebron.mp4
videos/curry.mp4
videos/tatum.mp4
```

---

## ✅ Checklist לפני פיתוח

- [ ] תמונת start frame ל-LeBron
- [ ] תמונת end frame ל-LeBron
- [ ] וידאו lebron.mp4 (5-6 שניות, מתחת ל-8MB)
- [ ] תמונת start frame ל-Curry
- [ ] תמונת end frame ל-Curry
- [ ] וידאו curry.mp4
- [ ] תמונת start frame ל-Tatum
- [ ] תמונת end frame ל-Tatum
- [ ] וידאו tatum.mp4
- [ ] הכנס קבצים לתיקייה `videos/`
- [ ] פתח `index.html` — האפקטים נכנסים אוטומטית!
