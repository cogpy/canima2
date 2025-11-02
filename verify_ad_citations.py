import re

# Load valid AD paragraphs
with open('/home/ubuntu/canima/AD_PARAGRAPHS_FROM_CLEAN_VERSION.txt', 'r') as f:
    content = f.read()

valid_ads = set()
for line in content.split('\n'):
    match = re.match(r'^\d+\.\s+AD\s+(\d+(?:\.\d+)*)', line.strip())
    if match:
        valid_ads.add(match.group(1))

print(f"Loaded {len(valid_ads)} valid AD paragraphs")
print()

def check_affidavit(filepath, name):
    print("=" * 70)
    print(f"CHECKING: {name}")
    print("=" * 70)
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find AD citations in text (not headers)
    # Pattern: "AD X.Y" or "AD X.Y.Z" in regular text
    citations = []
    invalid_citations = []
    
    # Look for AD references in paragraphs (not headers)
    for line in content.split('\n'):
        # Skip markdown headers
        if line.strip().startswith('#'):
            continue
        
        # Find AD references in text
        for match in re.finditer(r'\bAD\s+(\d+(?:\.\d+)+)\b', line):
            ad_num = match.group(1)
            citations.append(ad_num)
            if ad_num not in valid_ads:
                invalid_citations.append((ad_num, line.strip()[:100]))
    
    print(f"Total AD citations in text: {len(citations)}")
    print(f"Unique AD citations: {len(set(citations))}")
    print(f"Invalid citations: {len(set([c[0] for c in invalid_citations]))}")
    
    if invalid_citations:
        print("\nInvalid citations found:")
        seen = set()
        for ad_num, context in invalid_citations:
            if ad_num not in seen:
                print(f"\n  - AD {ad_num}")
                print(f"    Context: {context}...")
                seen.add(ad_num)
    else:
        print("✅ All AD citations are VALID!")
    
    print()
    return citations, invalid_citations

# Check both affidavits
jax_cites, jax_invalid = check_affidavit(
    '/home/ubuntu/canima/affidavits_refined/Jacqueline_Answering_Affidavit_v7_Refined.md',
    "Jacqueline's Answering Affidavit v7 Refined"
)

dan_cites, dan_invalid = check_affidavit(
    '/home/ubuntu/canima/affidavits_refined/Daniel_Answering_Affidavit_v7_Refined.md',
    "Daniel's Answering Affidavit v7 Refined"
)

# Generate report
with open('/home/ubuntu/canima/AD_CITATIONS_VERIFICATION_REPORT.md', 'w') as f:
    f.write("# AD Citations Verification Report\n\n")
    f.write("**Date:** November 2, 2025\n")
    f.write("**Scope:** AD paragraph citations in body text (excluding section headers)\n\n")
    f.write("---\n\n")
    
    f.write("## Jacqueline's Answering Affidavit v7 Refined\n\n")
    f.write(f"- **Total AD citations:** {len(jax_cites)}\n")
    f.write(f"- **Unique AD citations:** {len(set(jax_cites))}\n")
    f.write(f"- **Invalid citations:** {len(set([c[0] for c in jax_invalid]))}\n\n")
    
    if jax_invalid:
        f.write("### Invalid Citations\n\n")
        seen = set()
        for ad_num, context in jax_invalid:
            if ad_num not in seen:
                f.write(f"**AD {ad_num}**\n\n")
                f.write(f"Context: `{context}...`\n\n")
                seen.add(ad_num)
    else:
        f.write("✅ **All AD citations are VALID!**\n\n")
    
    f.write("---\n\n")
    
    f.write("## Daniel's Answering Affidavit v7 Refined\n\n")
    f.write(f"- **Total AD citations:** {len(dan_cites)}\n")
    f.write(f"- **Unique AD citations:** {len(set(dan_cites))}\n")
    f.write(f"- **Invalid citations:** {len(set([c[0] for c in dan_invalid]))}\n\n")
    
    if dan_invalid:
        f.write("### Invalid Citations\n\n")
        seen = set()
        for ad_num, context in dan_invalid:
            if ad_num not in seen:
                f.write(f"**AD {ad_num}**\n\n")
                f.write(f"Context: `{context}...`\n\n")
                seen.add(ad_num)
    else:
        f.write("✅ **All AD citations are VALID!**\n\n")
    
    f.write("---\n\n")
    f.write("## Summary\n\n")
    total_invalid = len(set([c[0] for c in jax_invalid + dan_invalid]))
    if total_invalid == 0:
        f.write("✅ **VERIFICATION COMPLETE: All AD citations in both affidavits are valid!**\n")
    else:
        f.write(f"⚠️  **Total unique invalid citations:** {total_invalid}\n")

print("=" * 70)
print("Citation verification report saved to: AD_CITATIONS_VERIFICATION_REPORT.md")
print("=" * 70)
