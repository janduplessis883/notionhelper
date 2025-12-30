"""
NotionHelper ML Demo: Logistic Regression with sklearn
=======================================================
This demo showcases how to use NotionHelper to track ML experiments.

Features:
- Logistic regression on sklearn's breast cancer dataset
- Complete metrics tracking (accuracy, precision, recall, F1)
- Hyperparameter configuration
- Automatic Notion database creation
- Experiment logging with plots and artifacts
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_curve,
    roc_auc_score
)
from sklearn.preprocessing import StandardScaler

from notionhelper import MLNotionHelper


def train_logistic_regression(
    test_size=0.2,
    random_state=42,
    C=1.0,
    max_iter=1000,
    solver='lbfgs',
    penalty='l2',
    scale_features=True
):
    """
    Train a logistic regression model on breast cancer dataset.

    Parameters:
    -----------
    test_size : float
        Proportion of dataset to use for testing
    random_state : int
        Random seed for reproducibility
    C : float
        Inverse of regularization strength
    max_iter : int
        Maximum iterations for solver
    solver : str
        Algorithm to use in optimization
    penalty : str
        Regularization penalty type
    scale_features : bool
        Whether to standardize features

    Returns:
    --------
    metrics : dict
        Dictionary containing all evaluation metrics
    plot_paths : list
        List of paths to generated plots
    artifacts : list
        List of paths to saved artifacts
    """

    print("\n" + "="*60)
    print("🔬 NOTIONHELPER ML DEMO: Logistic Regression")
    print("="*60 + "\n")

    # 1. Load Dataset
    print("📊 Loading breast cancer dataset...")
    data = load_breast_cancer()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = pd.Series(data.target, name='target')

    print(f"   Dataset shape: {X.shape}")
    print(f"   Classes: {data.target_names}")
    print(f"   Features: {X.shape[1]}")

    # 2. Split Data
    print("\n🔀 Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    print(f"   Training set: {X_train.shape[0]} samples")
    print(f"   Test set: {X_test.shape[0]} samples")

    # 3. Feature Scaling (optional but recommended)
    if scale_features:
        print("\n⚖️  Scaling features...")
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

    # 4. Train Model
    print("\n🤖 Training Logistic Regression model...")
    model = LogisticRegression(
        C=C,
        max_iter=max_iter,
        solver=solver,
        penalty=penalty,
        random_state=random_state
    )
    model.fit(X_train, y_train)
    print("   ✓ Model trained successfully")

    # 5. Make Predictions
    print("\n🎯 Making predictions...")
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    # 6. Calculate Metrics
    print("\n📈 Calculating metrics...")
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)

    metrics = {
        "Accuracy": round(accuracy * 100, 2),
        "Precision": round(precision * 100, 2),
        "Recall": round(recall * 100, 2),
        "F1_Score": round(f1 * 100, 2),
        "ROC_AUC": round(roc_auc * 100, 2),
        "Train_Samples": int(X_train.shape[0]),
        "Test_Samples": int(X_test.shape[0])
    }

    # Print metrics
    print("\n" + "="*60)
    print("📊 MODEL PERFORMANCE METRICS")
    print("-" * 60)
    print(f"Accuracy  : {metrics['Accuracy']:.2f}%")
    print(f"Precision : {metrics['Precision']:.2f}%")
    print(f"Recall    : {metrics['Recall']:.2f}%")
    print(f"F1 Score  : {metrics['F1_Score']:.2f}%")
    print(f"ROC AUC   : {metrics['ROC_AUC']:.2f}%")
    print("="*60 + "\n")

    # 7. Generate Visualizations
    print("📊 Generating visualizations...")
    plot_paths = []

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=data.target_names,
                yticklabels=data.target_names)
    plt.title('Confusion Matrix', fontsize=14, fontweight='bold')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    cm_path = 'confusion_matrix.png'
    plt.savefig(cm_path, dpi=150)
    plot_paths.append(cm_path)
    plt.close()
    print(f"   ✓ Saved: {cm_path}")

    # ROC Curve
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='#1f77b4', lw=2,
             label=f'ROC curve (AUC = {roc_auc:.3f})')
    plt.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--',
             label='Random Classifier')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('ROC Curve', fontsize=14, fontweight='bold')
    plt.legend(loc="lower right")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    roc_path = 'roc_curve.png'
    plt.savefig(roc_path, dpi=150)
    plot_paths.append(roc_path)
    plt.close()
    print(f"   ✓ Saved: {roc_path}")

    # Feature Importance (Coefficients)
    if not scale_features:
        feature_importance = pd.DataFrame({
            'Feature': data.feature_names,
            'Coefficient': model.coef_[0]
        }).sort_values('Coefficient', key=abs, ascending=False).head(15)

        plt.figure(figsize=(10, 6))
        colors = ['#d62728' if x < 0 else '#2ca02c' for x in feature_importance['Coefficient']]
        plt.barh(feature_importance['Feature'], feature_importance['Coefficient'], color=colors)
        plt.xlabel('Coefficient Value', fontsize=12)
        plt.title('Top 15 Feature Importance (Logistic Regression Coefficients)',
                  fontsize=14, fontweight='bold')
        plt.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        feat_path = 'feature_importance.png'
        plt.savefig(feat_path, dpi=150)
        plot_paths.append(feat_path)
        plt.close()
        print(f"   ✓ Saved: {feat_path}")

    # 8. Save Artifacts
    print("\n💾 Saving artifacts...")
    artifacts = []

    # Save predictions
    predictions_df = pd.DataFrame({
        'True_Label': y_test.values,
        'Predicted_Label': y_pred,
        'Probability_Malignant': y_pred_proba,
        'Correct': (y_test.values == y_pred).astype(int)
    })
    pred_path = 'predictions.csv'
    predictions_df.to_csv(pred_path, index=False)
    artifacts.append(pred_path)
    print(f"   ✓ Saved: {pred_path}")

    # Save classification report
    report = classification_report(y_test, y_pred,
                                   target_names=data.target_names,
                                   output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    report_path = 'classification_report.csv'
    report_df.to_csv(report_path)
    artifacts.append(report_path)
    print(f"   ✓ Saved: {report_path}")

    # Combine plot paths and artifacts
    all_artifacts = plot_paths + artifacts

    return metrics, plot_paths, all_artifacts


def main():
    """
    Main function to demonstrate NotionHelper integration.
    """

    # ============================================================
    # STEP 1: Define Hyperparameters Configuration
    # ============================================================
    config = {
        "Experiment_Name": "Logistic Regression Demo",
        "Model": "Logistic Regression",
        "Dataset": "Breast Cancer (sklearn)",
        "Test_Size": 0.2,
        "Random_State": 42,
        "C_Regularization": 1.0,
        "Max_Iterations": 2,
        "Solver": "lbfgs",
        "Penalty": "l2",
        "Feature_Scaling": True
    }

    # ============================================================
    # STEP 2: Train Model and Calculate Metrics
    # ============================================================
    metrics, plot_paths, artifacts = train_logistic_regression(
        test_size=config["Test_Size"],
        random_state=config["Random_State"],
        C=config["C_Regularization"],
        max_iter=config["Max_Iterations"],
        solver=config["Solver"],
        penalty=config["Penalty"],
        scale_features=config["Feature_Scaling"]
    )

    # ============================================================
    # STEP 3: Initialize NotionHelper
    # ============================================================
    print("\n" + "="*60)
    print("📝 NOTION INTEGRATION")
    print("="*60 + "\n")

    # IMPORTANT: Replace with your Notion API token
    NOTION_TOKEN = os.getenv("NOTION_TOKEN", "your_notion_token_here")

    if NOTION_TOKEN == "your_notion_token_here":
        print("⚠️  WARNING: Please set your NOTION_TOKEN environment variable")
        print("   Example: export NOTION_TOKEN='secret_...'")
        print("\n✅ Demo completed successfully (without Notion logging)")
        print(f"\n📁 Generated files:")
        for artifact in artifacts:
            print(f"   • {artifact}")
        return

    try:
        nh = MLNotionHelper(NOTION_TOKEN)
        print("✓ MLNotionHelper initialized successfully")

        # ============================================================
        # STEP 4A: Create New Database (First time only)
        # ============================================================
        # Set CREATE_NEW_DB to True on first run, then set to False
        CREATE_NEW_DB = False  # Force creation for this run
        PARENT_PAGE_ID = "your page id here"

        if CREATE_NEW_DB:
            print("\n🗄️  Creating new Notion database...")
            data_source_id = nh.create_ml_database(
                parent_page_id=PARENT_PAGE_ID,
                db_title="ML Experiments - Logistic Regression Demo",
                config=config,
                metrics=metrics,
                file_property_name="Artifacts"
            )
            print(f"\n✅ Database created successfully!")
            print(f"📝 Data Source ID: {data_source_id}")
            print("\n" + "="*60)
            print("⚠️  CRITICAL: Complete these steps NOW!")
            print("="*60)
            print("\n1️⃣  Go to Notion and find the new database:")
            print("   'ML Experiments - Logistic Regression Demo'")
            print("\n2️⃣  Click '...' (top right) → Add connections")
            print("   → Select your integration")
            print("\n3️⃣  Save this Data Source ID:")
            print(f"   DATA_SOURCE_ID = \"{data_source_id}\"")
            print("\n4️⃣  Set CREATE_NEW_DB = False in this script")
            print("\n5️⃣  Run the script again to log experiments")
            print("="*60 + "\n")

            print("⏸️  Skipping experiment logging for this run.")
            print("   Complete steps above, then run again.")
            return  # Exit after database creation

        # This else block will only be reached if CREATE_NEW_DB was initially False
        # and the user has already provided a DATA_SOURCE_ID.
        else:
            # Replace with your actual data source ID after creating the database
            DATA_SOURCE_ID = "your_data_source_id_here" # This should be updated by the user


        if DATA_SOURCE_ID == "your_data_source_id_here":
            print("\n💡 To log experiments:")
            print("   1. Ensure CREATE_NEW_DB is False and DATA_SOURCE_ID is set.")
            print("   2. Make sure the database is shared with your integration.")
        else:
            print("\n� Logging experiment to Notion...")
            page_id = nh.log_ml_experiment(
                data_source_id=DATA_SOURCE_ID,
                config=config,
                metrics=metrics,
                plots=plot_paths,
                target_metric="F1_Score",
                higher_is_better=True,
                file_paths=artifacts,
                file_property_name="Artifacts"
            )

            if page_id:
                print(f"✓ Experiment logged successfully!")
                print(f"  Page ID: {page_id}")
            else:
                print("❌ Failed to log experiment")

    except Exception as e:
        print(f"❌ Notion API Error: {e}")
        print("   Continuing without Notion logging...")

    # ============================================================
    # FINAL SUMMARY
    # ============================================================
    print("\n" + "="*60)
    print("✅ DEMO COMPLETED SUCCESSFULLY")
    print("="*60)
    print(f"\n📁 Generated files:")
    for artifact in artifacts:
        print(f"   • {artifact}")

    print("\n📊 Key Metrics:")
    print(f"   • Accuracy:  {metrics['Accuracy']:.2f}%")
    print(f"   • F1 Score:  {metrics['F1_Score']:.2f}%")
    print(f"   • ROC AUC:   {metrics['ROC_AUC']:.2f}%")

    print("\n🎉 Thank you for trying NotionHelper!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
