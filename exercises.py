#!/usr/bin/env python3
"""
Code P exercises (EX1-EX50)
Rules:
- Each answer graded: Correct / Partially correct / Incorrect
- Model answer shown ONLY on attempt 5
- Attempt 4 with score < 0.50 is rejected
"""

import os
import json
import random
from datetime import datetime

EX_PROGRESS_FILE = "exercise_progress.json"


def clear():
    os.system("clear" if os.name != "nt" else "cls")


def load_progress():
    if os.path.exists(EX_PROGRESS_FILE):
        try:
            with open(EX_PROGRESS_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"attempts": {}, "scores": {}, "completed": []}


def save_progress(data):
    with open(EX_PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def grade_answer(user_answer: str, expected: str) -> float:
    """Return correctness ratio 0.0 .. 1.0"""
    user = user_answer.strip().lower()
    exp = expected.strip().lower()
    if not user:
        return 0.0
    if len(user) < 3:
        return 0.0
    if user == exp:
        return 1.0
    if user in exp or exp in user:
        return 0.85

    user_words = {w for w in user.replace(".", " ").replace(",", " ").split() if len(w) > 2}
    exp_words = {w for w in exp.replace(".", " ").replace(",", " ").split() if len(w) > 2}
    if not exp_words:
        return 0.0
    overlap = len(user_words & exp_words)
    ratio = overlap / max(len(exp_words), 1)
    # clamp
    if ratio > 1:
        ratio = 1.0
    return ratio


def label_score(score: float) -> str:
    if score >= 0.80:
        return "Correct"
    if score >= 0.50:
        return "Partially correct"
    return "Incorrect"


def practice_one(ex):
    """
    Critical attempt logic:
    - feedback every attempt
    - model answer only at attempt 5
    - attempt 4 below 50% rejected
    """
    clear()
    print(f"{ex['id']} - {ex['title']} ({ex['level']})")
    print("\nBROKEN / TASK CODE:")
    print(ex["broken"])
    print("\nSYMPTOM / SCENARIO:")
    print(ex["symptom"])
    print("\nTASKS:")
    for i, t in enumerate(ex["tasks"], 1):
        print(f"{i}. {t}")

    expected = ex["answer"]
    progress = load_progress()
    attempt = 0
    best = 0.0

    while attempt < 5:
        attempt += 1
        print(f"\n--- Attempt {attempt}/5 ---")
        ans = input("Your solution/explanation:\n> ").strip()
        score = grade_answer(ans, expected)
        best = max(best, score)
        print(f"Result: {label_score(score)} ({int(score * 100)}%)")

        # Attempt 4 rejection rule
        if attempt == 4 and score < 0.50:
            print("Rejected on 4th attempt (< 50% correctness). Try again.")
            # do not consume as successful finish; allow a replacement 4th try
            attempt -= 1
            continue

        # Model answer ONLY on 5th attempt
        if attempt >= 5:
            print("\nMODEL ANSWER:")
            print(expected)
            break

        print("Model answer is locked until attempt 5.")

    # persistence
    progress["attempts"][ex["id"]] = progress.get("attempts", {}).get(ex["id"], 0) + attempt
    prev = progress.get("scores", {}).get(ex["id"], 0)
    progress.setdefault("scores", {})[ex["id"]] = max(prev, best)
    if best >= 0.80 and ex["id"] not in progress.get("completed", []):
        progress.setdefault("completed", []).append(ex["id"])
    progress["last_update"] = datetime.now().isoformat()
    save_progress(progress)

    print(f"\nSaved. Best score for {ex['id']}: {int(best * 100)}%")
    input("Press Enter...")


EXERCISES = [
    # -------- EX1-EX20 core --------
    {"id":"EX1","title":"Early return in nested loop","level":"Beginner","broken":"def flatten(bags):\n    flat=[]\n    for bag in bags:\n        for x in bag:\n            flat.append(x)\n        return flat\n","symptom":"Only first bag processed","tasks":["Find bug","Explain","Minimal fix"],"answer":"return is inside outer loop so function exits early. Dedent return to function level after both loops."},
    {"id":"EX2","title":"append vs extend on strings","level":"Intermediate","broken":"out.extend(list(token)) for token in items","symptom":"Flags/tokens split into characters","tasks":["Why split?","When extend is correct","Safe fix"],"answer":"list(string) yields characters. extend expands iterable. append whole string; extend only real lists."},
    {"id":"EX3","title":"Hardcoded salt + print leak","level":"Intermediate","broken":"salt=b'advanced_path_generator_v200'; print(salt)","symptom":"Shared salt pattern and secret leakage","tasks":["Two problems","Minimal patch","What never to show"],"answer":"Hardcoded salt and debug leak. Use secrets.token_bytes(32), remove print. Never show internal salt or intermediates."},
    {"id":"EX4","title":"DictReader without header","level":"Beginner","broken":"CSV without header used by DictReader","symptom":"Wrong keys/odd behavior","tasks":["What header is required","What breaks","Correct header"],"answer":"DictReader needs header names. Without header first row becomes keys. Use type,term,meaning,category."},
    {"id":"EX5","title":"JSON progress KeyError","level":"Beginner","broken":"progress['wrong'].append(...) with default {}","symptom":"KeyError on first run","tasks":["Why","Safe default","Rewrite loader"],"answer":"Default {} lacks keys. Use {'wrong': [], 'next_review': {}}."},
    {"id":"EX6","title":"Off-by-one switch point","level":"Intermediate","broken":"if i <= switch_point","symptom":"One extra hardened level","tasks":["Boundary bug","Which indexes","Fix compare"],"answer":"<= hardens one extra index. Use i < switch_point."},
    {"id":"EX7","title":"Noise before digits","level":"Intermediate","broken":"piece = noise + number + \"'\"","symptom":"Invalid path parsing risk","tasks":["Why dangerous","Correct order","Rule"],"answer":"Digits must come first. Order: number, optional ', then noise."},
    {"id":"EX8","title":"Shadowed loop variable","level":"Intermediate","broken":"for emoji in pools:\n  for emoji in emoji:","symptom":"Fragile confusing logic","tasks":["Define shadowing","Rename","Risk"],"answer":"Inner name overwrites outer. Use group/item names."},
    {"id":"EX9","title":"Missing try-except int(input)","level":"Beginner","broken":"num=int(input(...))","symptom":"ValueError on text","tasks":["Exception","Wrap","Default"],"answer":"Catch ValueError and fallback default e.g. 10."},
    {"id":"EX10","title":"Direct experimental commits on main","level":"Process","broken":"commit breaks directly on main","symptom":"Stable branch ruined","tasks":["Why bad","Safer flow","When merge"],"answer":"Use feature branch, test, then merge to main."},
    {"id":"EX11","title":"Secret committed then deleted","level":"Security","broken":"commit .env then delete file","symptom":"Secret remains in history","tasks":["Why not enough","What to do to secret","Prevention"],"answer":"Rotate secret; history still has it. .gitignore and env vars."},
    {"id":"EX12","title":"cat heredoc .gitignore","level":"Linux","broken":"echo .env > .gitignore only","symptom":"Incomplete ignore rules","tasks":["Write heredoc command","Include key entries","Why heredoc"],"answer":"cat > .gitignore << 'EOF' ... EOF with .env __pycache__/ venv/."},
    {"id":"EX13","title":"diff then patch workflow","level":"Linux","broken":"no patch trail for edits","symptom":"No auditable repair","tasks":["Create patch","Inspect","Apply"],"answer":"diff -u old new > fix.patch; cat fix.patch; patch < fix.patch"},
    {"id":"EX14","title":"heredoc piped to patch","level":"Linux","broken":"need inline patch no file","symptom":"Unknown inline pattern","tasks":["Write pattern","Risk","Benefit"],"answer":"cat << 'PATCH' | patch ... PATCH. Fast but risky without review."},
    {"id":"EX15","title":"Combined cat/diff/patch recovery","level":"Linux","broken":"broken config no trail","symptom":"Ad-hoc irreparable edits","tasks":["Ordered steps","Why order matters"],"answer":"backup, edit, diff -u backup edited > fix.patch, review with cat, apply patch."},
    {"id":"EX16","title":"Deep nested count early return","level":"Intermediate","broken":"return inside middle nested loop","symptom":"Undercount","tasks":["Find return level","Fix","Link to flatten"],"answer":"Return too deep. Accumulate all levels then return once."},
    {"id":"EX17","title":"Nested stall random.choice","level":"Intermediate","broken":"random.choice(nested_groups)","symptom":"Whole group selected","tasks":["Why","Flatten then choose","Generator link"],"answer":"choice picks top-level list. Flatten first."},
    {"id":"EX18","title":"Thin UI violated","level":"Design","broken":"pbkdf2 and path build inside main.py","symptom":"Hard to audit/test","tasks":["Principle violated","File split","Role of main"],"answer":"Separation of concerns. crypto.py/generator.py; main coordinates only."},
    {"id":"EX19","title":"Fixed switch point fingerprint","level":"Security","broken":"if i < 200 always","symptom":"Predictable structure","tasks":["Why fingerprint","Random switch","Attacker advantage"],"answer":"Fixed pattern is detectable. Use random switch_point range."},
    {"id":"EX20","title":"Loose is_correct false positives","level":"Logic","broken":"return user in correct with no min length","symptom":"Weak answers pass","tasks":["False positive example","Min length","Tighten rule"],"answer":"Require len>=3 and stronger token overlap."},

    # -------- EX21-EX35 advanced --------
    {"id":"EX21","title":"PBKDF2 iterations too low","level":"Advanced","broken":"pbkdf2_hmac(..., 1000)","symptom":"Fast brute force","tasks":["Why weak","Choose stronger setting","Tradeoff"],"answer":"Low iterations are cheap to attack. Use high iteration count; slower but safer."},
    {"id":"EX22","title":"Returning internal salt to UI","level":"Advanced","broken":"return salt, stretched and print both","symptom":"Secret surface expanded","tasks":["Why bad","What to return","Least privilege"],"answer":"Return only what next step needs. Never expose internal salt to UI/logs."},
    {"id":"EX23","title":"Predictable path ending always same","level":"Advanced","broken":"always force identical large suffix pattern","symptom":"Structural fingerprint","tasks":["Identify leak","What can stay fixed","What should vary"],"answer":"Keep compatibility constraints minimal; avoid unnecessary fixed long patterns."},
    {"id":"EX24","title":"Env var missing handling","level":"Advanced","broken":"os.environ['APP_PEPPER'] with no check","symptom":"KeyError crash","tasks":["Safer read","Fail closed?","Message quality"],"answer":"Use get() and raise clear config error if required secret absent."},
    {"id":"EX25","title":".env committed in repo","level":"Advanced","broken":"git add .env","symptom":"Secret exposure risk","tasks":["Immediate actions","Repo controls","Future prevention"],"answer":"Rotate secrets, remove from tracking, add .gitignore, protect branch."},
    {"id":"EX26","title":"Feature branch not used","level":"Advanced","broken":"all work on main","symptom":"No safe experimentation","tasks":["Describe branch flow","PR review value","Main protection"],"answer":"Develop on feature branch, review, merge. Protect main."},
    {"id":"EX27","title":"Clipboard code not optional","level":"Advanced","broken":"always call termux-clipboard-set","symptom":"Fails on desktop Linux","tasks":["Portability issue","Fallback design","Detection approach"],"answer":"Wrap clipboard in try/except or platform check; fallback to manual copy."},
    {"id":"EX28","title":"HMAC used with non-secret key material","level":"Advanced","broken":"hmac.new(b'public', ...)","symptom":"Weak binding","tasks":["Why key matters","Where key should come from","Fix direction"],"answer":"HMAC key should be secret material from secure salt/seed context."},
    {"id":"EX29","title":"Logging path with passphrase","level":"Advanced","broken":"logger.info(passphrase)","symptom":"Secret in logs","tasks":["Risk","What may be logged","Safe policy"],"answer":"Never log secrets. Log events only, not secret values."},
    {"id":"EX30","title":"Random from random module for security","level":"Advanced","broken":"import random; random.randint for salt","symptom":"Not cryptographically secure","tasks":["Why wrong","What to use","Where acceptable"],"answer":"Use secrets for security-sensitive randomness; random is for non-security tasks."},
    {"id":"EX31","title":"Git force push on shared main","level":"Advanced","broken":"git push --force origin main","symptom":"History rewrite danger","tasks":["Risk to collaborators","Safer alternative","Policy"],"answer":"Avoid force push on shared main. Use PR and protected branch rules."},
    {"id":"EX32","title":"Dependency not pinned","level":"Advanced","broken":"streamlit with no version pin","symptom":"Reproducibility and supply risk","tasks":["Why pin","requirements approach","Update strategy"],"answer":"Pin versions for reproducibility; update intentionally."},
    {"id":"EX33","title":"Exception swallowed silently","level":"Advanced","broken":"try: ...\nexcept: pass","symptom":"Hidden failures","tasks":["Why bad","Better pattern","User messaging"],"answer":"Catch specific exceptions, log/safe message, fail visibly when needed."},
    {"id":"EX34","title":"Path truncation splits emoji","level":"Advanced","broken":"path[:500] hard cut","symptom":"Broken unicode segment","tasks":["Why unicode cut fails","Safer approach","Validation"],"answer":"Hard byte/char cuts can split graphemes. Truncate on segment boundaries."},
    {"id":"EX35","title":"Same pepper for all users in multi-user service","level":"Advanced","broken":"global hardcoded pepper in source","symptom":"Cross-user secret concentration","tasks":["Architecture issue","Better secret storage","Return policy"],"answer":"Do not hardcode shared pepper in source; use external secret storage and least return."},

    # -------- EX36-EX50 master's research-grade --------
    {"id":"EX36","title":"Threat model: local CLI vs public web","level":"Master","broken":"same trust assumptions for Termux CLI and public Streamlit","symptom":"Missing rate limit and abuse controls on web","tasks":["Compare threat models","Controls for each","What transfers"],"answer":"CLI local user threat differs from public web. Web needs rate limits input validation and stricter secret handling."},
    {"id":"EX37","title":"Supply-chain malicious PR review","level":"Master","broken":"merge dependency 'cleanup' PR without line audit","symptom":"Possible exfiltration commit","tasks":["What to inspect","High-risk patterns","Process control"],"answer":"Review every line for network calls secret reads and unexpected files. Protect main require review."},
    {"id":"EX38","title":"Research critique of obfuscation claims","level":"Master","broken":"README claims emoji noise equals cryptographic strength","symptom":"Overstated security marketing","tasks":["Separate claims","Evidence standard","Rewrite claim ethically"],"answer":"Obfuscation is not crypto strength. State noise as usability/obfuscation only; ground security in CSPRNG and KDF."},
    {"id":"EX39","title":"Fingerprintability evaluation plan","level":"Master","broken":"no methodology to test path structure leakage","symptom":"Unknown detectability","tasks":["Define metrics","Experiment design","Mitigation loop"],"answer":"Measure structural invariants across outputs, test classifier detectability, randomize non-essential patterns."},
    {"id":"EX40","title":"Secret retention in memory/UI buffers","level":"Master","broken":"passphrase stays in multiple variables and widgets","symptom":"Extended exposure window","tasks":["Exposure points","Minimization strategy","UI guidance"],"answer":"Minimize copies, avoid logs, clear temporary buffers where practical, show once with user save responsibility."},
    {"id":"EX41","title":"Argon2id migration design","level":"Master","broken":"PBKDF2 only with no migration notes","symptom":"Unclear upgrade path","tasks":["Benefits","Compatibility concerns","Parameter choices"],"answer":"Argon2id improves memory-hardness. Document params and keep reproducibility notes for local tooling."},
    {"id":"EX42","title":"Reproducible research packaging","level":"Master","broken":"no pinned deps no version tag no checksum","symptom":"Weak artifact integrity","tasks":["Package requirements","Integrity controls","Release checklist"],"answer":"Pin deps, tag releases, provide checksums, document exact run steps."},
    {"id":"EX43","title":"Adversarial README social engineering","level":"Master","broken":"README tells users to disable verification and paste seeds online","symptom":"Dangerous guidance","tasks":["Identify unsafe advice","Rewrite safe guidance","Why users fall for it"],"answer":"Never ask for seeds online. Emphasize offline test-with-small-amount and password manager storage."},
    {"id":"EX44","title":"Cross-platform clipboard threat differences","level":"Master","broken":"assume clipboard is private everywhere","symptom":"Clipboard malware risk ignored","tasks":["Threat variance","Mitigations","UX tradeoff"],"answer":"Clipboard can be sniffed. Offer manual copy and warn on shared devices."},
    {"id":"EX45","title":"Git history secret incident response","level":"Master","broken":"only delete file after leak","symptom":"Incomplete response","tasks":["Incident steps","Technical vs operational","Communication"],"answer":"Rotate revoke rewrite if needed, audit logs, notify affected parties, prevent with scanning and ignore rules."},
    {"id":"EX46","title":"Formalizing least privilege in module APIs","level":"Master","broken":"crypto functions return full internal state objects","symptom":"Unnecessary secret spread","tasks":["API redesign","Return minimization","Test strategy"],"answer":"Return only required outputs. Keep internal state local. Unit test that secrets are not included in UI-facing returns."},
    {"id":"EX47","title":"Evaluating non-determinism claims","level":"Master","broken":"claim non-deterministic but seed fixed in tests accidentally left on","symptom":"False assurance","tasks":["How to verify","Test harness design","Release gate"],"answer":"Run multiple generations assert diversity. Ensure test-only seeds cannot ship enabled."},
    {"id":"EX48","title":"Hybrid exam: loop + security","level":"Master","broken":"flatten pools with extend(list()) then use for path noise and log chosen noise","symptom":"Broken tokens plus leakage","tasks":["Identify both bug classes","Patch both","Explain interaction"],"answer":"Use safe flatten and never log selected secret-adjacent material."},
    {"id":"EX49","title":"Defense-in-depth map for Code N2","level":"Master","broken":"single control focus on emojis only","symptom":"Shallow defense","tasks":["List layered controls","Map to files","Residual risks"],"answer":"Layers: CSPRNG, hidden salt, KDF, optional passphrase, structural unpredictability, repo hygiene. Residual: user backup failure and endpoint malware."},
    {"id":"EX50","title":"Research mini-proposal","level":"Master","broken":"no evaluation criteria for custom path generator security claims","symptom":"Not research-grade","tasks":["Write research question","Methods","Threat model","Metrics","Ethics"],"answer":"RQ on detectability vs usability. Methods: entropy estimates structural classifiers recovery tests. Metrics: detection AUC compatibility rate user error. Ethics: no real-fund risk, no seed collection."},
]


def show_stats(progress):
    completed = progress.get("completed", [])
    scores = progress.get("scores", {})
    print(f"Completed: {len(completed)}/50")
    if scores:
        avg = sum(scores.values()) / len(scores)
        print(f"Average best score: {int(avg * 100)}%")
    else:
        print("No scores yet.")


def run_exercises():
    while True:
        clear()
        progress = load_progress()
        print("=== Exercises-only mode (EX1-EX50) ===")
        show_stats(progress)
        print("\n1. List all exercises")
        print("2. Practice one by ID")
        print("3. Random exercise")
        print("4. Random Master-level only")
        print("0. Back")
        choice = input("\nChoose: ").strip()

        if choice == "0":
            return
        if choice == "1":
            clear()
            for ex in EXERCISES:
                mark = "✓" if ex["id"] in progress.get("completed", []) else " "
                print(f"[{mark}] {ex['id']} [{ex['level']}] {ex['title']}")
            input("\nPress Enter...")
        elif choice == "2":
            ex_id = input("ID (EX1..EX50): ").strip().upper()
            ex = next((e for e in EXERCISES if e["id"] == ex_id), None)
            if not ex:
                print("Not found")
                input("Press Enter...")
            else:
                practice_one(ex)
        elif choice == "3":
            practice_one(random.choice(EXERCISES))
        elif choice == "4":
            masters = [e for e in EXERCISES if e["level"] == "Master"]
            practice_one(random.choice(masters))
        else:
            print("Invalid choice")
            input("Press Enter...")


if __name__ == "__main__":
    run_exercises()