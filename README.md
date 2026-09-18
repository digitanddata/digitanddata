# Tutoring Platform — Project README

## 1. Vision

An independent, teacher-owned tutoring platform for Mathematics and Computer
Science, marketed directly to parents worldwide — no aggregators, no
marketplaces, no middlemen. The website is the digital storefront; the
relationship with each family is built through direct 1:1 outreach and
discovery calls, not algorithmic matching.

**Core differentiators**
- One teacher, full ownership of curriculum, pricing, and relationships
- Global reach across time zones — not tied to one country's market
- Broad curriculum coverage so the site captures search traffic and
  inquiries from any major education system a parent might search for
- A technical-skills wing (programming, data science, robotics, etc.)
  that goes beyond what school tutoring alone offers

## 2. Target audience

- Parents of school-age children (roughly grades 6–12 / ages 11–18)
  following an international, national, or state curriculum
- Expat and international-school families, who are especially active in
  Facebook/WhatsApp parent groups and search heavily for curriculum-specific
  tutors
- Parents seeking enrichment beyond school (programming, robotics, data
  science) regardless of the child's academic curriculum

## 3. Subject & curriculum coverage (broad launch approach)

Launch strategy: **cover the full landscape**, since major boards will drive
the bulk of inquiries, while the long tail of other boards still generates
organic search traffic and fills out the site's authority.

### Mathematics

**International programs**
- IB: PYP, MYP, DP (Applications & Interpretation, Analysis & Approaches)
- Cambridge International: Primary, Lower Secondary, IGCSE, AS & A Level
- Edexcel International (GCSE & A Level)
- Advanced Placement (AP): Calculus AB/BC, Statistics, Precalculus

**National / regional curricula**
- UK: KS1–KS3, GCSE, A-Level (AQA, OCR, Edexcel, WJEC)
- US: Common Core, individual state standards
- Canada: Provincial (Ontario, BC, Alberta, Quebec, etc.)
- Australia: Australian Curriculum, VCE, HSC (NSW), QCE (Queensland)
- Singapore: MOE syllabus, O-Level, Singapore-Cambridge A-Level
- India: CBSE, ICSE, state boards
- New Zealand: NCEA
- UAE / Middle East: MOE curriculum, international-school variants
- Europe: European Baccalaureate, national systems

**Standardized tests / competitive**
- SAT Math, ACT Math
- AMC/AIME and Math Olympiad prep

### Computer Science — school curricula
- IB Computer Science (MYP/DP)
- Cambridge IGCSE & A-Level Computer Science
- AP Computer Science A, AP Computer Science Principles
- GCSE Computer Science (UK)
- CBSE/ICSE Computer Science (India)
- Australian Curriculum – Digital Technologies, VCE Computing
- Singapore O-Level/A-Level Computing
- NCEA Digital Technologies (NZ)

### Computer Science — technical tracks (beyond school syllabus)
- Programming: Python, Java, C++, JavaScript
- Web Development (front-end & back-end basics)
- App Development (Android/iOS basics)
- Data Structures & Algorithms / competitive programming
- Data Science & Machine Learning
- Robotics: Arduino, Raspberry Pi, LEGO Mindstorms/Spike
- Game Development: Scratch, Unity/Unreal basics
- Cybersecurity fundamentals
- Databases & SQL
- Cloud computing basics

## 4. Technology stack

| Layer | Choice |
|---|---|
| Backend framework | Python + Django |
| Database | MySQL |
| Hosting (Phase 1) | GoDaddy Linux (shared) hosting via cPanel "Setup Python App" (Passenger) |
| Hosting (Phase 2) | GoDaddy VPS / Dedicated hosting, once traffic/revenue justifies it |
| Static/media files | WhiteNoise (shared hosting has no separate app server) |
| DB driver | PyMySQL (pure Python — avoids compiling `mysqlclient` on shared hosting) |
| Forms | Django forms / django-crispy-forms |
| Admin | Django's built-in admin — used to manage curricula, tracks, and leads without touching code |

**Known constraint**: GoDaddy's shared Linux hosting does not officially
support Django (no `mod_wsgi`, no root access); it works via cPanel's
Python App (Passenger) feature but is community-documented, not
GoDaddy-supported. This is an acceptable trade-off for Phase 1 given the
cost savings, with a clear upgrade path to VPS/Dedicated hosting in Phase 2.

See [DEPLOYMENT.md](DEPLOYMENT.md) for the full GoDaddy setup guide and the
repeatable push-to-deploy workflow.

## 5. Website structure (Django apps)

```
tutoring_platform/
├── manage.py
├── passenger_wsgi.py          # GoDaddy Passenger entry point
├── requirements.txt
├── .env                       # DB credentials, secret key
├── tutoring_platform/         # project settings, urls, wsgi
├── core/                      # home, about, pricing, testimonials
├── mathematics/               # Curriculum model + views (all Math boards)
├── computer_science/          # Curriculum model (CS boards) + TechnicalTrack model
├── leads/                     # Lead + Booking models, contact/booking forms
├── templates/                 # shared base.html + per-app templates
└── static/                    # CSS/JS
```

