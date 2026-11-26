#!/usr/bin/env python3
"""
MyPalUSA Navigation Framework Validator
Ensures navigation consistency, standardized hub links, and 1:1 desktop-mobile parity across all HTML files.
"""

import glob
import os
import re
import sys

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Canonical 12 services in exact order
CANONICAL_SERVICES = [
    ("service_blinds.html", "Custom Blinds Installation"),
    ("service_ceiling_fans.html", "Ceiling Fan Installation & Wiring"),
    ("service_tv_mounting.html", "TV Wall Mounting"),
    ("service_furniture_assembly.html", "Furniture Assembly & Build"),
    ("service_curtains.html", "Curtains & Custom Drapery Rods"),
    ("service_smart_switches.html", "Smart Switches & Automation"),
    ("service_thermostats.html", "Smart Thermostats"),
    ("service_smart_locks.html", "Smart Locks & Keyless Entry"),
    ("service_garage_door.html", "Smart Garage Door Openers"),
    ("service_garage_shelves.html", "Garage Ceiling Storage Racks"),
    ("service_garbage_disposal.html", "Garbage Disposal Installation"),
    ("service_smart_hubs.html", "Smart Hubs & Whole-Home Scenes"),
]

EXCLUDED_FILES = {"contact.html"}

def validate_file(filepath):
    filename = os.path.basename(filepath)
    if filename in EXCLUDED_FILES:
        return True, ["Excluded (Redirect)"]

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    errors = []

    # 1. Check site-navbar presence
    if '<header class="site-navbar">' not in content:
        errors.append("Missing <header class=\"site-navbar\">")
        return False, errors

    # 2. Check Residential Installation dropdown header
    header_match = re.search(r'<div class="nav-dropdown-header">\s*<span class="nav-dropdown-title">RESIDENTIAL INSTALLATION</span>([\s\S]*?)</div>', content)
    if not header_match:
        errors.append("Missing RESIDENTIAL INSTALLATION header block")
    else:
        header_content = header_match.group(1)
        if 'nav-dropdown-view-all' not in header_content or 'All Services Hub' not in header_content:
            errors.append("Missing '<a href=\"installation.html\" class=\"nav-dropdown-view-all\">All Services Hub &rsaquo;</a>' in header")

    # 3. Check simple-list desktop items
    list_match = re.search(r'<div class="nav-dropdown-grid simple-list">([\s\S]*?)</div>', content)
    if not list_match:
        errors.append("Missing <div class=\"nav-dropdown-grid simple-list\">")
    else:
        grid_html = list_match.group(1)
        for href, label in CANONICAL_SERVICES:
            # Check href exists
            if f'href="{href}"' not in grid_html:
                errors.append(f"Desktop grid missing href '{href}'")
            # Check label exists (normalize HTML entities and spaces)
            norm_grid = re.sub(r'\s+', ' ', grid_html.replace('&amp;', '&'))
            if label not in norm_grid:
                errors.append(f"Desktop grid missing or mismatched label '{label}' for '{href}'")

    # 4. Check mobile accordion
    mobile_match = re.search(r'<details class="mobile-services-accordion">[\s\S]*?Installation Services[\s\S]*?<div class="mobile-sublinks">([\s\S]*?)</div>\s*</details>', content)
    if not mobile_match:
        errors.append("Missing Installation Services mobile-services-accordion")
    else:
        mobile_html = mobile_match.group(1)
        if 'All Services Hub' not in mobile_html:
            errors.append("Missing standard 'All Services Hub &rsaquo;' link in mobile accordion")
        if 'All Services Overview' in mobile_html:
            errors.append("Legacy 'All Services Overview' found - must be standardized to 'All Services Hub &rsaquo;'")

        for href, label in CANONICAL_SERVICES:
            if f'href="{href}"' not in mobile_html:
                errors.append(f"Mobile accordion missing href '{href}'")

    return len(errors) == 0, errors

def main():
    html_files = sorted(glob.glob(os.path.join(REPO_DIR, "*.html")))
    total = 0
    passed = 0
    failed = 0

    print("=" * 70)
    print("MyPalUSA Navigation Framework Validation")
    print("=" * 70)

    for f in html_files:
        name = os.path.basename(f)
        if name in EXCLUDED_FILES:
            continue
        total += 1
        ok, msgs = validate_file(f)
        if ok:
            passed += 1
            print(f"[PASS] {name}")
        else:
            failed += 1
            print(f"[FAIL] {name}:")
            for m in msgs:
                print(f"       - {m}")

    print("=" * 70)
    print(f"Summary: {passed}/{total} passed, {failed} failed.")
    print("=" * 70)
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
