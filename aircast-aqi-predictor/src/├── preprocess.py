import pandas as pd

def load_and_preprocess(path):
    df = pd.read_csv(path)
    df['datetime'] = pd.to_datetime(df['datetime'])

    # Time features
    df['hour'] = df['datetime'].dt.hour
    df['day'] = df['datetime'].dt.day

    df = df.drop(columns=['datetime'])

    return df
