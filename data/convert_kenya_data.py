"""
This script parses the kenya data csv into the correct format for the sites.csv used in the audit code
"""
import pandas as pd
import argparse

def parse(input_file, output_file):
	input_df = pd.read_csv(input_file)
	candidates = [ 'Kenyatta', 'Odinga', 'Nyagah', 'Dida', 'Aukot', 'Kaluyu', 'Jirongo', 'Mwaura']
	output_df = input_df[['POLLING.STATION.CODE','ValidVotes','COUNTY.CODE'] + candidates]
	output_df = output_df.rename(index=str, columns = {'POLLING.STATION.CODE': 'Polling Site ID','ValidVotes':'Number voters', 'COUNTY.CODE': 'County ID'})
	output_df = output_df[['Polling Site ID', 'County ID', 'Number voters']+ candidates]
	
	#remove 0 vote columns
	output_df = output_df[output_df['Number voters']>0]
	output_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert csv file into the format for audit code.')
    parser.add_argument('--unformatted_csv', type=str,
                        help="""CSV file with the kenya result format provided by Prof. Mebane""", required=True)
    parser.add_argument('--output_sites_file', type=str,
                        help="""A csv file with the output format used for the audit code""", required=False)
    parser.set_defaults(output_sites_file='sites.csv')
    args = parser.parse_args()
    parse(args.unformatted_csv, args.output_sites_file)