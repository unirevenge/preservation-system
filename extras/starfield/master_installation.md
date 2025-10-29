# 🎮 STARFIELD OPTIMIZED CONFIGURATION
## Complete Installation Package - All Files Ready

---

## 📦 PACKAGE CONTENTS (11 FILES)

### ✅ FILES 1-4: Core Configuration (INI + TOML)
Place in respective folders as indicated below

### ✅ FILES 5-11: Batch Utilities
All go in `Starfield/Data/` folder

---

## 📂 INSTALLATION LOCATIONS

```
📁 C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data/
├── 📄 DawFiles.toml                    ← FILE 1
├── 📄 Freebird.txt                     ← FILE 5
├── 📄 bkrTra.txt                       ← FILE 6
├── 📄 ELockP.txt                       ← FILE 7
├── 📄 DawInventoryReset.txt            ← FILE 8
├── 📄 EssToPower.txt                   ← FILE 9
├── 📄 MTNA.txt                         ← FILE 10
└── 📄 neuroampth.txt                   ← FILE 11

📁 C:/Users/[YourName]/Documents/My Games/Starfield/
├── 📄 StarfieldCustom.ini              ← FILE 3
├── 📄 StarfieldPrefs.ini               ← FILE 4
└── 📄 Hotkeys.ini                      ← FILE 2
```

---

## 🚀 QUICK INSTALLATION STEPS

### STEP 1: BACKUP EXISTING FILES
```
Create folder: Starfield_Backup_[DATE]
Copy your current INI files there
```

### STEP 2: DELETE OLD FILES
Navigate to `Starfield/Data/` and **DELETE**:
- ❌ DawCH.txt
- ❌ SpaceshipTravel.txt
- ❌ Old DawFiles.toml (if exists)

### STEP 3: COPY ALL FILES
1. Copy artifacts 1, 5-11 → `Starfield/Data/`
2. Copy artifacts 2-4 → `Documents/My Games/Starfield/`

### STEP 4: LAUNCH & TEST
- Start Starfield
- Look for: "DawFiles Optimized - All Systems Active"
- Press F5 (Quick Save) to test hotkeys
- Press Ctrl-F4 to test batch files (clear bounties)

---

## 🎯 FILE SUMMARIES

### FILE 1: DawFiles.toml (Auto-loads on game start)
**Contains:**
- Balanced player stats (1000 HP, 50K carry weight)
- Enhanced resistances (150 damage/energy resist)
- Ship system improvements
- Scanner enhancements
- Starting resources (2M credits, 25K caps, 2K ammo)

### FILE 2: Hotkeys.ini (50+ Keybinds)
**Key Features:**
- F1-F12: Primary functions (save, heal, combat)
- Ctrl+F1-F12: Utilities (perks, cheats, lockpicking)
- NumPad: Companions & items
- Special keys: N (night vision), - (noclip), = (freecam)

### FILE 3: StarfieldCustom.ini (Engine Settings)
**Optimizations:**
- RX 7600 8GB VRAM optimized
- 120 FOV all views
- Shadow quality: 1024 resolution
- Volumetric lighting: OFF (VRAM saver)

### FILE 4: StarfieldPrefs.ini (Graphics Settings)
**Optimizations:**
- FSR3 Performance mode (85% render scale)
- Frame generation enabled
- TAA disabled (FSR3 handles AA)
- Target: 60+ FPS

### FILE 5: Freebird.txt (Ctrl-F4)
Clears all bounties across 9 factions instantly

### FILE 6: bkrTra.txt (Ctrl-F5)
Adds all Physical + Combat tree perks

### FILE 7: ELockP.txt (Ctrl-F7)
Makes all locks 1-ring puzzles (trivial difficulty)

### FILE 8: DawInventoryReset.txt (Ctrl-F9)
Wipes inventory, adds essentials, sets 50K carry weight

### FILE 9: EssToPower.txt (NumPad 5)
Converts essence to power (mod-specific)

### FILE 10: MTNA.txt (Console: bat MTNA)
Teleports to New Atlantis instantly

### FILE 11: neuroampth.txt (Console: bat neuroampth)
Adds all neuroamps (mod-specific)

---

## ⌨️ HOTKEY QUICK REFERENCE

