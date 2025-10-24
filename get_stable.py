#!/usr/bin/env python3
"""
Find the latest promote action and which commit it ran for.
"""

import sys

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
            print("❌ No promote workflow runs found", file=sys.stderr)
            return None
        
        # Get the latest promote run
        latest_run = promote_runs[0]  # Already sorted by created_at desc
        return latest_run.get('head_sha')

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching data: {e}", file=sys.stderr)
        return None
