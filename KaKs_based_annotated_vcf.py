import sys

def parse_vcf(vcf_file_path):
    """ Parse the VCF file to count synonymous and non-synonymous variants per gene. """
    gene_variants = {}

    with open(vcf_file_path, 'r') as file:
        for line in file:
            if not line.startswith('#'):  # Skip header lines
                parts = line.split('\t')
                if len(parts) > 7:  # Ensure there are enough columns
                    gene_id = parts[2]  # Assuming the gene name is in the ID column
                    info_column = parts[7]
                    if gene_id not in gene_variants:
                        gene_variants[gene_id] = {'synonymous': 0, 'nonsynonymous': 0}
                    
                    if 'synonymous' in info_column:
                        gene_variants[gene_id]['synonymous'] += 1
                    if 'nonsynonymous' in info_column:
                        gene_variants[gene_id]['nonsynonymous'] += 1

    return gene_variants

def calculate_kaks_per_gene(gene_variants):
    """ Calculate the Dn, Ds, and Dn/Ds ratio for each gene. """
    for gene, counts in gene_variants.items():
        dn = counts['nonsynonymous']
        ds = counts['synonymous']
        if ds > 0:
            dn_ds_ratio = dn / ds
        else:
            dn_ds_ratio = float('inf')  # To handle division by zero if no synonymous variants are present
        
        print(f"Gene: {gene}")
        print(f"Dn (Nonsynonymous substitutions): {dn}")
        print(f"Ds (Synonymous substitutions): {ds}")
        print(f"Dn/Ds ratio: {dn_ds_ratio}")
        print("----------")

def main(vcf_file_path):
    gene_variants = parse_vcf(vcf_file_path)
    calculate_kaks_per_gene(gene_variants)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python kaks_ratio.py <vcf_file_path>")
        sys.exit(1)
    main(sys.argv[1])
