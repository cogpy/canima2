import re

# Read PDF paragraphs
pdf_paras = set()
with open('/home/ubuntu/canima/AD_PARAGRAPHS_FROM_PDF.txt', 'r') as f:
    for line in f:
        if ':' in line:
            para_num = line.split(':')[0].strip()
            if re.match(r'^\d+(\.\d+)*$', para_num) and para_num not in ['570607', '5300']:
                pdf_paras.add(para_num)

print(f"Total valid AD paragraphs in PDF: {len(pdf_paras)}")

# Identify potential issues in Jacqueline's affidavit
jax_issues = []

# Check for invalid paragraph numbers in Jacqueline's affidavit
invalid_refs_jax = ['10.7.1.4', '10.10.22', '10.10.41', '10.10.2.4']

for ref in invalid_refs_jax:
    if ref not in pdf_paras:
        jax_issues.append(f"INVALID: {ref} does not exist in Founding Affidavit")

# Write detailed discrepancy report
with open('/home/ubuntu/canima/AD_DISCREPANCY_REPORT.md', 'w') as f:
    f.write("# AD Paragraph Discrepancy Report\n\n")
    f.write("## Critical Findings\n\n")
    
    if jax_issues:
        f.write("### Jacqueline's Affidavit - Invalid AD Paragraph References\n\n")
        f.write("The following AD paragraph references in Jacqueline's affidavit **DO NOT EXIST** in Peter's Founding Affidavit:\n\n")
        for issue in jax_issues:
            f.write(f"- {issue}\n")
        
        f.write("\n#### Analysis\n\n")
        f.write("These appear to be **typos or incorrect references**. The correct paragraphs should be:\n\n")
        f.write("- `10.7.1.4` → Should likely be `10.7.1.2` (the only 10.7.1.x paragraph in the PDF)\n")
        f.write("- `10.10.22` → Should likely be `10.10.2.2` (missing decimal point)\n")
        f.write("- `10.10.41` → Should likely be `10.10.2.1` (typo: 41 instead of 2.1)\n")
        f.write("- `10.10.2.4` → Does not exist; should be `10.10.2.3` (last sub-paragraph is 10.10.2.3)\n\n")
    
    f.write("## Coverage Analysis\n\n")
    f.write("### Major Sections in Founding Affidavit\n\n")
    f.write("1. **Introduction (1.1-1.3)** - Applicant's identity and oath\n")
    f.write("2. **Applicant (2.1-2.4)** - Applicant's standing\n")
    f.write("3. **Identification of Respondents (3.1-3.13)** - All parties\n")
    f.write("4. **Jurisdiction (4)** - Court jurisdiction\n")
    f.write("5. **Locus Standi (5)** - Standing to bring application\n")
    f.write("6. **Relationships (6.1-6.5)** - Corporate structure\n")
    f.write("7. **Discovery of Financial Irregularities (7.1-7.20)** - Allegations of misconduct\n")
    f.write("8. **IT Expenses Analysis (8.1-8.10)** - Financial details\n")
    f.write("9. **Substantial Financial Misconduct (9.1-9.4)** - Core allegations\n")
    f.write("10. **Delinquency and Probation Application (10.1-10.13)** - Legal grounds\n")
    f.write("11. **UK Operations (11.1-11.9)** - International operations\n")
    f.write("12. **Necessity of Relief (12.1-12.4)** - Urgency arguments\n")
    f.write("13. **Interdicts Sought (13.1-13.7)** - Interdict requirements\n")
    f.write("14. **Other Relief Sought (14.1-14.5)** - Additional relief\n")
    f.write("15. **Urgency (16.1-16.12)** - Urgency justification\n")
    f.write("16. **Ex Parte Basis (17.1-17.4)** - Ex parte justification\n\n")
    
    f.write("### Sections 4, 5, and 15 Not Addressed\n\n")
    f.write("**NOTE:** The refined affidavits do not explicitly address:\n")
    f.write("- **Section 4 (Jurisdiction)** - This is typically not disputed\n")
    f.write("- **Section 5 (Locus Standi)** - This is typically not disputed\n")
    f.write("- **Section 15** - This section does not exist in the PDF (jumps from 14 to 16)\n\n")
    
    f.write("## Recommendations\n\n")
    f.write("1. **Correct the invalid AD paragraph references in Jacqueline's affidavit**\n")
    f.write("2. **Consider whether Sections 4 and 5 need explicit responses** (typically not required)\n")
    f.write("3. **Verify all range references** (e.g., \"7-7.20\") cover all paragraphs in that range\n")

print("\nDetailed discrepancy report written to AD_DISCREPANCY_REPORT.md")
print("\nInvalid references found in Jacqueline's affidavit:")
for issue in jax_issues:
    print(f"  - {issue}")
