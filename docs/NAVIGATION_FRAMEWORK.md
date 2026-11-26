# MyPalUSA Navigation Framework & Standards Guide

This document establishes the architecture, standards, and **Thumb Rules** governing the site-wide navigation system across all HTML pages in MyPalUSA.

---

## 1. Core Architecture Principles

1. **Framework-Driven Consistency**: Every user-facing page shares an identical navigation hierarchy, naming convention, and markup structure.
2. **Desktop & Mobile Parity**: Any destination accessible via the desktop dropdown must be accessible in the mobile navigation drawer.
3. **Automated Verification**: Navigation integrity is protected by automated synchronization (`scripts/sync_nav.py`) and strict validation (`scripts/validate_nav.py`).

---

## 2. Mandatory "Thumb Rules"

### Rule 1: Standardized Dropdown Header
Every service category dropdown header **must** feature both the category section title (e.g., `RESIDENTIAL INSTALLATION`) and a direct right-aligned link to the category Hub (`All Services Hub ›` pointing to `installation.html`).

```html
<div class="nav-dropdown-header">
  <span class="nav-dropdown-title">RESIDENTIAL INSTALLATION</span>
  <a href="installation.html" class="nav-dropdown-view-all">All Services Hub &rsaquo;</a>
</div>
```

### Rule 2: Unified Wording Standard
- **Always use**: `All Services Hub &rsaquo;`
- **Never use**: `All Services Overview`, `View All Services`, `All Services`, or custom variations.
- **Entity**: Use `&rsaquo;` for the trailing chevron arrow.

### Rule 3: Mobile Accordion Parity
The mobile navigation accordion under `Installation Services` must begin with the direct Hub link as the very first sublink before the individual service items:

```html
<div class="mobile-sublinks">
  <a href="installation.html" class="mobile-sublink all-link">All Services Hub &rsaquo;</a>
  <a href="service_blinds.html" class="mobile-sublink"><span>Custom Blinds Installation</span></a>
  <!-- Remaining 11 canonical services -->
</div>
```

### Rule 4: Canonical 12-Service Sequence
All service links must appear in this exact order across both desktop grids and mobile accordions:
1. `service_blinds.html` — Custom Blinds Installation
2. `service_ceiling_fans.html` — Ceiling Fan Installation & Wiring
3. `service_tv_mounting.html` — TV Wall Mounting
4. `service_furniture_assembly.html` — Furniture Assembly & Build
5. `service_curtains.html` — Curtains & Custom Drapery Rods
6. `service_smart_switches.html` — Smart Switches & Automation
7. `service_thermostats.html` — Smart Thermostats
8. `service_smart_locks.html` — Smart Locks & Keyless Entry
9. `service_garage_door.html` — Smart Garage Door Openers
10. `service_garage_shelves.html` — Garage Ceiling Storage Racks
11. `service_garbage_disposal.html` — Garbage Disposal Installation
12. `service_smart_hubs.html` — Smart Hubs & Whole-Home Scenes

### Rule 5: Active State Management
- When the visitor is on an installation page (`installation.html`, `installation-service.html`, or any `service_*.html`), the parent desktop trigger `<a href="installation.html" class="nav-link active nav-dropdown-trigger">` and mobile summary `<summary class="mobile-nav-link active">` receive the `active` class.
- On the Hub pages (`installation.html`), the Hub link receives `class="mobile-sublink all-link active"`.
- On a specific service page (e.g. `service_blinds.html`), that specific mobile link receives `class="mobile-sublink active"`.

---

## 3. Automation Tools

Whenever navigation links, service titles, or routes are modified:

1. **Synchronize across all pages**:
   ```bash
   python3 scripts/sync_nav.py
   ```
   *Propagates the canonical navigation template and updates all 20 pages while preserving contextual active states.*

2. **Validate site-wide compliance**:
   ```bash
   python3 scripts/validate_nav.py
   ```
   *Audits all 20 HTML files against the thumb rules, verifying headers, view-all links, and canonical item ordering.*
