import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Import your existing database connection functions
from your_database_module import create_connection, fetch_query_results

class RunningInjuryDataset(Dataset):
    def __init__(self, features, labels):
        """
        Custom PyTorch Dataset for running injury prediction
        
        Args:
            features (torch.Tensor): Input features
            labels (torch.Tensor): Binary injury labels
        """
        self.features = features
        self.labels = labels
    
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]

class InjuryPredictionModel(nn.Module):
    def __init__(self, input_size):
        """
        Neural Network for Injury Prediction
        
        Args:
            input_size (int): Number of input features
        """
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 1),
            nn.Sigmoid()
        )
    
    def forward(self, x):
        return self.network(x)

class InjuryPredictor:
    def __init__(self, database_connection):
        """
        Initialize injury prediction workflow
        
        Args:
            database_connection: MySQL database connection
        """
        self.connection = database_connection
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.scaler = StandardScaler()
    
    def prepare_data(self, test_size=0.2, random_state=42):
        """
        Prepare data for training and testing from the database
        
        Args:
            test_size (float): Proportion of data for testing
            random_state (int): Seed for reproducibility
        """
        # Fetch data from database using your existing fetch function
        query = """
        SELECT 
            a.user_id,
            f.activity_minutes,
            f.sleep_hours,
            a.cadence,
            a.pace,
            CASE WHEN a.pain_indicator = 'Y' THEN 1 ELSE 0 END as injury_label
        FROM fitness_watch f
        JOIN activities a ON f.log_id = a.log_id
        WHERE a.pain_indicator IS NOT NULL
        """
        data = fetch_query_results(self.connection, query)
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Select features and label
        features = ['activity_minutes', 'sleep_hours', 'cadence', 'pace']
        X = df[features]
        y = df['injury_label']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Convert to PyTorch tensors
        self.X_train = torch.FloatTensor(X_train_scaled)
        self.X_test = torch.FloatTensor(X_test_scaled)
        self.y_train = torch.FloatTensor(y_train.values).reshape(-1, 1)
        self.y_test = torch.FloatTensor(y_test.values).reshape(-1, 1)
        
        # Create datasets and dataloaders
        train_dataset = RunningInjuryDataset(self.X_train, self.y_train)
        test_dataset = RunningInjuryDataset(self.X_test, self.y_test)
        
        self.train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
        self.test_loader = DataLoader(test_dataset, batch_size=32)
    
    def train_model(self, epochs=100, learning_rate=0.001):
        """
        Train the injury prediction neural network
        
        Args:
            epochs (int): Number of training epochs
            learning_rate (float): Optimization learning rate
        """
        if not hasattr(self, 'X_train'):
            self.prepare_data()
        
        # Initialize model
        input_size = self.X_train.shape[1]
        self.model = InjuryPredictionModel(input_size).to(self.device)
        
        # Loss and optimizer
        criterion = nn.BCELoss()
        optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        
        # Training loop
        for epoch in range(epochs):
            self.model.train()
            total_loss = 0
            
            for batch_features, batch_labels in self.train_loader:
                batch_features = batch_features.to(self.device)
                batch_labels = batch_labels.to(self.device)
                
                optimizer.zero_grad()
                outputs = self.model(batch_features)
                loss = criterion(outputs, batch_labels)
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
            
            # Validation
            if epoch % 10 == 0:
                self.model.eval()
                val_loss = 0
                correct_predictions = 0
                total_predictions = 0
                
                with torch.no_grad():
                    for test_features, test_labels in self.test_loader:
                        test_features = test_features.to(self.device)
                        test_labels = test_labels.to(self.device)
                        
                        test_outputs = self.model(test_features)
                        val_loss += nn.BCELoss()(test_outputs, test_labels).item()
                        
                        predicted = (test_outputs > 0.5).float()
                        correct_predictions += (predicted == test_labels).sum().item()
                        total_predictions += test_labels.size(0)
                
                accuracy = correct_predictions / total_predictions
                print(f'Epoch {epoch}: Training Loss = {total_loss}, '
                      f'Validation Loss = {val_loss}, '
                      f'Accuracy = {accuracy*100:.2f}%')
        
        # Save model weights if needed
        torch.save(self.model.state_dict(), 'injury_prediction_model.pth')
    
    def predict_injury_risk(self, running_data):
        """
        Predict injury risk for new running data
        
        Args:
            running_data (dict): Dictionary of running metrics
        
        Returns:
            float: Probability of injury
        """
        if self.model is None:
            # Load saved model if not trained in current session
            try:
                input_size = len(running_data)
                self.model = InjuryPredictionModel(input_size)
                self.model.load_state_dict(torch.load('injury_prediction_model.pth'))
                self.model.eval()
            except Exception as e:
                raise ValueError("No trained model found. Call train_model() first.") from e
        
        # Prepare input data
        input_features = np.array([
            running_data['activity_minutes'],
            running_data['sleep_hours'],
            running_data['cadence'],
            running_data['pace']
        ]).reshape(1, -1)
        
        # Scale input
        scaled_input = self.scaler.transform(input_features)
        input_tensor = torch.FloatTensor(scaled_input)
        
        # Predict
        with torch.no_grad():
            injury_probability = self.model(input_tensor).item()
        
        return injury_probability

def integrate_injury_prediction(connection):
    """
    Main function to integrate injury prediction into coach app
    
    Args:
        connection: MySQL database connection
    """
    # Initialize predictor
    predictor = InjuryPredictor(connection)
    
    # Train model
    predictor.prepare_data()
    predictor.train_model()
    
    # Return predictor for further use
    return predictor

# Example usage in your main application flow
def main():
    # Establish database connection (from your existing code)
    connection = create_connection(username, password)
    
    # Integrate injury prediction
    injury_predictor = integrate_injury_prediction(connection)
    
    # Example prediction
    sample_run = {
        'activity_minutes': 45,
        'sleep_hours': 7.5,
        'cadence': 180,
        'pace': 5.5  # min/km
    }
    
    # Predict injury risk for a sample run
    injury_risk = injury_predictor.predict_injury_risk(sample_run)
    print(f"Injury Risk Probability: {injury_risk * 100:.2f}%")

if __name__ == "__main__":
    main()