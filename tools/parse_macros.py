#!/usr/bin/env python3
"""Parse a UO classic (2D) client MACROS.TXT into keybinds.json.

MACROS.TXT entry format (entries separated by a line of ``########``)::

    <KEY> <f1> <f2> <f3>
    <action line 1>
    [<action line 2> ...]
    ########

The three flags after the key name are modifier toggles (0/1).  For this
data set the order is interpreted as ``Ctrl Alt Shift`` (see README for the
reasoning).  Change MOD_ORDER below if that turns out to be wrong.
"""
import json
import sys
from datetime import date
from pathlib import Path

MOD_ORDER = ["ctrl", "alt", "shift"]


def categorize(actions):
    head = (actions[0] if actions else "").strip().lower()
    if head.startswith("castspell"):
        return "spell"
    if head.startswith("useskill"):
        return "skill"
    if head.startswith(("say", "yell", "emote", "whisper")):
        return "say"
    return "command"


def parse(text):
    bindings = []
    entry = []
    for raw in text.splitlines():
        line = raw.rstrip("\n")
        if line.strip() == "########":
            if entry:
                bindings.append(build(entry))
                entry = []
            continue
        if line.strip() == "" and not entry:
            continue
        entry.append(line)
    if entry:
        bindings.append(build(entry))
    return [b for b in bindings if b]


def build(entry):
    header = entry[0].strip()
    if not header:
        return None
    tokens = header.split()
    # last three tokens are the modifier flags; everything before is the key name
    flags = tokens[-3:]
    key = " ".join(tokens[:-3]).strip()
    mods = {name: flags[i] == "1" for i, name in enumerate(MOD_ORDER)}
    actions = [a.strip() for a in entry[1:] if a.strip()]
    return {
        "key": key,
        "mods": mods,
        "actions": actions,
        "category": categorize(actions),
        "source": "client",  # UO client macro (vs. "uoassist")
    }


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/MACROS.TXT")
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("data/keybinds.default.json")
    bindings = parse(src.read_text(encoding="utf-8", errors="replace"))
    doc = {
        "meta": {
            "title": "UO キーバインド",
            "source": src.name,
            "modifierOrder": MOD_ORDER,
            "generated": date.today().isoformat(),
        },
        "bindings": bindings,
    }
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # summary to stderr
    from collections import Counter
    cats = Counter(b["category"] for b in bindings)
    print(f"parsed {len(bindings)} bindings -> {out}", file=sys.stderr)
    print("by category:", dict(cats), file=sys.stderr)


if __name__ == "__main__":
    main()
