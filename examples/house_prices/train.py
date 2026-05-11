import joblib
import json
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split

def train():
    # Load dataset
    print("Loading data...")
    data = fetch_california_housing()
    X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)

    # Train model
    print("Training RandomForest model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    score = model.score(X_test, y_test)
    print(f"Model R2 Score: {score:.4f}")

    # Create directories if they don't exist
    os.makedirs("../../models", exist_ok=True)
    
    # Save model
    model_path = "../../models/house_prices_rf.pkl"
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
    
    # Generate a sample request
    sample = {
        "model_name": "house_prices",
        "inputs": X_test[:2].tolist()
    }
    with open("sample_request.json", "w") as f:
        json.dump(sample, f, indent=2)
    print("Sample request saved to sample_request.json")

if __name__ == "__main__":
    train()
