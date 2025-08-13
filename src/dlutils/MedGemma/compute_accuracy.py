import pandas as pd
import numpy as np

def analyze_errors(predictions, references, all_outputs=None, meta=None, max_mistakes=200, max_invalid_examples=3):
    """
    Analyze prediction errors and display detailed statistics.
    
    Args:
        predictions: List of predicted classes (-1 for invalid predictions)
        references: List of true/reference classes
        all_outputs: Optional list of raw model outputs for invalid prediction examples
        meta: Optional DataFrame containing metadata with 'Pathology' column for subgroup analysis
        max_mistakes: Maximum number of mistakes to analyze for patterns (default: 200)
        max_invalid_examples: Maximum number of invalid prediction examples to show (default: 3)
    
    Returns:
        dict: Dictionary containing analysis results with keys:
              - correct_predictions: list of correct prediction indices
              - incorrect_predictions: list of incorrect prediction indices  
              - invalid_predictions: list of invalid prediction indices
              - mistake_patterns: dict of mistake patterns and their counts
              - prediction_df: DataFrame with predictions and references
              - subgroup_acc: Series with subgroup accuracies (if meta provided)
    """
    correct_predictions = []
    incorrect_predictions = []
    invalid_predictions = []
    
    for i, (pred, ref) in enumerate(zip(predictions, references)):
        if pred == -1:
            invalid_predictions.append(i)
        elif pred == ref:
            correct_predictions.append(i)
        else:
            incorrect_predictions.append(i)
    
    print("🔍 Error Analysis:")
    print("=" * 30)
    print(f"Correct predictions: {len(correct_predictions)}")
    print(f"Incorrect predictions: {len(incorrect_predictions)}")
    print(f"Invalid predictions: {len(invalid_predictions)}")
    
    # Show confusion patterns
    mistake_count = {}
    if incorrect_predictions:
        print("\n❌ Common mistakes:")
        for idx in incorrect_predictions[:max_mistakes]:
            true_class = references[idx]
            pred_class = predictions[idx] if predictions[idx] != -1 else "Invalid"
            mistake = f"{true_class} → {pred_class}"
            mistake_count[mistake] = mistake_count.get(mistake, 0) + 1
        
        for mistake, count in sorted(mistake_count.items(), key=lambda x: x[1], reverse=True):
            print(f"  {mistake}: {count} times")
    
    # Show examples of invalid predictions
    if invalid_predictions:
        print("\n⚠️ Examples of invalid predictions:")
        for idx in invalid_predictions[:max_invalid_examples]:
            true_class = references[idx]
            raw_output = all_outputs[idx]["generated_text"] if all_outputs else "N/A"
            print(f"  True: {true_class}")
            print(f"  Raw output: '{raw_output}'")
    
    # Subgroup accuracy analysis
    prediction_df = pd.DataFrame({'predictions': predictions, 'references': references})
    subgroup_acc = prediction_df.groupby('references').predictions.value_counts(normalize=True)
    
    print("\n📊 Subgroup Accuracies:")
    print("=" * 30)
    if meta is not None:
        for i in meta.Pathology.unique():
            try:
                accuracy = subgroup_acc.loc[i, i]
                print(f'{i} Accuracy: {accuracy:.2f}')
            except KeyError:
                print(f'{i} Accuracy: 0.00 (no correct predictions)')
    else:
        # If meta is not provided, use unique values from references
        for i in pd.Series(references).unique():
            try:
                accuracy = subgroup_acc.loc[i, i]
                print(f'{i} Accuracy: {accuracy:.2f}')
            except KeyError:
                print(f'{i} Accuracy: 0.00 (no correct predictions)')
    
    return {
        'correct_predictions': correct_predictions,
        'incorrect_predictions': incorrect_predictions,
        'invalid_predictions': invalid_predictions,
        'mistake_patterns': mistake_count,
        'prediction_df': prediction_df,
        'subgroup_acc': subgroup_acc
    }

def compute_accuracy(predictions, references):
    """Compute accuracy and other metrics"""
    # Filter out invalid predictions
    valid_indices = [i for i, pred in enumerate(predictions) if pred != -1]

    if not valid_indices:
        return {
            'accuracy': 0.0,
            'valid_predictions': 0,
            'total_samples': len(predictions),
            'correct_predictions': 0
        }

    valid_predictions = [predictions[i] for i in valid_indices]
    valid_references = [references[i] for i in valid_indices]

    correct = sum(1 for p, r in zip(valid_predictions, valid_references) if p == r)
    accuracy = correct / len(valid_predictions)

    return {
        'accuracy': accuracy,
        'valid_predictions': len(valid_predictions),
        'total_samples': len(predictions),
        'correct_predictions': correct
    }