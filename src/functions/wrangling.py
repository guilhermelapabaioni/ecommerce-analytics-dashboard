import pandas as pd
import numpy as np

def get_date(df, column, year=False, quarter=False, month=False, day=False, period=False):
    """_summary_

    Args:
        df (_type_): _description_
        column (_type_): _description_
        year (bool, optional): _description_. Defaults to False.
        quarter (bool, optional): _description_. Defaults to False.
        month (bool, optional): _description_. Defaults to False.
        day (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    df[column] = pd.to_datetime(df[column])
    print(f'Column {column} is converted to datetime.')
    
    if year:
        df['Year'] = df[column].dt.year
        
    if quarter:
        df['Quarter'] = df[column].dt.quarter
        
    if month:
        df['Month'] = df[column].dt.month
        
    if day:
        df['Day'] = df[column].dt.day
        
    if period:
        df['Period Date'] = df[column].dt.to_period('M')
    
    return df

def get_total(df, mcolumn, auxcolumn, newcolumn='Total'):
    """
    Docstring for get_total
    
    :param df: Description
    :param mcolumn: Description
    :param auxcolumn: Description
    :param newcolumn: Description
    """
    df[newcolumn] = (df[mcolumn] * df[auxcolumn]).round(2)
    print(f'Column {newcolumn} was created based on {mcolumn, auxcolumn}')
    
    return df

def get_categorial(df, mcolumn, newcolumn, condition, val_true, val_false):
    """
    Docstring for get_categorial
    
    :param df: Description
    :param mcolumn: Description
    :param newcolumn: Description
    :param condition: Description
    :param val_true: Description
    :param val_false: Description
    """
    df[newcolumn] = np.where(df[mcolumn] < condition, val_true, val_false)
    
    return df

def get_binned(df, mcolumn, newcolumn, bins=[], labels=[]):
    df[newcolumn] = pd.cut(df[mcolumn], bins, labels=labels)
    
    return df
    
def new_data(df, mcolumn, method='total', **kwargs):
    """
    Docstring for new_data
    
    :param df: Description
    :param mcolumn: Description
    :param method: Description
    :param kwargs: Description
    """
    df = df.copy()
    try:
        if method == 'total':
            auxcolumn = kwargs.get('auxcolumn')
            newcolumn = kwargs.get('newcolumn')
            
            return get_total(df, mcolumn, auxcolumn, newcolumn)
        
        elif method == 'categorial':
            newcolumn = kwargs.get('newcolumn')
            condition = kwargs.get('condition')
            val_true = kwargs.get('val_true')
            val_false = kwargs.get('val_false')
            
            return get_categorial(df, mcolumn, newcolumn, condition, val_true, val_false)
        
        elif method == 'binned':
            newcolumn = kwargs.get('newcolumn')
            bins = kwargs.get('bins')
            labels = kwargs.get('labels')
            
            return get_binned(df, mcolumn, newcolumn, bins, labels)
        
        else:
            return ValueError(f"Method {method} not recognized. Use 'total' or 'categorial'")
        
    except:
        return ValueError(f"Method {method} not recognized. Use 'total' or 'categorial'")