### F-Keys (Primary)
| Key | Function | Key | Function |
|-----|----------|-----|----------|
| F1 | Use Stimpack | F7 | Kill All |
| F2 | Use Med Item | F8 | God Mode |
| F3 | +5K Credits | F9 | Quick Load |
| F4 | +500 Health | F10-F12 | Time Set |
| F5 | Quick Save | F6 | Combat AI |

### Ctrl+F-Keys (Utilities)
| Key | Function | Key | Function |
|-----|----------|-----|----------|
| Ctrl-F1 | Char Editor | Ctrl-F7 | Easy Lockpick |
| Ctrl-F2 | Resurrect | Ctrl-F8 | Max Carry |
| Ctrl-F3 | +Digipicks | Ctrl-F9 | Reset Inventory |
| Ctrl-F4 | **Clear Bounties** | Ctrl-F10 | Space Combat |
| Ctrl-F5 | **Add Perks** | Ctrl-F11 | Sleep Menu |
| Ctrl-F6 | **SUPER CHEAT** | Ctrl-F12 | Toggle HUD |

### NumPad (Companions & Items)
| Key | Function | Key | Function |
|-----|----------|-----|----------|
| 0 | Call Sarah | 5 | Essence→Power |
| 1 | Call Vasco | 6-8 | Use Items |
| 2 | Call Ship | 9 | Restock Ammo |
| 3 | Invis ON | + | Use Food |
| 4 | Invis OFF | - | Use Drink |

### Ctrl+NumPad (Advanced)
| Key | Function | Key | Function |
|-----|----------|-----|----------|
| Ctrl-0 | Barrett | Ctrl-5 | All Powers |
| Ctrl-1 | Sam | Ctrl-8 | Refill Fuel |
| Ctrl-2 | Andreja | Ctrl-9 | Repair Ship |

### Special Keys
| Key | Function | Key | Function |
|-----|----------|-----|----------|
| N | Night Vision | - | NoClip |
| O | Auto Oxygen | = | Free Cam |
| Home | Speed Boost | End | Normal Speed |
| Backspace | Quick Save | Insert | Quick Load |

---

## 🔧 EXPECTED PERFORMANCE (RX 7600 8GB)

### Before Optimization
- New Atlantis: 35-45 FPS
- Space: 55-65 FPS
- Combat: 40-50 FPS

### After Optimization
- New Atlantis: 45-55 FPS (+10-15)
- Space: 70-90 FPS (+15-25)
- Combat: 55-70 FPS (+15-20)

---

## ⚙️ CUSTOMIZATION OPTIONS

### Want MORE FPS?
Edit **StarfieldPrefs.ini**:
```ini
fRenderResolutionScaleFactor=0.75  ; Lower from 0.85
```

### Want LESS Cheaty?
Edit **DawFiles.toml**:
```toml
"player.setav carryweight 10000",  ; Lower from 50000
"player.modav DamageResist 50",    ; Lower from 150
"player.additem f 500000",         ; Lower from 2000000
```

### Want MORE Cheaty?
Press **Ctrl-F6** for SUPER CHEAT MODE:
- 1M carry weight
- 500 resistances
- 10M credits
- 5K health
- Level 100
- 50 perk points

---

## 🐛 TROUBLESHOOTING

### Problem: No "DawFiles Optimized" notification
**Solution:**
- Verify file named exactly: `DawFiles.toml`
- Check location: `Starfield/Data/`
- Ensure proper TOML syntax (no errors)

### Problem: Hotkeys don't work
**Solution:**
- Open StarfieldCustom.ini
- Verify under [Menu]: `sConsoleINI=Hotkeys.ini`
- Restart game

### Problem: "Batch file not found"
**Solution:**
- Ensure files in `Starfield/Data/` (not subfolders)
- Check exact names: Freebird.txt, bkrTra.txt, ELockP.txt
- No "_Optimized" suffix

### Problem: Low FPS
**Solution:**
- Lower render scale to 0.75 in StarfieldPrefs.ini
- Disable grass: `bAllowLoadGrass=0`
- Reduce shadows: `fShadowDistance=3000`

### Problem: Commands work but no notifications
**Solution:**
- Console Command Runner mod not installed
- Commands still work, just no visual feedback
- Check mods are enabled in plugins.txt

---

## 📋 VERIFICATION CHECKLIST

Before playing, verify:

**Installation:**
- [ ] All 11 files downloaded from artifacts
- [ ] Old redundant files deleted (DawCH, SpaceshipTravel)
- [ ] Original INI files backed up
- [ ] New files in correct folders
- [ ] Files renamed correctly (no _Optimized suffix)

