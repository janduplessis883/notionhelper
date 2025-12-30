# NotionHelper ML Demo Guide

## Overview

`ml_demo.py` is a comprehensive demonstration of how to use **MLNotionHelper** (which extends NotionHelper) to track machine learning experiments. It showcases a complete workflow from model training to Notion integration.

**Note:** The ML experiment tracking features are available in the `MLNotionHelper` class, which inherits from `NotionHelper` and adds specialized methods for logging ML experiments.

## Features

✨ **Complete ML Pipeline**
- Logistic Regression on sklearn's breast cancer dataset
- Train/test split with stratification
- Feature scaling
- Comprehensive metrics calculation

📊 **Metrics Tracked**
- Accuracy
- Precision
- Recall
- F1 Score
- ROC AUC
- Training/Test sample sizes

📈 **Visualizations**
- Confusion Matrix (heatmap)
- ROC Curve with AUC score
- Feature Importance (when scaling is disabled)

💾 **Artifacts**
- Predictions CSV with probabilities
- Classification report
- All generated plots

## Quick Start

### 1. Run the Demo (without Notion)

```bash
python ml_demo.py
```

This will:
- Train the model
- Generate all metrics and plots
- Save artifacts to disk
- Show instructions for Notion integration

### 2. Set Up Notion Integration

#### A. Get Your Notion API Token

1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Create a new integration
3. Copy the "Internal Integration Token"
4. Set it as an environment variable:

```bash
export NOTION_TOKEN='secret_your_token_here'
```

#### B. Create a Parent Page

1. Create a new page in Notion (this will hold your ML experiment databases)
2. Share the page with your integration
3. Copy the page ID from the URL:
   - URL: `https://www.notion.so/My-ML-Experiments-abc123def456...`
   - Page ID: `abc123def456...`

#### C. Create the Database (First Time Only)

1. Open `ml_demo.py`
2. Find the "STEP 4A" section
3. Uncomment the database creation code
4. Set `PARENT_PAGE_ID = "your_page_id_here"`
5. Run the script:

```bash
python ml_demo.py
```

6. **IMPORTANT**: Copy the `data_source_id` from the output!

Example output:
```
✓ Database created! Data Source ID: 2d2fdfd6-8a97-80ba-bdd6-000b787993a4
💡 Save this ID for future experiment logging!
```

#### D. Log Experiments

1. Comment out the database creation code (STEP 4A)
2. Set `DATA_SOURCE_ID = "your_data_source_id_from_step_C"`
3. Run experiments:

```bash
python ml_demo.py
```

Each run will:
- Create a new row in your Notion database
- Upload confusion matrix and ROC curve plots
- Attach CSV artifacts
- Compare metrics with previous runs
- Show 🏆 if it's a new best score!

## Customization

### Hyperparameters

Modify the `config` dictionary in the `main()` function:

```python
config = {
    "Experiment_Name": "Your Experiment",
    "Model": "Logistic Regression",
    "C_Regularization": 10.0,        # Change this
    "Max_Iterations": 2000,          # Or this
    "Solver": "saga",                # Try different solvers
    "Penalty": "l1",                 # L1 or L2 regularization
    "Feature_Scaling": True          # Enable/disable scaling
}
```

### Target Metric

Change which metric to optimize in the `log_ml_experiment()` call:

```python
page_id = nh.log_ml_experiment(
    ...
    target_metric="Accuracy",     # Or "Precision", "Recall", "F1_Score"
    higher_is_better=True,        # Higher scores are better
    ...
)
```

## Example Workflow

### Experiment 1: Baseline
```python
config = {
    "C_Regularization": 1.0,
    "Penalty": "l2",
    "Solver": "lbfgs"
}
# Results: F1 Score = 98.61%
```

### Experiment 2: Stronger Regularization
```python
config = {
    "C_Regularization": 0.1,  # Stronger regularization
    "Penalty": "l2",
    "Solver": "lbfgs"
}
# Run to see if it improves performance
```

