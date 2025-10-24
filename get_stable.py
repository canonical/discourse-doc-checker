#!/usr/bin/env python3
"""
Find the latest promote action and which commit it ran for.
"""

from datetime import datetime

import requests


def find_latest_promote_action(repo: str, owner: str = "canonical") -> str | None:
    """Find the latest promote action run.
    
    Args:
        repo: The GitHub repository name.
        owner: The GitHub repository owner (default is "canonical").

    Returns:
        The commit SHA the latest promote action ran for, or None if not found.

    Raises:
        requests.exceptions.RequestException: If there is an error fetching data from GitHub.
    """
    
    # GitHub API endpoint for workflow runs
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs"
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Promote-Action-Checker/1.0"
    }
    
    params = {
        "per_page": 100,  # Get more runs to find promote actions
        "status": "completed",  # Only completed runs
        "branch": "main",
        "event" : "workflow_dispatch"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        runs = data.get("workflow_runs", [])
        
        # Filter for promote-related workflows
        promote_runs = []
        for run in runs:
            workflow_name = run.get("name", "").lower()
            if "promote" in workflow_name:
                promote_runs.append(run)
        
        if not promote_runs:
            print("❌ No promote workflow runs found")
            return
        
        # Get the latest promote run
        latest_run = promote_runs[0]  # Already sorted by created_at desc
        
        print("🚀 Latest Promote Action Found:")
        print("="*50)
        print(f"Workflow Name: {latest_run['name']}")
        print(f"Status: {latest_run['status']}")
        print(f"Conclusion: {latest_run.get('conclusion', 'N/A')}")
        print(f"Branch: {latest_run['head_branch']}")
        print(f"Commit SHA: {latest_run['head_sha']}")
        print(f"Commit Message: {latest_run.get('display_title', 'N/A')}")
        
        created_at = datetime.fromisoformat(latest_run["created_at"].replace("Z", "+00:00"))
        print(f"Created: {created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"Run URL: {latest_run['html_url']}")
        
        return latest_run.get('head_sha')

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data: {e}")
        return None
