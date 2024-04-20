import pandas as pd
import argparse

def extract_genes(file_path):
    """
    Extract gene information from a GFF3 file.

    Parameters:
    file_path (str): The path to the GFF3 file.

    Returns:
    DataFrame: A pandas DataFrame containing gene names and their lengths.
    """
    genes = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            if parts[2] == 'gene':
                attributes = parts[8]
                gene_id = attributes.split(';')[1].split('=')[1]  # Adjust based on your file structure if needed
                start = int(parts[3])
                end = int(parts[4])
                length = end - start + 1
                genes.append({'Gene Name': gene_id, 'Gene Length': length})
    return pd.DataFrame(genes)

def main(args):
    # Extract genes
    gene_data = extract_genes(args.input_file)

    # Output the DataFrame to a CSV file
    gene_data.to_csv(args.output_file, index=False)
    print(f"Data has been saved to {args.output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract genes from a GFF3 file and calculate their lengths.')
    parser.add_argument('-i', '--input_file', required=True, help='Path to the input GFF3 file')
    parser.add_argument('-o', '--output_file', required=True, help='Path to the output CSV file where results will be saved')
    
    args = parser.parse_args()
    main(args)
