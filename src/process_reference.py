from  argparse import ArgumentParser
import subprocess, json, yaml

def parse_args():
    parser = ArgumentParser(description = "Process and move files")
    parser.add_argument('-f', '--filename', required = True, help = "zipped genome filepath")
    parser.add_argument('-s', '--species', required = True, help = "species name")
    return parser.parse_args()

def main():
    args = parse_args()
    filename, species = args.filename, args.species
    
    # unzip the file and auto input 'no' to replace README prompt
    subprocess.run(f'echo "n" | unzip {filename}', shell = True)
    with open('ncbi_dataset/data/dataset_catalog.json') as dataset_catalog, open(f'configs/config_{species}.yaml') as config_file: 
        parsed_dataset = json.load(dataset_catalog)
        config_file = yaml.safe_load(config_file)
    
    data_dir = config_file['data_directory']
    fa_filepath = f"ncbi_dataset/data/{parsed_dataset['assemblies'][2]['files'][0]['filePath']}"
    subprocess.run(
        f"""
        cp {fa_filepath} {data_dir}/{species}/{species}.fa
        echo "File has been moved and renamed to {species}.fa"
        rm -r ncbi_dataset
        cd {data_dir}/{species}
        samtools faidx {species}.fa
        bwa index -p {species} {species}.fa
        """, shell = True
    )

if __name__ == "__main__":
    main()