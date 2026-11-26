#!/usr/bin/env python3
"""
MyPalUSA Navigation Framework Synchronizer
Applies the canonical navigation structure across all HTML files while preserving active states.
"""

import glob
import os
import re

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

def generate_desktop_dropdown(is_active=False):
    active_cls = " active" if is_active else ""
    items_html = "\n".join([
        f'              <a href="{href}" class="nav-dropdown-item simple">{label.replace("&", "&amp;")}</a>'
        for href, label in CANONICAL_SERVICES
    ])
    return f"""        <div class="nav-dropdown-wrapper">
          <a href="installation.html" class="nav-link nav-dropdown-trigger{active_cls}">
            <span>Installation Services</span>
            <svg class="nav-chevron" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor"
              stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </a>
          <div class="nav-dropdown-menu simple-menu">
            <div class="nav-dropdown-header">
              <span class="nav-dropdown-title">RESIDENTIAL INSTALLATION</span>
              <a href="installation.html" class="nav-dropdown-view-all">All Services Hub &rsaquo;</a>
            </div>
            <div class="nav-dropdown-grid simple-list">
{items_html}
            </div>
          </div>
        </div>"""

def generate_mobile_accordion(is_active=False, current_file=""):
    active_summary = ' active' if is_active else ''
    hub_active = ' active' if current_file in ('installation.html', 'installation-service.html') else ''
    
    sublinks = [f'          <a href="installation.html" class="mobile-sublink all-link{hub_active}">All Services Hub &rsaquo;</a>']
    for href, label in CANONICAL_SERVICES:
        item_active = ' active' if current_file == href else ''
        sublinks.append(f'          <a href="{href}" class="mobile-sublink{item_active}"><span>{label.replace("&", "&amp;")}</span></a>')
    
    sublinks_html = "\n".join(sublinks)
    return f"""      <details class="mobile-services-accordion">
        <summary class="mobile-nav-link{active_summary}">
          Installation Services <span class="accordion-arrow">▾</span>
        </summary>
        <div class="mobile-sublinks">
{sublinks_html}
        </div>
      </details>"""

def sync_file(filepath):
    filename = os.path.basename(filepath)
    if filename == "contact.html":
        return

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Determine if this file should have active class on Installation Services
    is_install_active = (
        filename.startswith("service_") or 
        filename in ("installation.html", "installation-service.html")
    )

    # 1. Update Desktop Dropdown
    if filename == "about.html":
        # Replace the flat installation link with full dropdown
        flat_pattern = r'<a href="installation\.html" class="nav-link">Installation Services</a>'
        new_desktop = generate_desktop_dropdown(is_active=False)
        content = re.sub(flat_pattern, new_desktop, content)
    else:
        # Match existing nav-dropdown-wrapper for Installation Services
        # It comes before Home Inspection dropdown
        dropdown_pattern = r'<div class="nav-dropdown-wrapper">\s*<a href="installation\.html"[\s\S]*?RESIDENTIAL INSTALLATION[\s\S]*?</div>\s*</div>\s*</div>'
        new_desktop = generate_desktop_dropdown(is_active=is_install_active)
        content = re.sub(dropdown_pattern, new_desktop, content)

    # 2. Update Mobile Accordion for Installation Services
    if filename == "about.html":
        # Replace flat mobile link with mobile accordion
        flat_mobile_pattern = r'<a href="installation\.html" class="mobile-nav-link">Installation Services</a>'
        new_mobile = generate_mobile_accordion(is_active=False, current_file=filename)
        content = re.sub(flat_mobile_pattern, new_mobile, content)
    else:
        mobile_pattern = r'<details class="mobile-services-accordion">\s*<summary class="mobile-nav-link[^"]*">\s*Installation Services[\s\S]*?</div>\s*</details>'
        new_mobile = generate_mobile_accordion(is_active=is_install_active, current_file=filename)
        content = re.sub(mobile_pattern, new_mobile, content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Synced {filename}")

def main():
    files = sorted(glob.glob(os.path.join(REPO_DIR, "*.html")))
    for f in files:
        sync_file(f)

if __name__ == "__main__":
    main()