**Testing:**
- [ ] Game launches without crashes
- [ ] "DawFiles Optimized" notification appears
- [ ] F5 saves game (notification shows)
- [ ] Ctrl-F4 clears bounties (notification shows)
- [ ] F8 toggles god mode
- [ ] NumPad 0 calls Sarah

**Performance:**
- [ ] FPS is 50+ in most areas
- [ ] No stuttering or freezing
- [ ] Graphics look sharp (FSR3 working)
- [ ] Shadows look acceptable

---

## 🎮 GAMEPLAY MODES

### Balanced Mode (Default - Recommended)
- DawFiles.toml active (auto-loads)
- Use hotkeys for convenience
- 50K carry weight, 150 resistances
- Good for first playthrough

**What's Active:**
✅ Enhanced stats
✅ Better ships
✅ Improved scanner
✅ Quality of life hotkeys

**What's Inactive:**
❌ Super cheat mode
❌ Easy lockpicking
❌ God mode

### Creative Mode (Full Cheats)
Press these in order:
1. **Ctrl-F6** → Super Cheat (max stats)
2. **Ctrl-F5** → All Perks
3. **Ctrl-F7** → Easy Lockpicking
4. **F8** → God Mode
5. **Ctrl-NumPad5** → All Powers

**Result:** Maximum power for testing, building, screenshots

### Immersion Mode (Minimal Cheats)
To disable DawFiles.toml auto-load:
1. Move DawFiles.toml OUT of Data folder
2. Use only convenience hotkeys (F5/F9, NumPad)
3. Avoid Ctrl-F6, Ctrl-F5, Ctrl-F7

**Result:** Near-vanilla with QoL improvements

---

## 📞 ADDITIONAL SUPPORT

### Console Commands (Type in game console)
```
bat MTNA           - Teleport to New Atlantis
bat neuroampth     - Add all neuroamps (if mod installed)
bat Freebird       - Clear bounties (same as Ctrl-F4)
bat bkrTra         - Add perks (same as Ctrl-F5)
bat ELockP         - Easy lockpick (same as Ctrl-F7)
psb                - Add ALL powers and perks (built-in)
```

### Manual Adjustments
**Change FOV:**
```
fov 100    ; Set to 100
fov 110    ; Set to 110
fov 120    ; Set to 120
```

**Add Items:**
```
player.additem f 1000000        ; Add 1M credits
player.additem 0000000A 100     ; Add 100 digipicks
player.additem 0000000F 50000   ; Add 50K caps
player.additem 002B5597 5000    ; Add 5K ammo
```

**Modify Stats:**
```
player.setav carryweight 100000  ; Set carry weight
player.setav health 2000         ; Set health
player.setav speedmult 200       ; Set speed (200%)
```

---

## ✨ WHAT'S BEEN OPTIMIZED

### Configuration
✅ Consolidated 3 files into 1 (DawFiles.toml)
✅ Eliminated all duplicate commands
✅ Balanced cheat values (not game-breaking)
✅ Added 50+ hotkeys for instant access
✅ Fixed all missing batch file references

### Performance
✅ FSR3 configured for AMD RX 7600
✅ Volumetric lighting disabled (major VRAM saver)
✅ Shadow quality balanced (1024 resolution)
✅ TAA disabled (FSR3 handles upscaling)
✅ Expected 15-20 FPS improvement

### Usability
✅ One-press access to all utilities
✅ Complete hotkey integration
✅ Smart conditional item usage
✅ Comprehensive documentation
✅ Easy customization options

---

## 🎉 YOU'RE READY!

All 11 files are provided above in individual artifacts:
1. DawFiles.toml
2. Hotkeys.ini
3. StarfieldCustom.ini
4. StarfieldPrefs.ini
5. Freebird.txt
6. bkrTra.txt
7. ELockP.txt
8. DawInventoryReset.txt
9. EssToPower.txt
10. MTNA.txt
11. neuroampth.txt

**Simply copy each file to its designated location and enjoy your optimized Starfield experience!**

---

**Document Version:** 3.0 Final
**Package:** Complete Optimization Suite
**Files:** 11 (4 Core + 7 Batch)
**Compatible:** Starfield + Shattered Space DLC
**Optimized For:** AMD RX 7600 8GB VRAM
**Target FPS:** 60+ in most areas
