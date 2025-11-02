import re
from collections import defaultdict

# Read the PDF-extracted paragraphs
with open('/home/ubuntu/canima/AD_PARAGRAPHS_FROM_PDF.txt', 'r') as f:
    pdf_content = f.read()

# Extract valid paragraph numbers from PDF (excluding false positives like ID numbers)
pdf_paragraphs = set()
for line in pdf_content.split('\n'):
    if ':' in line:
        para_num = line.split(':')[0].strip()
        # Filter out ID numbers and other false positives
        if para_num and not para_num.isdigit() or (para_num.isdigit() and int(para_num) < 100):
            # Only include if it looks like a proper paragraph number
            if re.match(r'^\d+(\.\d+)*$', para_num) and not para_num in ['570607', '5300']:
                pdf_paragraphs.add(para_num)

print(f"Found {len(pdf_paragraphs)} valid AD paragraphs in PDF")
print("Sample paragraphs:", sorted(list(pdf_paragraphs))[:20])

# Read refined affidavits and extract AD paragraph references
affidavit_files = [
    '/home/ubuntu/canima/affidavits_refined/Daniel_Answering_Affidavit_v7_Refined.md',
    '/home/ubuntu/canima/affidavits_refined/Jacqueline_Answering_Affidavit_v7_Refined.md'
]

referenced_paragraphs = defaultdict(list)

for affidavit_file in affidavit_files:
    try:
        with open(affidavit_file, 'r') as f:
            content = f.read()
        
        # Find AD paragraph references (e.g., "AD 1", "AD 1.3", "AD PARAGRAPH 7.1", etc.)
        patterns = [
            r'AD\s+PARAGRAPH[S]?\s+(\d+(?:\.\d+)*(?:-\d+(?:\.\d+)*)?)',
            r'AD\s+(\d+(?:\.\d+)*)',
            r'#### AD (\d+(?:\.\d+)*)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                # Handle ranges like "7-7.20"
                if '-' in match:
                    parts = match.split('-')
                    referenced_paragraphs[affidavit_file.split('/')[-1]].append(match)
                else:
                    referenced_paragraphs[affidavit_file.split('/')[-1]].append(match)
    except FileNotFoundError:
        print(f"File not found: {affidavit_file}")

# Write comparison report
with open('/home/ubuntu/canima/AD_PARAGRAPH_VERIFICATION_REPORT.md', 'w') as f:
    f.write("# AD Paragraph Verification Report\n\n")
    f.write("## Summary\n\n")
    f.write(f"- **Total AD paragraphs in Founding Affidavit PDF:** {len(pdf_paragraphs)}\n")
    
    for affidavit_name, refs in referenced_paragraphs.items():
        unique_refs = set(refs)
        f.write(f"- **AD paragraph references in {affidavit_name}:** {len(unique_refs)}\n")
    
    f.write("\n## Valid AD Paragraphs from PDF\n\n")
    sorted_paras = sorted(pdf_paragraphs, key=lambda x: [int(p) for p in x.split('.')])
    f.write("```\n")
    for para in sorted_paras:
        f.write(f"{para}\n")
    f.write("```\n\n")
    
    f.write("## AD Paragraph References in Refined Affidavits\n\n")
    for affidavit_name, refs in referenced_paragraphs.items():
        f.write(f"### {affidavit_name}\n\n")
        unique_refs = sorted(set(refs), key=lambda x: [int(p) if p.isdigit() else 0 for p in x.replace('-', '.').split('.')])
        f.write("```\n")
        for ref in unique_refs:
            f.write(f"{ref}\n")
        f.write("```\n\n")

print("\nVerification report written to AD_PARAGRAPH_VERIFICATION_REPORT.md")