### Experiment 3: L1 Regularization
```python
config = {
    "C_Regularization": 1.0,
    "Penalty": "l1",          # Switch to L1
    "Solver": "saga"          # L1 requires saga or liblinear
}
# L1 can perform feature selection
```

## Generated Files

After running the demo, you'll find:

```
├── confusion_matrix.png           # Confusion matrix heatmap
├── roc_curve.png                  # ROC curve with AUC
├── feature_importance.png         # Feature coefficients (if no scaling)
├── predictions.csv                # Test set predictions
└── classification_report.csv      # Detailed metrics per class
```

## Notion Database Schema

The created database will have columns for:

**Config Fields:**
- Experiment_Name (Title)
- Model
- Dataset
- Test_Size
- Random_State
- C_Regularization (Number)
- Max_Iterations (Number)
- Solver
- Penalty
- Feature_Scaling (Checkbox) ✅

**Metric Fields:**
- Accuracy (Number)
- Precision (Number)
- Recall (Number)
- F1_Score (Number)
- ROC_AUC (Number)
- Train_Samples (Number)
- Test_Samples (Number)
- Run Status (shows 🏆 for new best)

**Artifacts:**
- Plots (embedded in page body)
- Artifacts (attached CSV files)

## Troubleshooting

### Boolean Properties Showing as Numbers

If you see boolean values (like `Feature_Scaling`) appearing as numbers in Notion:

1. Check the debug output in the console
2. Ensure you're passing Python `bool` types (not 0/1 integers)
3. The `dict_to_notion_schema()` includes debug prints to help diagnose

### Notion API Errors

Common issues:
- **401 Unauthorized**: Check your NOTION_TOKEN
- **404 Not Found**: Verify your PARENT_PAGE_ID or DATA_SOURCE_ID
- **400 Bad Request**: Make sure the page is shared with your integration

### Missing Plots

Ensure matplotlib and seaborn are installed:
```bash
pip install matplotlib seaborn
```

## Advanced Usage

### Use Your Own Dataset

Replace the data loading section:

```python
# Replace this:
data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target, name='target')

# With your own data:
df = pd.read_csv('your_data.csv')
X = df.drop('target_column', axis=1)
y = df['target_column']
```

### Add More Metrics

Calculate additional metrics:

```python
from sklearn.metrics import matthews_corrcoef, balanced_accuracy_score

metrics = {
    ...
    "MCC": round(matthews_corrcoef(y_test, y_pred), 4),
    "Balanced_Accuracy": round(balanced_accuracy_score(y_test, y_pred) * 100, 2)
}
```

### Grid Search Integration

Combine with sklearn's GridSearchCV:

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'C': [0.1, 1.0, 10.0],
    'penalty': ['l1', 'l2']
}

grid = GridSearchCV(LogisticRegression(), param_grid, cv=5)
grid.fit(X_train, y_train)

# Log each configuration
for params, mean_score in zip(grid.cv_results_['params'],
                               grid.cv_results_['mean_test_score']):
    config.update(params)
    metrics['CV_Score'] = mean_score
    nh.log_ml_experiment(...)
```

## Benefits of Using NotionHelper

✅ **Centralized Tracking**: All experiments in one place
✅ **Visual Comparison**: See which hyperparameters work best
✅ **Automatic Leaderboard**: Highlights new best scores
✅ **File Attachments**: Keep plots and CSVs with experiments
✅ **Team Collaboration**: Share results with your team
✅ **Reproducibility**: Track all hyperparameters and seeds

## Next Steps

1. **Run the demo** to familiarize yourself with the workflow
2. **Create your Notion database** following the setup guide
3. **Customize for your project** - replace with your ML model
4. **Run multiple experiments** with different hyperparameters
5. **Review results in Notion** - compare and analyze performance

## Support

For issues or questions:
- Check the [NotionHelper documentation](carecast/notionhelper.py)
- Review the [Notion API docs](https://developers.notion.com/)
- Examine the debug output for type checking issues

---

**Happy Experimenting! 🚀**
