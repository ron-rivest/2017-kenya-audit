"""
Change results to bias one candidate 
"""
import pandas as pd
import argparse

def parse(input_file, output_file, preferred_canddiate, bias, n_sites):
    input_df = pd.read_csv(input_file)
    if not ( preferred_canddiate  in input_df.columns):
        raise ValueError("Specified candidate must be in input csv.")
    if bias <= 0:
        raise ValueError("Bias must be a positive float.")
    input_df[preferred_canddiate] = input_df[preferred_canddiate].apply(lambda x: int(x*bias))  
    input_df = input_df.sample(frac=1)
    output_df = input_df.head(n_sites)
    output_df = output_df.drop(['Number voters', 'County ID'], 1)
    output_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert csv file into the format for audit code.')
    parser.add_argument('--sites_csv', type=str,
                        help="""Sites csv file""", required=True)
    parser.add_argument('--output_audit_file', type=str,
                        help="""A csv file with the output format used for the audit code""", required=False)
    parser.add_argument('--preferred_candidate', type=str,
                        help="""Candidate to increase votes for""", required=True)
    parser.add_argument('--bias', type=float,
                        help="""Percent to increase for candidate""", required=False)
    parser.add_argument('--n_sites', type=int,
                        help="""Number of sites to include""", required=False)

    parser.set_defaults(output_audit_file='audit.csv')
    parser.set_defaults(bias=1.2)
    parser.set_defaults(n_sites=1000)

    args = parser.parse_args()
    parse(args.sites_csv, args.output_audit_file, args.preferred_candidate, args.bias, args.n_sites)
