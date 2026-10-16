
EXERCISES = [
    {
        "id": "EX1",
        "title": "Early return in nested loop",
        "level": "Beginner",
        "broken_code_text": '''def flatten_bags(list_of_bags):
    flat_list = []
    for one_bag in list_of_bags:
        for one_item in one_bag:
            flat_list.append(one_item)
        return flat_list

print(flatten_bags([[1, 2], [3]]))''',
        "symptom_text": "Output is [1, 2] instead of [1, 2, 3]",
        "task_list": ["Find the bug", "Explain why", "Write minimal fix"],
        "model_answer_text": "return is inside the outer loop so the function exits after the first bag. Move return to the end of the function after both loops.",
    },
    {
        "id": "EX2",
        "title": "append vs extend on strings",
        "level": "Intermediate",
        "broken_code_text": '''def flatten_pool(token_list):
    flat_list = []
    for one_token in token_list:
        flat_list.extend(list(one_token))
    return flat_list

print(flatten_pool(["AB", "CD"]))''',
        "symptom_text": "Gets ['A','B','C','D'] instead of whole tokens",
        "task_list": ["Why split?", "When is extend correct?", "Safe fix"],
        "model_answer_text": "list(string) breaks a string into characters. Use append for whole strings. Use extend only when the value is already a list of items.",
    },
    {
        "id": "EX3",
        "title": "Hardcoded salt + print leak",
        "level": "Intermediate",
        "broken_code_text": '''import hashlib

def make_system_salt(material_bytes):
    salt_bytes = b"advanced_path_generator_v200"
    stretched = hashlib.pbkdf2_hmac("sha3_512", material_bytes, salt_bytes, 600000)
    print("salt=", salt_bytes)
    return stretched.hex()''',
        "symptom_text": "Same salt pattern every time; secret may leak in logs",
        "task_list": ["Name two security problems", "Minimal patch", "What never to show"],
        "model_answer_text": "Hardcoded salt and printed secret. Use secrets.token_bytes(32) and remove print. Never show internal salt or intermediate secret values.",
    },
    {
        "id": "EX4",
        "title": "DictReader without header",
        "level": "Beginner",
        "broken_code_text": '''# knowledge.csv has no header row
import csv
with open("knowledge.csv", newline="", encoding="utf-8") as csv_file:
    rows = list(csv.DictReader(csv_file))
print(rows[0])''',
        "symptom_text": "Keys become first-row values; meaning becomes wrong",
        "task_list": ["What header is required?", "What breaks?", "Correct header line"],
        "model_answer_text": "DictReader expects a header line. Without it, the first data row becomes keys. Use: type,term,meaning,category",
    },
    {
        "id": "EX5",
        "title": "JSON progress KeyError",
        "level": "Beginner",
        "broken_code_text": '''import json, os

def load_progress():
    if os.path.exists("progress.json"):
        with open("progress.json") as progress_file:
            return json.load(progress_file)
    return {}

progress_data = load_progress()
progress_data["wrong"].append({"term": "x"})''',
        "symptom_text": "KeyError: 'wrong' on first run",
        "task_list": ["Why KeyError?", "Safe default structure", "Rewrite loader"],
        "model_answer_text": "Default {} has no 'wrong' key. Default must be {'wrong': [], 'next_review': {}}.",
    },
    {
        "id": "EX6",
        "title": "Off-by-one switch point",
        "level": "Intermediate",
        "broken_code_text": '''switch_point = 5
path_parts = []
for level_number in range(8):
    if level_number <= switch_point:
        path_parts.append(f"{level_number}'")
    else:
        path_parts.append(str(level_number))
print(path_parts)''',
        "symptom_text": "One extra hardened index",
        "task_list": ["Boundary bug", "Which indexes hardened?", "Fix comparison"],
        "model_answer_text": "<= hardens one extra index. Use level_number < switch_point.",
    },
    {
        "id": "EX7",
        "title": "Noise before digits",
        "level": "Intermediate",
        "broken_code_text": '''number_text = "42"
noise_text = "🔥"
path_piece = noise_text + number_text + "'"
print(path_piece)''',
        "symptom_text": "Wallet may reject or misparse path segment",
        "task_list": ["Why dangerous?", "Correct order", "State the rule"],
        "model_answer_text": "Digits must come first. Correct order: number, optional ', then noise.",
    },
    {
        "id": "EX8",
        "title": "Shadowed loop variable",
        "level": "Intermediate",
        "broken_code_text": '''emoji_groups = [["a", "b"], ["c"]]
flat_list = []
for emoji in emoji_groups:
    for emoji in emoji:
        flat_list.append(emoji)
print(flat_list)''',
        "symptom_text": "Works sometimes but is confusing and fragile",
        "task_list": ["What is shadowing?", "Rename cleanly", "Maintainability risk"],
        "model_answer_text": "Inner emoji overwrites outer emoji. Use names like one_group and one_emoji.",
    },
    {
        "id": "EX9",
        "title": "Missing try-except on int(input)",
        "level": "Beginner",
        "broken_code_text": '''how_many = int(input("How many questions? "))
print("Got", how_many)''',
        "symptom_text": "Typing text crashes with ValueError",
        "task_list": ["What exception?", "Wrap safely", "Choose default"],
        "model_answer_text": "ValueError. Use try/except and fallback default such as 10.",
    },
    {
        "id": "EX10",
        "title": "Direct experimental commits on main",
        "level": "Process",
        "broken_code_text": '''# process anti-pattern
# 1. edit on main
# 2. commit experimental break
# 3. push immediately''',
        "symptom_text": "Stable branch becomes unusable",
        "task_list": ["Why dangerous?", "Safer branch flow", "When update main?"],
        "model_answer_text": "Use a feature branch, test, then merge. Main should stay stable.",
    },
    {
        "id": "EX11",
        "title": "Secret committed then deleted",
        "level": "Security",
        "broken_code_text": '''# Day 1: commit .env with real key
# Day 2: delete .env and commit deletion
# Assume secret is gone forever''',
        "symptom_text": "Secret still recoverable from git history",
        "task_list": ["Why deletion is not enough", "What to do to the secret", "Prevention"],
        "model_answer_text": "History still contains the secret. Rotate/revoke it. Add .env to .gitignore and use environment variables.",
    },
    {
        "id": "EX12",
        "title": "Create .gitignore with cat heredoc",
        "level": "Linux",
        "broken_code_text": '''echo .env > .gitignore
# incomplete ignore list''',
        "symptom_text": "Only one ignore rule",
        "task_list": ["Write heredoc command", "Include key entries", "Why heredoc helps"],
        "model_answer_text": "cat > .gitignore << 'EOF' then .env __pycache__/ venv/ then EOF. Heredoc writes multi-line files cleanly.",
    },
    {
        "id": "EX13",
        "title": "diff then patch workflow",
        "level": "Linux",
        "broken_code_text": '''# edited in place with no patch trail''',
        "symptom_text": "No auditable repair history",
        "task_list": ["Create patch command", "Inspect patch", "Apply patch"],
        "model_answer_text": "diff -u old.py new.py > fix.patch; cat fix.patch; patch < fix.patch",
    },
    {
        "id": "EX14",
        "title": "Heredoc piped to patch",
        "level": "Linux",
        "broken_code_text": '''# need emergency fix with no patch file on disk''',
        "symptom_text": "Unknown inline patch pattern",
        "task_list": ["Write pattern", "One risk", "One benefit"],
        "model_answer_text": "cat << 'PATCH' | patch ... PATCH. Benefit: fast. Risk: applying without review can damage files.",
    },
    {
        "id": "EX15",
        "title": "Combined cat/diff/patch recovery",
        "level": "Linux",
        "broken_code_text": '''# config.py broken; config.py.bak exists''',
        "symptom_text": "Ad-hoc edits with no recoverable trail",
        "task_list": ["Ordered recovery steps", "Why order matters"],
        "model_answer_text": "Keep backup, edit copy, diff -u backup edited > fix.patch, review with cat, apply with patch. Order preserves rollback.",
    },
    {
        "id": "EX16",
        "title": "Deep nested counting early return",
        "level": "Intermediate",
        "broken_code_text": '''def count_people(country_data):
    total_people = 0
    for one_state in country_data:
        for one_lga in one_state:
            for one_person in one_lga:
                total_people += 1
            return total_people''',
        "symptom_text": "Counts only first LGA group",
        "task_list": ["Find wrong return level", "Fix function", "Link to flatten lesson"],
        "model_answer_text": "return is too deep. Finish all loops, then return once.",
    },
    {
        "id": "EX17",
        "title": "Nested stall random.choice",
        "level": "Intermediate",
        "broken_code_text": '''import random
emoji_stall = [["🔥", "🚀"], ["🐍"]]
print(random.choice(emoji_stall))''',
        "symptom_text": "Sometimes returns a whole group list",
        "task_list": ["Why?", "Flatten then choose", "Generator link"],
        "model_answer_text": "choice picks one top-level element. Flatten first, then choose from the flat list.",
    },
    {
        "id": "EX18",
        "title": "Thin UI violated",
        "level": "Design",
        "broken_code_text": '''# main.py owns crypto and path building
import hashlib, secrets
def main():
    salt_bytes = secrets.token_bytes(32)
    material = hashlib.pbkdf2_hmac("sha3_512", b"x", salt_bytes, 600000)
    print("m/" + material.hex())''',
        "symptom_text": "Hard to test/audit/reuse",
        "task_list": ["Principle violated", "File split", "Role of main"],
        "model_answer_text": "Separation of Concerns. Move crypto to crypto.py and path building to generator.py. main only coordinates input/output.",
    },
    {
        "id": "EX19",
        "title": "Fixed switch point fingerprint",
        "level": "Security",
        "broken_code_text": '''for level_number in range(levels):
    if level_number < 200:
        piece = f"{index_text}'"
    else:
        piece = index_text''',
        "symptom_text": "Every output shares same hardening pattern",
        "task_list": ["Why fingerprint?", "Random switch approach", "Attacker advantage"],
        "model_answer_text": "Fixed rule is detectable. Use a random switch_point in a range so structure is less predictable.",
    },
    {
        "id": "EX20",
        "title": "Loose answer checker",
        "level": "Logic",
        "broken_code_text": '''def answer_looks_correct(student_answer, expected_answer):
    student_text = student_answer.lower().strip()
    expected_text = expected_answer.lower()
    return student_text in expected_text or expected_text in student_text''',
        "symptom_text": "Very short weak answers can pass",
        "task_list": ["False-positive example", "Min-length guard", "Extra tightening rule"],
        "model_answer_text": "Require length >= 3 and stronger word overlap checks to reduce false positives.",
    },
    {
        "id": "EX21",
        "title": "PBKDF2 iterations too low",
        "level": "Advanced",
        "broken_code_text": '''hashlib.pbkdf2_hmac("sha3_512", material_bytes, salt_bytes, 1000)''',
        "symptom_text": "Too fast to brute force",
        "task_list": ["Why weak?", "Stronger setting idea", "Tradeoff"],
        "model_answer_text": "Low iterations are cheap for attackers. Use a much higher iteration count; slower but safer.",
    },
    {
        "id": "EX22",
        "title": "Returning internal salt to UI",
        "level": "Advanced",
        "broken_code_text": '''return salt_bytes, stretched_bytes  # then print both in UI''',
        "symptom_text": "Secret surface expanded",
        "task_list": ["Why bad?", "What to return?", "Least privilege"],
        "model_answer_text": "Return only what the next step needs. Never expose internal salt to UI or logs.",
    },
    {
        "id": "EX23",
        "title": "Predictable forced path ending",
        "level": "Advanced",
        "broken_code_text": '''# always force the same long artificial ending on every path''',
        "symptom_text": "Structural fingerprint",
        "task_list": ["Identify leak", "What can stay fixed", "What should vary"],
        "model_answer_text": "Keep only necessary compatibility endings. Avoid extra fixed patterns that make every output look the same.",
    },
    {
        "id": "EX24",
        "title": "Missing environment variable handling",
        "level": "Advanced",
        "broken_code_text": '''pepper = os.environ["APP_PEPPER"]''',
        "symptom_text": "KeyError crash when unset",
        "task_list": ["Safer read", "Fail closed?", "Clear message"],
        "model_answer_text": "Use os.environ.get and raise a clear config error if a required secret is missing.",
    },
    {
        "id": "EX25",
        "title": ".env committed to git",
        "level": "Advanced",
        "broken_code_text": '''git add .env && git commit -m "config"''',
        "symptom_text": "Secret exposure risk",
        "task_list": ["Immediate actions", "Repo controls", "Prevention"],
        "model_answer_text": "Rotate secrets, stop tracking .env, add .gitignore, protect main branch.",
    },
    {
        "id": "EX26",
        "title": "No feature branch workflow",
        "level": "Advanced",
        "broken_code_text": '''# all experiments committed on main''',
        "symptom_text": "No safe experimentation lane",
        "task_list": ["Describe safer flow", "PR value", "Main protection"],
        "model_answer_text": "Develop on feature branch, review, then merge. Keep main protected and stable.",
    },
    {
        "id": "EX27",
        "title": "Termux clipboard hard dependency",
        "level": "Advanced",
        "broken_code_text": '''subprocess.run(["termux-clipboard-set", result], check=True)''',
        "symptom_text": "Fails on desktop Linux",
        "task_list": ["Portability issue", "Fallback design", "Detection idea"],
        "model_answer_text": "Wrap clipboard call in try/except and fall back to manual copy on non-Termux systems.",
    },
    {
        "id": "EX28",
        "title": "HMAC with public key material",
        "level": "Advanced",
        "broken_code_text": '''hmac.new(b"public", message_bytes, hashlib.sha3_512)''',
        "symptom_text": "Weak binding to secret state",
        "task_list": ["Why key matters", "Where key should come from", "Fix direction"],
        "model_answer_text": "HMAC key should come from secret internal material, not a public constant.",
    },
    {
        "id": "EX29",
        "title": "Logging passphrase",
        "level": "Advanced",
        "broken_code_text": '''logger.info("passphrase=%s", passphrase_text)''',
        "symptom_text": "Secret lands in logs",
        "task_list": ["Risk", "What may be logged", "Safe policy"],
        "model_answer_text": "Never log secrets. Log events only, not secret values.",
    },
    {
        "id": "EX30",
        "title": "Using random for security salt",
        "level": "Advanced",
        "broken_code_text": '''import random
salt_number = random.randint(0, 10**18)''',
        "symptom_text": "Not cryptographically secure",
        "task_list": ["Why wrong?", "What to use?", "Where random is okay"],
        "model_answer_text": "Use secrets for security-sensitive randomness. random is only for non-security tasks.",
    },
    {
        "id": "EX31",
        "title": "Force push on shared main",
        "level": "Advanced",
        "broken_code_text": '''git push --force origin main''',
        "symptom_text": "Shared history can be destroyed",
        "task_list": ["Risk to collaborators", "Safer alternative", "Policy"],
        "model_answer_text": "Avoid force push on shared main. Use pull requests and branch protection.",
    },
    {
        "id": "EX32",
        "title": "Unpinned dependencies",
        "level": "Advanced",
        "broken_code_text": '''# requirements.txt
streamlit
argon2-cffi''',
        "symptom_text": "Reproducibility and supply risk",
        "task_list": ["Why pin?", "How to pin", "Update strategy"],
        "model_answer_text": "Pin versions for reproducibility and update intentionally after testing.",
    },
    {
        "id": "EX33",
        "title": "Bare except pass",
        "level": "Advanced",
        "broken_code_text": '''try:
    risky_work()
except:
    pass''',
        "symptom_text": "Failures become invisible",
        "task_list": ["Why bad?", "Better pattern", "User messaging"],
        "model_answer_text": "Catch specific exceptions, show or log a clear message, and fail visibly when needed.",
    },
    {
        "id": "EX34",
        "title": "Hard truncation splits emoji",
        "level": "Advanced",
        "broken_code_text": '''path_text = path_text[:500]''',
        "symptom_text": "Unicode segment can break",
        "task_list": ["Why hard cut fails", "Safer approach", "Validation idea"],
        "model_answer_text": "Hard cuts can split multi-codepoint characters. Truncate on path segment boundaries instead.",
    },
    {
        "id": "EX35",
        "title": "Hardcoded shared pepper for all users",
        "level": "Advanced",
        "broken_code_text": '''PEPPER = b"one_global_pepper_for_everyone"''',
        "symptom_text": "Cross-user secret concentration",
        "task_list": ["Architecture issue", "Better storage", "Return policy"],
        "model_answer_text": "Do not hardcode shared pepper in source. Use external secret storage and return only needed values.",
    },
    {
        "id": "EX36",
        "title": "CLI threat model used for public web",
        "level": "Master",
        "broken_code_text": '''# same trust assumptions for local Termux CLI and public Streamlit app''',
        "symptom_text": "Missing web abuse controls",
        "task_list": ["Compare threat models", "Controls for each", "What transfers"],
        "model_answer_text": "Local CLI and public web have different threats. Web needs rate limiting, stronger input validation, and stricter secret handling.",
    },
    {
        "id": "EX37",
        "title": "Malicious PR merged without audit",
        "level": "Master",
        "broken_code_text": '''# merge "cleanup" PR without reading every changed line''',
        "symptom_text": "Possible secret exfiltration",
        "task_list": ["What to inspect", "High-risk patterns", "Process control"],
        "model_answer_text": "Review every line for network calls, secret reads, and unexpected files. Protect main and require review.",
    },
    {
        "id": "EX38",
        "title": "Overstated obfuscation claims",
        "level": "Master",
        "broken_code_text": '''# README: emoji noise = cryptographic strength''',
        "symptom_text": "Misleading security claim",
        "task_list": ["Separate claims", "Evidence standard", "Ethical rewrite"],
        "model_answer_text": "Obfuscation is not cryptographic strength. Say noise is obfuscation only; real strength is CSPRNG, KDF, and secrets.",
    },
    {
        "id": "EX39",
        "title": "No fingerprintability test plan",
        "level": "Master",
        "broken_code_text": '''# no method to test whether outputs are easy to detect''',
        "symptom_text": "Unknown detectability",
        "task_list": ["Define metrics", "Experiment design", "Mitigation loop"],
        "model_answer_text": "Measure structural invariants across outputs, test detectability, then randomize non-essential patterns.",
    },
    {
        "id": "EX40",
        "title": "Passphrase retained in many places",
        "level": "Master",
        "broken_code_text": '''# passphrase copied into many variables and UI widgets''',
        "symptom_text": "Longer exposure window",
        "task_list": ["Exposure points", "Minimization strategy", "UI guidance"],
        "model_answer_text": "Minimize copies, avoid logs, show once, and make the user responsible for safe storage.",
    },
    {
        "id": "EX41",
        "title": "Argon2id migration design",
        "level": "Master",
        "broken_code_text": '''# PBKDF2 only, no upgrade notes''',
        "symptom_text": "Unclear hardening path",
        "task_list": ["Benefits", "Compatibility concerns", "Parameter notes"],
        "model_answer_text": "Argon2id is memory-hard and stronger against GPU attacks. Document parameters and reproducibility notes.",
    },
    {
        "id": "EX42",
        "title": "Weak research packaging",
        "level": "Master",
        "broken_code_text": '''# no pinned deps, no version tag, no checksum''',
        "symptom_text": "Weak artifact integrity",
        "task_list": ["Package requirements", "Integrity controls", "Release checklist"],
        "model_answer_text": "Pin dependencies, tag releases, provide checksums, and document exact run steps.",
    },
    {
        "id": "EX43",
        "title": "Dangerous README guidance",
        "level": "Master",
        "broken_code_text": '''# README tells users to paste seed phrases into online forms''',
        "symptom_text": "Social-engineering risk",
        "task_list": ["Unsafe advice", "Safe rewrite", "Why users fall for it"],
        "model_answer_text": "Never ask for seeds online. Emphasize offline use, small test amounts, and password-manager storage.",
    },
    {
        "id": "EX44",
        "title": "Clipboard privacy assumption",
        "level": "Master",
        "broken_code_text": '''# assume clipboard is always private''',
        "symptom_text": "Clipboard malware ignored",
        "task_list": ["Threat variance", "Mitigations", "UX tradeoff"],
        "model_answer_text": "Clipboard can be sniffed. Offer manual copy and warn on shared devices.",
    },
    {
        "id": "EX45",
        "title": "Incomplete secret incident response",
        "level": "Master",
        "broken_code_text": '''# only delete leaked file from repo''',
        "symptom_text": "Incomplete response",
        "task_list": ["Incident steps", "Technical vs operational", "Communication"],
        "model_answer_text": "Rotate and revoke secrets, audit history/logs, notify if needed, and prevent repeat with ignore rules and scanning.",
    },
    {
        "id": "EX46",
        "title": "API returns full internal state",
        "level": "Master",
        "broken_code_text": '''return {"salt": salt_bytes, "stretched": stretched_bytes, "debug": everything}''',
        "symptom_text": "Unnecessary secret spread",
        "task_list": ["API redesign", "Return minimization", "Test strategy"],
        "model_answer_text": "Return only required outputs. Keep internal state private. Test that UI-facing returns contain no secrets.",
    },
    {
        "id": "EX47",
        "title": "False non-determinism claim",
        "level": "Master",
        "broken_code_text": '''# test seed left enabled in release build''',
        "symptom_text": "Outputs become predictable in release",
        "task_list": ["How to verify", "Test harness", "Release gate"],
        "model_answer_text": "Run many generations and assert diversity. Ensure test-only seeds cannot ship enabled.",
    },
    {
        "id": "EX48",
        "title": "Hybrid loop + security bug",
        "level": "Master",
        "broken_code_text": '''flat_list.extend(list(one_token))
print("selected noise:", chosen_noise)''',
        "symptom_text": "Broken tokens plus leakage",
        "task_list": ["Identify both bug classes", "Patch both", "Explain interaction"],
        "model_answer_text": "Use safe flatten that keeps whole tokens, and never log secret-adjacent selected material.",
    },
    {
        "id": "EX49",
        "title": "Defense-in-depth map for Code N2",
        "level": "Master",
        "broken_code_text": '''# only focus on emojis as protection''',
        "symptom_text": "Shallow defense",
        "task_list": ["List layered controls", "Map to files", "Residual risks"],
        "model_answer_text": "Layers: CSPRNG, hidden salt, KDF, optional passphrase, structural unpredictability, repo hygiene. Residual risks include user backup failure and endpoint malware.",
    },
    {
        "id": "EX50",
        "title": "Research mini-proposal for path generator claims",
        "level": "Master",
        "broken_code_text": '''# no evaluation criteria for security claims''',
        "symptom_text": "Not research-grade",
        "task_list": ["Research question", "Methods", "Threat model", "Metrics", "Ethics"],
        "model_answer_text": "Ask how detectable and usable custom paths are. Use structural tests, compatibility tests, and recovery-error tests. Never collect real seeds or encourage real-fund risk.",
    },
]

