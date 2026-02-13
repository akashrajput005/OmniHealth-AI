import pandas as pd
import os

DATASET_DIR = 'dataset'

def get_stats():
    stats = {}
    
    # Diabetes
    try:
        df = pd.read_csv(os.path.join(DATASET_DIR, 'diabetes.csv'))
        stats['diabetes'] = {
            'mean': df.mean(numeric_only=True).to_dict(),
            'healthy': df[df['Outcome'] == 0].mean(numeric_only=True).to_dict(),
            'positive': df[df['Outcome'] == 1].mean(numeric_only=True).to_dict()
        }
    except Exception as e: print(f"Diabetes stats error: {e}")

    # Heart Disease
    try:
        df = pd.read_csv(os.path.join(DATASET_DIR, 'heart.csv'))
        stats['heart'] = {
            'mean': df.mean(numeric_only=True).to_dict(),
            'healthy': df[df['target'] == 0].mean(numeric_only=True).to_dict(),
            'positive': df[df['target'] == 1].mean(numeric_only=True).to_dict()
        }
    except Exception as e: print(f"Heart stats error: {e}")

    # Parkinson's
    try:
        df = pd.read_csv(os.path.join(DATASET_DIR, 'parkinsons.csv'))
        # Name column is not numeric
        numeric_df = df.drop(columns=['name'], errors='ignore')
        stats['parkinsons'] = {
            'mean': numeric_df.mean(numeric_only=True).to_dict(),
            'healthy': numeric_df[numeric_df['status'] == 0].mean(numeric_only=True).to_dict(),
            'positive': numeric_df[numeric_df['status'] == 1].mean(numeric_only=True).to_dict()
        }
    except Exception as e: print(f"Parkinsons stats error: {e}")

    return stats

if __name__ == "__main__":
    import json
    with open('src/dataset_stats.json', 'w') as f:
        json.dump(get_stats(), f, indent=4)
    print("Stats generated successfully.")
