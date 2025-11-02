import re

# Read the cleaner text version
with open('/home/ubuntu/upload/pasted_content.txt', 'r') as f:
    content = f.read()

# Extract all AD paragraph numbers
ad_pattern = r'^AD\s+(\d+(?:\.\d+)*)\s*$'
ad_numbers = []

for line in content.split('\n'):
    match = re.match(ad_pattern, line.strip())
    if match:
        ad_numbers.append(match.group(1))

# Write to file
with open('/home/ubuntu/canima/AD_PARAGRAPHS_FROM_CLEAN_VERSION.txt', 'w') as f:
    f.write("AD Paragraphs from Clean Text Version\n")
    f.write("=" * 50 + "\n\n")
    for i, num in enumerate(ad_numbers, 1):
        f.write(f"{i}. AD {num}\n")
    f.write(f"\nTotal AD paragraphs: {len(ad_numbers)}\n")

print(f"Extracted {len(ad_numbers)} AD paragraphs from clean version")
print(f"Saved to AD_PARAGRAPHS_FROM_CLEAN_VERSION.txt")
