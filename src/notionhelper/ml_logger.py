from typing import Optional, Dict, List, Any
import pandas as pd
import numpy as np
import os
from datetime import datetime

from .helper import NotionHelper


class MLNotionHelper(NotionHelper):
    """
    ML experiment tracking helper that extends NotionHelper.

    Provides specialized methods for logging and tracking machine learning experiments,
    automatically comparing metrics against historical runs and logging results to Notion.

    Methods
    -------
    log_ml_experiment(data_source_id, config, metrics, plots, target_metric,
                     higher_is_better, file_paths, file_property_name):
        Logs an ML experiment run with metrics, plots, and artifacts.

    create_ml_database(parent_page_id, db_title, config, metrics, file_property_name):
        Creates a new Notion database optimized for ML experiment tracking.

    dict_to_notion_schema(data, title_key):
        Converts a dictionary into a Notion property schema.

    dict_to_notion_props(data, title_key):
        Converts a dictionary into Notion property values.
    """

    def dict_to_notion_schema(self, data: Dict[str, Any], title_key: str) -> Dict[str, Any]:
        """Converts a dictionary into a Notion property schema for database creation.

        Parameters:
            data (dict): Dictionary containing sample values to infer types from.
            title_key (str): The key that should be used as the title property.

        Returns:
            dict: A dictionary defining the Notion property schema.
        """
        properties = {}

        for key, value in data.items():
            # Handle NumPy types
            if hasattr(value, "item"):
                value = value.item()

            # Debug output to help diagnose type issues
            print(f"DEBUG: key='{key}', value={value}, type={type(value).__name__}, isinstance(bool)={isinstance(value, bool)}, isinstance(int)={isinstance(value, int)}")

            if key == title_key:
                properties[key] = {"title": {}}
            # IMPORTANT: Check for bool BEFORE (int, float) because bool is a subclass of int in Python
            elif isinstance(value, bool):
                properties[key] = {"checkbox": {}}
                print(f"  → Assigned as CHECKBOX")
            elif isinstance(value, (int, float)):
                properties[key] = {"number": {"format": "number"}}
                print(f"  → Assigned as NUMBER")
            else:
                properties[key] = {"rich_text": {}}
                print(f"  → Assigned as RICH_TEXT")

        return properties

    def dict_to_notion_props(self, data: Dict[str, Any], title_key: str) -> Dict[str, Any]:
        """Converts a dictionary into Notion property values for page creation.

        Parameters:
            data (dict): Dictionary containing the values to convert.
            title_key (str): The key that should be used as the title property.

        Returns:
            dict: A dictionary defining the Notion property values.
        """
        notion_props = {}
        for key, value in data.items():
            # Handle NumPy types
            if hasattr(value, "item"):
                value = value.item()

            if key == title_key:
                ts = datetime.now().strftime("%Y-%m-%d %H:%M")
                notion_props[key] = {"title": [{"text": {"content": f"{value} ({ts})"}}]}

            # FIX: Handle Booleans
            elif isinstance(value, bool):
                # Option A: Map to a Checkbox column in Notion
                # notion_props[key] = {"checkbox": value}

                # Option B: Map to a Rich Text column as a string (since you added a rich text field)
                notion_props[key] = {"rich_text": [{"text": {"content": str(value)}}]}

            elif isinstance(value, (int, float)):
                if pd.isna(value) or np.isinf(value):
                    continue
                notion_props[key] = {"number": float(value)}
            else:
                notion_props[key] = {"rich_text": [{"text": {"content": str(value)}}]}
        return notion_props

    def log_ml_experiment(
        self,
        data_source_id: str,
        config: Dict,
        metrics: Dict,
        plots: List[str] = None,
        target_metric: str = "sMAPE",
        higher_is_better: bool = False,
        file_paths: Optional[List[str]] = None,
        file_property_name: str = "Output Files"
    ):
        """Logs ML experiment and compares metrics with multiple file support."""
        improvement_tag = "Standard Run"
        new_score = metrics.get(target_metric)

        # 1. Leaderboard Logic (Champions)
        if new_score is not None:
            try:
                df = self.get_data_source_pages_as_dataframe(data_source_id, limit=100)
                if not df.empty and target_metric in df.columns:
                    valid_scores = pd.to_numeric(df[target_metric], errors='coerce').dropna()
                    if not valid_scores.empty:
                        current_best = valid_scores.max() if higher_is_better else valid_scores.min()
                        is_improvement = (new_score > current_best) if higher_is_better else (new_score < current_best)
                        if is_improvement:
                            improvement_tag = f"🏆 NEW BEST {target_metric} (Prev: {current_best:.2f})"
                        else:
                            diff = abs(new_score - current_best)
                            improvement_tag = f"No Improvement (+{diff:.2f} {target_metric})"
            except Exception as e:
                print(f"Leaderboard check skipped: {e}")

        # 2. Prepare Notion Properties
        data_for_notion = metrics.copy()
        data_for_notion["Run Status"] = improvement_tag
        combined_payload = {**config, **data_for_notion}
        title_key = list(config.keys())[0]
        properties = self.dict_to_notion_props(combined_payload, title_key)

        try:
            # 3. Create the row
            new_page = self.new_page_to_data_source(data_source_id, properties)
            page_id = new_page["id"]

            # 4. Handle Plots (Body)
            if plots:
                for plot_path in plots:
                    if os.path.exists(plot_path):
                        self.one_step_image_embed(page_id, plot_path)

            # 5. Handle Multiple File Uploads (Property)
            if file_paths:
                file_assets = []
                for path in file_paths:
                    if os.path.exists(path):
                        print(f"Uploading {path}...")
                        upload_resp = self.upload_file(path)
                        file_assets.append({
                            "type": "file_upload",
                            "file_upload": {"id": upload_resp["id"]},
                            "name": os.path.basename(path),
                        })

                if file_assets:
                    # Attach all files in one request
                    update_url = f"https://api.notion.com/v1/pages/{page_id}"
                    file_payload = {"properties": {file_property_name: {"files": file_assets}}}
                    self._make_request("PATCH", update_url, file_payload)
                    print(f"✅ {len(file_assets)} files attached to {file_property_name}")

            return page_id
        except Exception as e:
            print(f"Log error: {e}")
            return None

    def create_ml_database(self, parent_page_id: str, db_title: str, config: Dict, metrics: Dict, file_property_name: str = "Output Files") -> str:
        """
        Analyzes dicts to create a new Notion Database with the correct schema.
        Uses dict_to_notion_schema() for universal type conversion.
        """
        combined = {**config, **metrics}
        title_key = list(config.keys())[0]

        # Use the universal dict_to_notion_schema() method
        properties = self.dict_to_notion_schema(combined, title_key)

        # Add 'Run Status' if not already present
        if "Run Status" not in properties:
            properties["Run Status"] = {"rich_text": {}}

        # Add the Multi-file property
        properties[file_property_name] = {"files": {}}

        print(f"Creating database '{db_title}' with {len(properties)} columns...")

        response = self.create_database(
            parent_page_id=parent_page_id,
            database_title=db_title,
            initial_data_source_properties=properties
        )

        data_source_id = response.get("initial_data_source", {}).get("id")
        return data_source_id if data_source_id else response.get("id")
