import pandas as pd

def clean_dataset(df, method):

    if df is None:
        return None

    cleaned_df = df.copy()

    for col in cleaned_df.columns:

        if cleaned_df[col].isnull().sum() > 0:

            if pd.api.types.is_numeric_dtype(cleaned_df[col]):

                if method == "Mean":
                    cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].mean())

                elif method == "Median":
                    cleaned_df[col] = cleaned_df[col].fillna(cleaned_df[col].median())

                elif method == "Mode":
                    mode_val = cleaned_df[col].mode()
                    if not mode_val.empty:
                        cleaned_df[col] = cleaned_df[col].fillna(mode_val[0])

            else:
                mode_val = cleaned_df[col].mode()
                if not mode_val.empty:
                    cleaned_df[col] = cleaned_df[col].fillna(mode_val[0])

    if method == "Drop Rows":
        cleaned_df = cleaned_df.dropna()

    cleaned_df = cleaned_df.drop_duplicates()

    return cleaned_df