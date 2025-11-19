import pandas as pd
import numpy as np
import requests
from io import StringIO

def fetch_sunspot_data():
    """从SILSO获取太阳黑子数据（替代数据源）"""
    try:
        print("Fetching sunspot data from SILSO... (this may take 10-15 seconds)")
        url = "http://www.sidc.be/silso/DATA/SN_m_tot_V2.0.csv"
        response = requests.get(url, timeout=15)  # Reduced timeout to 15 seconds
        response.raise_for_status()
        
        data = response.text
        df = pd.read_csv(StringIO(data), sep=';', header=None)
        df.columns = ['year', 'month', 'year_frac', 'sunspot_number', 'std_dev', 'observations', 'indicator']
        
        df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'].astype(str) + '-01')
        df = df[['date', 'sunspot_number']].rename(columns={'sunspot_number': 'sunspot_area'})
        df = df.dropna(subset=['sunspot_area'])
        df = df[df['sunspot_area'] >= 0]
        
        print(f"成功获取太阳黑子数据：{df['date'].min().strftime('%Y-%m')} 至 {df['date'].max().strftime('%Y-%m')}")
        return df
    except Exception as e:
        print(f"数据获取失败，使用内置样本数据：{e}")
        dates = pd.date_range(start='1749-01-01', end='2024-12-01', freq='MS')
        cycle_years = 11
        t = np.linspace(0, 25*2*np.pi, len(dates))
        sunspot_area = 150 * np.sin(t) ** 2 + np.random.normal(0, 10, len(dates))
        sunspot_area = np.maximum(sunspot_area, 0)
        return pd.DataFrame({'date': dates, 'sunspot_area': sunspot_area})

def preprocess_data(df):
    """标注太阳活动周期（11年/周期，NOAA官方周期编号）"""
    cycles = [
        (1755, 1766, 1), (1766, 1775, 2), (1775, 1784, 3), (1784, 1798, 4),
        (1798, 1810, 5), (1810, 1823, 6), (1823, 1833, 7), (1833, 1843, 8),
        (1843, 1855, 9), (1855, 1867, 10), (1867, 1878, 11), (1878, 1890, 12),
        (1890, 1902, 13), (1902, 1913, 14), (1913, 1923, 15), (1923, 1933, 16),
        (1933, 1945, 17), (1945, 1954, 18), (1954, 1964, 19), (1964, 1976, 20),
        (1976, 1986, 21), (1986, 1996, 22), (1996, 2008, 23), (2008, 2020, 24),
        (2020, 2030, 25)
    ]
    
    df['cycle'] = np.nan
    for start_year, end_year, cycle_num in cycles:
        mask = (df['date'].dt.year >= start_year) & (df['date'].dt.year < end_year)
        df.loc[mask, 'cycle'] = cycle_num
    
    cycle_peaks = df.groupby('cycle')['sunspot_area'].agg(['max', 'idxmax']).reset_index()
    cycle_peaks['peak_date'] = df.loc[cycle_peaks['idxmax'], 'date'].values
    cycle_peaks = cycle_peaks[cycle_peaks['cycle'].notna()]
    
    return df, cycle_peaks