Curricula and technical tracks live in the database (not hardcoded
templates), so adding a new board later — e.g. a country not on the
initial list — is a data entry via Django admin, not a code change.

## 6. Sitemap

```
/                                   Home
/mathematics/                       Math hub — full curriculum list, grouped
                                     by International / National / Tests
/mathematics/<board-slug>/          Per-board detail page (e.g. /mathematics/ib/)
/computer-science/                  CS hub — school curricula + technical tracks
/computer-science/<board-slug>/     Per-board detail page (school curricula)
/computer-science/<track-slug>/     Technical track detail page
                                     (e.g. /computer-science/robotics/)
/about/                             Tutor bio, credentials, teaching philosophy
/pricing/                           Pricing structure, packages
/testimonials/                      Parent/student testimonials
/contact/                           General inquiry form
/book-a-call/                       Discovery-call lead capture form
```

Future additions (not in initial launch): `/blog/` for SEO content,
`/resources/` for free downloadable materials (lead magnets).

## 7. Content model (database entities)

- **Curriculum** — subject (Math/CS), board name, category (International /
  National / Test-prep), level range, summary, syllabus outline
- **TechnicalTrack** — title, summary, syllabus outline, target age range
- **Lead** — every inquiry: parent name, email, WhatsApp, child's subject/
  curriculum/level, message, source page, timestamp
- **Booking** — discovery call requests linked to a Lead: requested time,
  timezone, status
- **Testimonial** — parent/student name, quote, curriculum tag

## 8. Marketing strategy — step by step (direct-to-parent, no aggregators)

### Step 1 — Foundation content (Weeks 1–4)
- Publish all curriculum/track pages with real (not placeholder) content,
  written for parent search intent: "IB Math tutor," "AP Computer Science A
  tutor," "Singapore Math tutor online," etc.
- Set up Google Business Profile and social profiles (Instagram, Facebook,
  LinkedIn, YouTube) under one consistent brand name.
- Write 3–5 founding blog posts targeting long-tail parent searches
  (e.g. "IB Math AA vs AI — which should my child choose?").

### Step 2 — Direct network outreach (Weeks 3–8, overlapping)
- Join expat/international-school parent groups on Facebook and WhatsApp
  relevant to the curricula you cover; contribute genuinely before pitching.
- Reach out personally to your existing network — former students' parents,
  colleagues, school community — with a clear, low-pressure offer of a free
  discovery call.
- Offer a limited number of discounted "founding family" slots in exchange
  for a testimonial and referral.

### Step 3 — Content-led SEO & short-form video (Weeks 6 onward, ongoing)
- Weekly short-form videos (Reels/Shorts/TikTok) explaining one tricky
  concept per board (e.g. "AP Calc related rates in 60 seconds").
- Publish one long-form blog post per week tied to a specific curriculum
  pain point — this is what search engines index and what parents find
  months later with zero ongoing ad spend.
- Cross-post video content to YouTube for long-term searchability.

### Step 4 — Lead capture & nurture (Weeks 8–12)
- Build a lead magnet: a "curriculum readiness checklist" or short
  diagnostic PDF per subject, gated behind the `/contact/` or `/book-a-call/`
  form.
- Set up an email/WhatsApp nurture sequence for anyone who submits a lead
  but doesn't book immediately.
- Track every lead's source page in the database (already modeled) to see
  which curriculum pages actually convert — double down on what works.

### Step 5 — Referral engine (Month 3 onward)
- After the first 5–10 paying families, explicitly ask for referrals —
  international/expat parent networks are small and tightly connected, so
  word-of-mouth compounds fast.
- Offer a modest referral incentive (a free session, or discount) to both
  referrer and new family.

### Step 6 — Scale marketing spend deliberately (Month 4+)
- Only once organic channels show which curricula/tracks convert best,
  consider small paid campaigns (Meta/Google Ads) targeting those specific
  segments — avoid broad, unfocused ad spend early.
- Reinvest revenue into either more content production or bringing on a
  second teacher for overflow subjects.

## 9. Build & launch roadmap

| Phase | Timeline | Focus |
|---|---|---|
| 1 | Month 1 | Django site built, deployed to GoDaddy shared hosting, all curriculum pages live |
| 2 | Month 1–2 | Content written for major boards first (IB, Cambridge, AP, UK, US, Canada), then remaining boards |
| 3 | Month 2–3 | Marketing Steps 1–3 executed; first leads captured |
| 4 | Month 3–4 | First paying families onboarded; testimonials collected |
| 5 | Month 4–6 | Referral engine active; evaluate traffic/leads by curriculum page to guide content priority |
| 6 | Month 6+ | Evaluate hosting needs — migrate to GoDaddy VPS/Dedicated if shared hosting shows performance or reliability limits |
