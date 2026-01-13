# UI Preview - Structural Drawing Analysis Platform

## Visual Design Overview

### Color Palette (Industrial Theme)

**Primary Colors:**
- Industrial Blue: `#5778a0` (buttons, accents)
- Steel Gray: `#677891` (secondary elements)
- Dark Industrial: `#2c394e` (headers, footer)

**Background Colors:**
- Light: `#f5f7fa` (page background)
- White: `#ffffff` (cards, content areas)

**Accent Colors:**
- Success Green: `#10b981` (completed states)
- Warning Red: `#ef4444` (errors)

---

## Page Sections

### 1. Hero Section
```
┌─────────────────────────────────────────────────────────────┐
│                                                               │
│         [Dark gradient background: Navy to Steel]             │
│                                                               │
│              Structural Drawing Analysis Platform             │
│                                                               │
│      AI-Powered Tendon Detection and Analysis for            │
│                  Construction Plans                           │
│                                                               │
│     Upload your PDF structural drawings and let our           │
│     advanced computer vision system automatically detect      │
│     and analyze tendons with precision and speed.             │
│                                                               │
│                   [ Get Started Button ]                      │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │     🔍      │  │      ⚡      │  │     📊      │          │
│  │ Advanced    │  │    Fast      │  │  Detailed   │          │
│  │    OCR      │  │ Processing   │  │   Results   │          │
│  │             │  │              │  │             │          │
│  │ State-of... │  │ GPU-accel... │  │ Comprehen...│          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

**Features:**
- Large, bold title in white
- Gradient background (dark industrial colors)
- Three feature cards with icons
- Prominent CTA button with hover effects
- Smooth scroll to upload section

---

### 2. File Upload Section
```
┌─────────────────────────────────────────────────────────────┐
│                                                               │
│              Upload Your PDF Drawing                          │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                                                         │  │
│  │                        📄                               │  │
│  │                                                         │  │
│  │          Drag and drop your PDF file here              │  │
│  │                                                         │  │
│  │                        or                               │  │
│  │                                                         │  │
│  │                 [ Browse Files ]                        │  │
│  │                                                         │  │
│  │          Supported format: PDF (max 50MB)              │  │
│  │                                                         │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  [When file selected:]                                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  📋  plan.pdf                    [ Upload & Process ]  │  │
│  │      2.45 MB                                           │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

**Features:**
- Dashed border drag-and-drop zone
- Changes color on drag hover
- File validation (PDF only, size limit)
- Selected file preview with size
- Upload button appears after selection

---

### 3. Processing Status Section
```
┌─────────────────────────────────────────────────────────────┐
│                                                               │
│              Processing Your Document                         │
│                                                               │
│                      [Spinning Loader]                        │
│                                                               │
│  Processing page 3 of 12...                      75%         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░│  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│              Processing page 3 of 12                          │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  ✅ Upload  │  │ 🔍 Analysis │  │ ✨ Complete │          │
│  │             │  │             │  │             │          │
│  │File received│  │OCR & Detect │  │Results ready│          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│   [Green border]   [Green border]   [Gray border]            │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

**Features:**
- Animated spinner during processing
- Progress bar with percentage
- Current page indicator
- Three-step visual progress
- Real-time status messages
- Auto-updates every 2 seconds

---

### 4. Results Display Section
```
┌─────────────────────────────────────────────────────────────┐
│                                                               │
│  Analysis Complete                [ Download All ] [ New ]   │
│  Successfully processed 12 pages                              │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │     📄      │  │      ✅      │  │     🎯      │          │
│  │     12      │  │      12      │  │    100%     │          │
│  │   Pages     │  │   Results    │  │  Success    │          │
│  │  Processed  │  │  Generated   │  │    Rate     │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
│                                                               │
│  Annotated Drawings                                           │
│                                                               │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ [Image] │  │ [Image] │  │ [Image] │  │ [Image] │        │
│  │         │  │         │  │         │  │         │        │
│  │ Page 1  │  │ Page 2  │  │ Page 3  │  │ Page 4  │        │
│  │[Download]│ │[Download]│ │[Download]│ │[Download]│        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
│                                                               │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ [Image] │  │ [Image] │  │ [Image] │  │ [Image] │        │
│  │         │  │         │  │         │  │         │        │
│  │ Page 5  │  │ Page 6  │  │ Page 7  │  │ Page 8  │        │
│  │[Download]│ │[Download]│ │[Download]│ │[Download]│        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

**Features:**
- Statistics cards with icons
- Responsive grid layout (3 columns on desktop)
- Thumbnail previews of results
- Individual download buttons
- Click to view full-size image
- "Download All" button
- "New Upload" button to restart

---

### 5. Footer
```
┌────────────────────────────────────────────────────────────────────────┐
│                                                                        │
│   © 2026 Structural Drawing Analysis Platform. Powered by Truestack AI │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

**Features:**
- Dark industrial background
- Centered text
- Minimal, professional

---

## Responsive Behavior

### Desktop (1024px+)
- Full-width hero section
- 3-column feature grid
- 3-column results grid
- Side-by-side layouts

### Tablet (768px - 1023px)
- 2-column grids
- Stacked layouts where needed
- Adjusted padding

### Mobile (< 768px)
- Single column layouts
- Stacked feature cards
- Full-width buttons
- Optimized touch targets

---

## Interactions & Animations

1. **Hover Effects:**
   - Buttons: Darken + shadow increase + slight lift
   - Result cards: Border color change + scale up
   - Upload zone: Background color change

2. **Transitions:**
   - All color changes: 200ms ease
   - Transform effects: 300ms ease
   - Progress bar: 500ms ease-out

3. **Loading States:**
   - Spinning loader animation
   - Pulsing progress bar
   - Disabled button states

4. **Smooth Scrolling:**
   - "Get Started" button scrolls to upload
   - Smooth page transitions

---

## Accessibility Features

- ✅ Semantic HTML
- ✅ ARIA labels where needed
- ✅ Keyboard navigation support
- ✅ High contrast text
- ✅ Focus indicators
- ✅ Responsive font sizes

---

**The UI is modern, professional, and perfectly suited for an industrial/construction platform!** 🏗️

