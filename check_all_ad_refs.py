import re
import os

# Load valid AD paragraphs
with open('/home/ubuntu/canima/AD_PARAGRAPHS_FROM_CLEAN_VERSION.txt', 'r') as f:
    content = f.read()

valid_ads = set()
for line in content.split('\n'):
    match = re.match(r'^\d+\.\s+AD\s+(\d+(?:\.\d+)*)', line.strip())
    if match:
        valid_ads.add(match.group(1))

# Key documents to check
key_docs = [
    './AD_PARAGRAPH_COVERAGE_REPORT.md',
    './LEGAL_ANALYSIS_REPORT_FINAL.md',
    './IMPROVEMENT_RECOMMENDATIONS.md',
    './LEGAL_ASPECTS_ANALYSIS_COMPREHENSIVE.md'
]

print(f"Checking {len(key_docs)} key documents for AD references...")
print(f"Valid AD paragraphs: {len(valid_ads)}")
print()

all_issues = []

for doc_path in key_docs:
    if not os.path.exists(doc_path):
        continue
    
    print(f"Checking: {doc_path}")
    
    with open(doc_path, 'r') as f:
        content = f.read()
    
    # Find all AD references (with at least one decimal point)
    refs = re.findall(r'\bAD\s+(\d+(?:\.\d+)+)\b', content)
    invalid_refs = [r for r in refs if r not in valid_ads]
    
    if invalid_refs:
        print(f"  ⚠️  Found {len(set(invalid_refs))} unique invalid references")
        for ref in sorted(set(invalid_refs), key=lambda x: [int(n) for n in x.split('.')]):
            print(f"    - AD {ref}")
            all_issues.append((doc_path, ref))
    else:
        print(f"  ✅ All references valid ({len(set(refs))} unique)")
    print()

if all_issues:
    print("=" * 70)
    print(f"SUMMARY: Found {len(all_issues)} invalid AD references across documents")
    print("=" * 70)
else:
    print("=" * 70)
    print("✅ ALL AD REFERENCES IN KEY DOCUMENTS ARE VALID!")
    print("=" * 70)
