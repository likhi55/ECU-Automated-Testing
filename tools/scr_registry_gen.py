# tools/scr_registry_gen.py
import json, re, os, glob
from datetime import datetime

SCR_DIR = "scr"
REG_JSON = os.path.join(SCR_DIR, "registry.json")
REG_MD   = os.path.join(SCR_DIR, "REGISTRY.md")

def first_heading(md_path):
    try:
        with open(md_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("#"):
                    return re.sub(r"^#+\s*", "", line.strip()).strip()
    except Exception:
        pass
    return None

def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"scr": []}

def save_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def upsert(entry_list, new_entry, key="id"):
    for i, e in enumerate(entry_list):
        if e.get(key) == new_entry[key]:
            entry_list[i].update(new_entry)
            return
    entry_list.append(new_entry)

def main():
    data = load_json(REG_JSON)
    files = sorted(glob.glob(os.path.join(SCR_DIR, "SCR*.md")))
    seen = set()

    for p in files:
        fname = os.path.basename(p)
        m = re.match(r"(SCR\d{6})\.md$", fname)
        if not m: 
            continue
        scr_id = m.group(1)
        seen.add(scr_id)
        title = first_heading(p) or scr_id
        upsert(data["scr"], {
            "id": scr_id,
            "title": title,
            "path": p.replace("\\", "/"),
            # leave issue_number/issue_url/status for the workflow to fill
        })

    # prune removed files
    data["scr"] = [e for e in data["scr"] if e["id"] in seen]

    # sort by numeric id
    data["scr"].sort(key=lambda e: int(e["id"][3:]))

    save_json(REG_JSON, data)

    # write MD
    lines = []
    lines.append("# SCR Registry")
    lines.append("")
    lines.append(f"_Auto-generated: {datetime.utcnow().isoformat(timespec='seconds')}Z_")
    lines.append("")
    lines.append("| SCR ID | Title | Issue | Status | File |")
    lines.append("|-------:|-------|-------|--------|------|")
    for e in data["scr"]:
        issue = f"[#{e['issue_number']}]({e['issue_url']})" if e.get("issue_number") else "—"
        status = e.get("status", "open")
        filelink = e["path"]
        lines.append(f"| `{e['id']}` | {e['title']} | {issue} | `{status}` | `{filelink}` |")

    with open(REG_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

if __name__ == "__main__":
    main()
