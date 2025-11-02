import re

# Read clean version and extract AD numbers
with open('/home/ubuntu/canima/AD_PARAGRAPHS_FROM_CLEAN_VERSION.txt', 'r') as f:
    clean_content = f.read()

clean_ads = []
for line in clean_content.split('\n'):
    match = re.match(r'^\d+\.\s+AD\s+(\d+(?:\.\d+)*)', line.strip())
    if match:
        clean_ads.append(match.group(1))

# Read PDF version and extract AD numbers  
with open('/home/ubuntu/canima/AD_PARAGRAPHS_FROM_PDF.txt', 'r') as f:
    pdf_content = f.read()

pdf_ads = []
for line in pdf_content.split('\n'):
    match = re.match(r'^(\d+(?:\.\d+)*):', line.strip())
    if match:
        ad_num = match.group(1)
        # Filter out ID numbers (6+ digits)
        if len(ad_num.replace('.', '')) < 6:
            pdf_ads.append(ad_num)

print(f"Clean version: {len(clean_ads)} AD paragraphs")
print(f"PDF version: {len(pdf_ads)} AD paragraphs")
print()

# Compare sets
clean_set = set(clean_ads)
pdf_set = set(pdf_ads)

only_in_clean = clean_set - pdf_set
only_in_pdf = pdf_set - clean_set

if only_in_clean:
    print(f"AD paragraphs ONLY in clean version ({len(only_in_clean)}):")
    for ad in sorted(only_in_clean, key=lambda x: [int(n) for n in x.split('.')]):
        print(f"  - AD {ad}")
    print()

if only_in_pdf:
    print(f"AD paragraphs ONLY in PDF version ({len(only_in_pdf)}):")
    for ad in sorted(only_in_pdf, key=lambda x: [int(n) for n in x.split('.')]):
        print(f"  - AD {ad}")
    print()

if not only_in_clean and not only_in_pdf:
    print("✅ Both versions contain the SAME AD paragraphs!")
    print()
    print("Verifying order...")
    if clean_ads == pdf_ads:
        print("✅ Both versions have the SAME ORDER!")
    else:
        print("⚠️  Order differs between versions")
        print()
        print("First 10 in clean version:", clean_ads[:10])
        print("First 10 in PDF version:", pdf_ads[:10])

# Save detailed report
with open('/home/ubuntu/canima/AD_COMPARISON_CLEAN_VS_PDF_V2.txt', 'w') as f:
    f.write("AD Paragraph Comparison: Clean Version vs PDF Extraction\n")
    f.write("=" * 70 + "\n\n")
    f.write(f"Clean version: {len(clean_ads)} AD paragraphs\n")
    f.write(f"PDF version: {len(pdf_ads)} AD paragraphs\n\n")
    
    if only_in_clean:
        f.write(f"AD paragraphs ONLY in clean version ({len(only_in_clean)}):\n")
        for ad in sorted(only_in_clean, key=lambda x: [int(n) for n in x.split('.')]):
            f.write(f"  - AD {ad}\n")
        f.write("\n")
    
    if only_in_pdf:
        f.write(f"AD paragraphs ONLY in PDF version ({len(only_in_pdf)}):\n")
        for ad in sorted(only_in_pdf, key=lambda x: [int(n) for n in x.split('.')]):
            f.write(f"  - AD {ad}\n")
        f.write("\n")
    
    if not only_in_clean and not only_in_pdf:
        f.write("✅ Both versions contain the SAME AD paragraphs!\n\n")
        if clean_ads == pdf_ads:
            f.write("✅ Both versions have the SAME ORDER!\n")
        else:
            f.write("⚠️  Order differs between versions\n")

print("Detailed comparison saved to AD_COMPARISON_CLEAN_VS_PDF_V2.txt")
