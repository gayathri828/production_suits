import numpy as np
import pandas as pd
from sklearn.linear_model import PassiveAggressiveClassifier

# Generate all 64 combinations of 6 binary attributes (1 or 0)
combinations = []
for i in range(64):
    # Generate a binary representation for each combination (6 attributes)
    binary_combination = list(map(int, bin(i)[2:].zfill(6)))  # Corrected to 6 binary attributes
    combinations.append(binary_combination)

# Define unique names for each suit combination (64 names)
suit_names = [
    "Defender", "Protector", "Guardian", "Sentinel", "Vanguard", "Shield", "Safeguard", "Fortress",
    "Aegis", "Warden", "Titan", "Bulwark", "Sentinel-X", "Barrier", "Ironclad", "Fortify",
    "Proteus", "Sentry", "Vigilant", "Watchman", "Resolute", "Armorite", "Stronghold", "Invictus",
    "Safeguard-X", "Guardian-X", "Defensive", "Watchguard", "Bastion", "SecureGuard", "Outpost", "Rampart",
    "Shieldmaster", "Lockdown", "Bastion-X", "SafeNet", "Protector-X", "Defense-X", "Fortress-X", "Guardian Elite",
    "Bulletproof", "Titanium", "Invulnerable", "StrongGuard", "DefenseMaster", "Iron Fortress", "Defender-X",
    "Safeguard Elite", "Protector-Guard", "Maximus", "UltraShield", "VigilGuard", "TitanGuard", "Perimeter",
    "Guardian Prime", "Sentinel-Xtreme", "FortifyElite", "AssaultGuard", "Vanguard-X", "Protector Titan",
    "SafeGuard Prime", "Defender Prime", "Sentinel Prime", "Security-X"
]


# Ensure that we have exactly 64 suit names
assert len(suit_names) == 64, "Suit names list must have exactly 64 names."

# Create a DataFrame for the combinations and suit names
data = pd.DataFrame(combinations, columns=[
    'fireproof', 'waterproof', 'gas_resistance',
    'chemical_resistance', 'germ_resistance',
    'bulletproof'
])
data['suit_name'] = suit_names  # Add the suit names column

# Define features (X) and labels (y)
X = data.drop('suit_name', axis=1)  # Remove 'suit_name' for the feature matrix
y = data['suit_name']  # 'suit_name' is the label

# Train the Passive Aggressive Classifier
model = PassiveAggressiveClassifier(max_iter=1000)
model.fit(X, y)

# Function to predict the suit based on user features
def predict_suit(features):
    """
    Predict the suit name based on user input features.
    Features must be in the form of a list: [fireproof, waterproof, gas_resistance, ...]
    """
    # Ensure features are in the right shape for prediction
    prediction = model.predict([features])
    return prediction[0]
