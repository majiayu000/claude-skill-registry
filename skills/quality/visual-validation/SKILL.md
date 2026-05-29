# Visual Validation Skill

**Use when:** Assessing visual polish, validating game appearance, or claiming visual work is complete

**Required for:** Phase 8+ visual work, UI polish, asset integration

---

## The Rule

> **Visual quality can ONLY be assessed from actual rendered game screenshots. Never from asset files alone.**

---

## Why This Matters

### Real Example (2026-01-28)

All sprite assets were marked "production quality" but screenshots revealed:
- Grass texture used **dithering** (violates style guide)
- Scylla Cove and Sacred Grove looked **identical**
- Locations lacked atmospheric differentiation

The assets were fine. The **rendered game** had problems.

---

## Required Screenshot Sources

### ✅ VALID Sources

| Method | How | When to Use |
|--------|-----|-------------|
| **Papershot** | Press F12 in-game | Manual capture during testing |
| **Levelshot** | Godot Editor → Levelshot tab | Batch capture multiple scenes |
| **MCP Runtime** | `execute_editor_script` with viewport capture | Automated testing |
| **Exported Build** | Screenshot of actual exported .exe/.apk | Final validation |

### ❌ INVALID Sources

| Source | Why Invalid |
|--------|-------------|
| Asset files (.png, .tscn) | Don't show in-game appearance |
| Godot Editor screenshots | Shows IDE chrome, not game |
| Sprite previews | No context, no lighting |
| Code analysis | Can't judge visual composition |

---

## Required Screenshots by Phase

### Phase 8: Visual Polish

**Must capture:**
1. World scene (overview)
2. World scene (close-up with player)
3. Scylla Cove
4. Sacred Grove
5. House interior
6. Dialogue UI active
7. Inventory open
8. Minigame (any)

### Phase 9: Export Testing

**Must capture:**
1. Main menu (from exported build)
2. Gameplay (from exported build)
3. All locations (from exported build)

---

## Validation Checklist

Before claiming visual work complete:

- [ ] All required screenshots captured
- [ ] Screenshots show rendered game (not editor)
- [ ] File sizes differ (identical files = bug)
- [ ] Content matches filename
- [ ] Locations visually distinct
- [ ] No style guide violations visible

---

## Common Bugs

| Bug | Check | Fix |
|-----|-------|-----|
| Duplicate images | `ls -la temp/screenshots/` - check file sizes | Verify scene loading, fix transitions |
| Black screenshots | Image is solid black | Check lighting, camera position |
| Wrong scene | world.png shows menu | Verify scene path in capture code |
| Editor chrome | Shows Godot IDE | Use --headless or game build |

---

## Quick Capture Commands

### Papershot (In-Game)
```
Run game → Press F12 → Check temp/screenshots/
```

### MCP Runtime
```bash
npx -y godot-mcp-cli execute_editor_script \
  --script "get_viewport().get_texture().get_image().save_png('res://temp/screenshots/capture.png')"
```

### Levelshot (Editor)
```
Godot Editor → Levelshot tab → Select scenes → Capture All
```

---

## Visual Development Targets

**Before doing visual work, study the targets:**

📁 `docs/reference/visual_targets/`

| Image | Shows | Key Takeaways |
|-------|-------|---------------|
| `harvest_moon_full_map.png` | World scene target | Warm grass, organic paths, detailed buildings |
| `harvest_moon_crops.jpg` | Farm area target | Textured soil, clear crops, natural layout |
| `stardew_valley_building.jpg` | Building target | Architectural detail, vegetation integration |

**Current vs Target:**
- ❌ Current: Dithered grass, gray box paths, plain buildings
- ✅ Target: Natural variation, organic edges, detailed architecture

See: `docs/reference/visual_targets/README.md` for full comparison

---

## Full Documentation

See: `docs/agent-instructions/VISUAL_VALIDATION_REQUIREMENTS.md`
