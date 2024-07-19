import pandas as pd
from pygris.data import get_census

def acs_extract(yr, variables, renamed, state_abbr, custom_func=None):

    # Get ACS data by state
    acs_data = get_census(dataset='acs/acs5', 
        year=yr, 
        variables=variables, 
        params = {
            "for": "state:*"
        })
    
    acs_df = pd.DataFrame(acs_data)

    #rename columns to be more 
    rename_dict = dict(zip(variables, renamed))
    rename_dict['state'] = 'state_fips'
    acs_df.rename(columns=rename_dict, inplace=True)
    
    # Convert columns to integers
    numeric_columns = [col for col in acs_df.columns if col not in ['state_fips']]
    acs_df[numeric_columns] = acs_df[numeric_columns].astype(int)

    print(acs_df)

    # Map state FIPS codes to state names
    acs_df['state'] = acs_df['state_fips'].map(state_abbr)

    acs_df['year'] = yr
    cols = ['year'] + ['state'] + [col for col in acs_df.columns if col not in ['year', 'state']]
    acs_df = acs_df[cols]

    #specific function for data being used on acs_df
    if custom_func is not None:
        acs_df = custom_func(acs_df)

    return acs_df