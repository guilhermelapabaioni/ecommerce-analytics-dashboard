import numpy as np
import random

def fillm(df, mcolumn, auxcolumn, get_dummies=False):
    """_summary_
        Function created to fill in missing values with the mode.
        Use fill_dummies() to fill the missing values without previous characteristics.
        Arguments:
        df (_type_): DataFrame
        mcolumn (_type_): Column with missing values.
        auxcolumn (_type_): Column used to assist the column with missing values. Used for grouping.
    """
    df[mcolumn] = df[mcolumn].fillna(
        df.groupby(auxcolumn)[mcolumn].transform(
            lambda x: x.mode()[0] if not x.mode().empty else np.nan
        )
    )
    
    if get_dummies:
        fill_dummies(df, mcolumn, auxcolumn)
    
    print(f'Process has been concluded. The column {mcolumn} has {df[mcolumn].isnull().sum()} missing values.')
    
    return df
    
def fill_dummies(df, mcolumn, auxcolumn):
    """_summary_
    Function create to fill dummies values without base values. For numeric dtypes it will fill with a random number between 999 and 9999, and object dtype will fill with "Verificar".
    Args:
        df (_type_): DataFrame
        mcolumn (_type_): Column with dummies values.
        auxcolumn (_type_): Column used to assist the column with dummies values.
    """
    numeric_dtype = df[mcolumn].dtype in ('int64', 'float64')
    
    if numeric_dtype:
        dummies = df.loc[df[mcolumn].isna(), auxcolumn].unique()
        for v in dummies:
            mask = (df[auxcolumn] == v) & (df[mcolumn].isna())
            df.loc[mask, mcolumn] = np.random.randint(999, 9999)
    else:
        mask = df[mcolumn].isna()
        df.loc[mask, mcolumn] = 'Verificar'
        
    return df