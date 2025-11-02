import re

# Read the extracted text
with open('/home/ubuntu/canima/founding_affidavit/affidavit_extracted.txt', 'r') as f:
    text = f.read()

# Extract all paragraph numbers (e.g., 1.1, 7.16, 10.5.1, etc.)
pattern = r'^\s*(\d+(?:\.\d+)*)\s+'
paragraphs = []

for line in text.split('\n'):
    match = re.match(pattern, line)
    if match:
        para_num = match.group(1)
        # Get the rest of the line as the heading/content
        content = line[match.end():].strip()
        paragraphs.append((para_num, content))

# Write to output file
with open('/home/ubuntu/canima/AD_PARAGRAPHS_FROM_PDF.txt', 'w') as f:
    f.write("AD PARAGRAPH NUMBERS EXTRACTED FROM FOUNDING AFFIDAVIT PDF\n")
    f.write("=" * 80 + "\n\n")
    for para_num, content in paragraphs:
        # Limit content to first 100 chars for readability
        content_preview = content[:100] + "..." if len(content) > 100 else content
        f.write(f"{para_num}: {content_preview}\n")
    f.write(f"\n\nTotal paragraphs found: {len(paragraphs)}\n")

print(f"Extracted {len(paragraphs)} paragraphs")
print("First 20 paragraphs:")
for para_num, content in paragraphs[:20]:
    content_preview = content[:80] + "..." if len(content) > 80 else content
    print(f"  {para_num}: {content_preview}")
