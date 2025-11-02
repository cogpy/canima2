#!/usr/bin/env python3.11

import re

# Load the 141 valid AD paragraphs
with open('/home/ubuntu/canima/AD_PARAGRAPHS_FROM_CLEAN_VERSION.txt', 'r') as f:
    valid_ads = set(line.strip().replace('AD ', '') for line in f if line.strip())

# Load Jacqueline's v8 affidavit
with open('/home/ubuntu/canima/affidavits_refined/Jacqueline_Answering_Affidavit_v8_JR.md', 'r') as f:
    jax_content = f.read()

# Load Daniel's v8 affidavit
with open('/home/ubuntu/canima/affidavits_refined/Daniel_Answering_Affidavit_v8_DR.md', 'r') as f:
    dan_content = f.read()

# Extract JR and DR references
jr_pattern = r'\*\*JR (\d+(?:\.\d+)*(?:\.\d+)?)\*\*'
dr_pattern = r'\*\*DR (\d+(?:\.\d+)*(?:\.\d+)?)\*\*'

jr_refs = set(re.findall(jr_pattern, jax_content))
dr_refs = set(re.findall(dr_pattern, dan_content))

print("=== V8 AFFIDAVIT COVERAGE VERIFICATION ===\n")
print(f"Total valid AD paragraphs: {len(valid_ads)}")
print(f"JR references found: {len(jr_refs)}")
print(f"DR references found: {len(dr_refs)}")
print()

# Check which AD paragraphs are covered
covered_by_jr = jr_refs & valid_ads
covered_by_dr = dr_refs & valid_ads
covered_by_both = covered_by_jr & covered_by_dr
covered_by_either = covered_by_jr | covered_by_dr

print(f"AD paragraphs covered by JR: {len(covered_by_jr)}")
print(f"AD paragraphs covered by DR: {len(covered_by_dr)}")
print(f"AD paragraphs covered by both: {len(covered_by_both)}")
print(f"AD paragraphs covered by either: {len(covered_by_either)}")
print()

# Find uncovered AD paragraphs
uncovered = valid_ads - covered_by_either
if uncovered:
    print(f"UNCOVERED AD PARAGRAPHS ({len(uncovered)}):")
    for ad in sorted(uncovered, key=lambda x: [int(n) if n.isdigit() else n for n in re.split(r'(\d+)', x)]):
        print(f"  AD {ad}")
else:
    print("✅ ALL 141 AD PARAGRAPHS COVERED!")

print()

# Save detailed report
with open('/home/ubuntu/canima/V8_COVERAGE_VERIFICATION_REPORT.md', 'w') as f:
    f.write("# V8 Affidavit Coverage Verification Report\n\n")
    f.write(f"**Date:** November 2, 2025\n\n")
    f.write(f"## Summary\n\n")
    f.write(f"- **Total valid AD paragraphs:** {len(valid_ads)}\n")
    f.write(f"- **JR references:** {len(jr_refs)}\n")
    f.write(f"- **DR references:** {len(dr_refs)}\n")
    f.write(f"- **Covered by JR:** {len(covered_by_jr)}\n")
    f.write(f"- **Covered by DR:** {len(covered_by_dr)}\n")
    f.write(f"- **Covered by both:** {len(covered_by_both)}\n")
    f.write(f"- **Covered by either:** {len(covered_by_either)}\n")
    f.write(f"- **Uncovered:** {len(uncovered)}\n\n")
    
    if uncovered:
        f.write(f"## Uncovered AD Paragraphs ({len(uncovered)})\n\n")
        for ad in sorted(uncovered, key=lambda x: [int(n) if n.isdigit() else n for n in re.split(r'(\d+)', x)]):
            f.write(f"- AD {ad}\n")
    else:
        f.write("## ✅ Complete Coverage Achieved\n\n")
        f.write("All 141 AD paragraphs are addressed in the v8 affidavits.\n")

print("Report saved to: V8_COVERAGE_VERIFICATION_REPORT.md")
