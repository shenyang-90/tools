#!/usr/bin/env python3
"""
Scripts/flow/update_dashboard.py - Dashboard生成脚本模板

Usage:
    python3 update_dashboard.py --project /path/to/project
"""

import json
import os
from datetime import datetime
from pathlib import Path


class DashboardGenerator:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.dashboard_path = self.project_path / "ProjectMgmt" / "Dashboard.md"

    def generate(self):
        """生成Dashboard"""
        content = []
        content.append(self._header())
        content.append(self._phase_status())
        content.append(self._active_tasks())
        content.append(self._agent_status())
        content.append(self._quality_metrics())
        content.append(self._alerts())
        content.append(self._milestones())
        content.append(self._footer())

        self.dashboard_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.dashboard_path, 'w') as f:
            f.write('\n'.join(content))
        print(f"[Dashboard] Generated: {self.dashboard_path}")

    def _header(self):
        project_name = self._load_project_name()
        return f"# {project_name} - Project Dashboard\n\n*Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"

    def _phase_status(self):
        phases = self._load_phase_data()
        lines = ["\n## Phase Status\n\n| Phase | Status | Progress | Gate Date |",
                 "|-------|--------|----------|-----------|"]
        for phase, data in phases.items():
            lines.append(f"| {phase} | {data['status']} | {data['progress']}% | {data.get('date', '-')} |")
        return '\n'.join(lines)

    def _active_tasks(self):
        tasks = self._load_task_data()
        lines = ["\n## Active Tasks\n\n| Task ID | Type | Assignee | Status | Deadline | Progress |",
                 "|---------|------|----------|--------|----------|----------|"]
        for t in tasks:
            lines.append(f"| {t['id']} | {t['type']} | {t['assignee']} | {t['status']} | {t.get('deadline', '-')} | {t.get('progress', '-')} |")
        return '\n'.join(lines)

    def _agent_status(self):
        return "\n## Agent Status\n\n| Agent | Active Tasks | Load |\n|-------|-------------|------|"

    def _quality_metrics(self):
        return "\n## Quality Metrics\n\n*Metrics placeholder*"

    def _alerts(self):
        return "\n## Alerts\n\n| Time | Severity | Message |\n|------|----------|---------|"

    def _milestones(self):
        return "\n## Upcoming Milestones\n\n| Date | Milestone | Owner |\n|------|-----------|-------|"

    def _footer(self):
        return "\n---\n*Dashboard auto-generated*"

    def _load_project_name(self):
        readme = self.project_path / "README.md"
        if readme.exists():
            return readme.read_text().split('\n')[0].lstrip('# ')
        return "Project"

    def _load_phase_data(self):
        return {"PCD": {"status": "COMPLETE", "progress": 100, "date": "-"},
                "PAD": {"status": "COMPLETE", "progress": 100, "date": "-"},
                "EDR": {"status": "COMPLETE", "progress": 100, "date": "-"},
                "IDR": {"status": "IN PROGRESS", "progress": 0, "date": "-"},
                "FDR": {"status": "NOT STARTED", "progress": 0, "date": "-"},
                "PostSilicon": {"status": "NOT STARTED", "progress": 0, "date": "-"}}

    def _load_task_data(self):
        return []


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=".", help="Project path")
    args = parser.parse_args()

    gen = DashboardGenerator(args.project)
    gen.generate()


if __name__ == "__main__":
    main()
