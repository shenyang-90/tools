#!/usr/bin/env python3
"""
Scripts/flow/task_workflow.py - 任务状态自动流转引擎模板

Usage:
    python3 task_workflow.py --task TASK_ID --event on_submit
"""

import json
import argparse
from pathlib import Path
from datetime import datetime


class TaskWorkflow:
    """任务状态自动流转引擎"""

    RULES = {
        # 规则: 当前状态 → 触发条件 → 下一状态
        "pending": {
            "on_assign": "assigned",
            "auto_assign": "assigned"  # 根据负载均衡自动分配
        },
        "assigned": {
            "on_start": "running",
            "on_timeout": "pending"  # 超时未开始，重新分配
        },
        "running": {
            "on_submit": "reviewing",
            "on_block": "blocked",
            "progress_check": "running"  # 进度检查点
        },
        "reviewing": {
            "on_pass": "completed",
            "on_fail": "rejected",
            "auto_review": "completed"  # 自动检查通过
        },
        "rejected": {
            "on_rework": "running",
            "on_reassign": "assigned"
        },
        "completed": {
            "trigger_next": True  # 触发下游任务
        }
    }

    def __init__(self, project_path):
        self.project_path = Path(project_path)

    def transition(self, task, event):
        """执行状态流转"""
        current = task.get("status", "pending")
        if event in self.RULES.get(current, {}):
            new_status = self.RULES[current][event]
            self._update_status(task, new_status)
            self._notify_agents(task, current, new_status)
            self._execute_hooks(task, new_status)
            return new_status
        return None

    def _update_status(self, task, new_status):
        task["status"] = new_status
        task["status_history"] = task.get("status_history", []) + [
            {"status": new_status, "timestamp": datetime.now().isoformat()}
        ]

    def _notify_agents(self, task, old_status, new_status):
        """通知相关Agent状态变更"""
        print(f"[Workflow] Task {task.get('task_id')} {old_status} -> {new_status}")

    def _execute_hooks(self, task, new_status):
        """执行状态钩子"""
        if new_status == "reviewing":
            self.trigger_quality_check(task)
        elif new_status == "completed":
            self.trigger_downstream_tasks(task)
            self.update_dashboard(task)

    def trigger_quality_check(self, task):
        """触发质量检查"""
        print(f"[Hook] Triggering quality check for {task.get('task_id')}")

    def trigger_downstream_tasks(self, task):
        """触发下游任务"""
        for dep in task.get("dependencies", {}).get("post_tasks", []):
            print(f"[Hook] Triggering downstream task: {dep}")

    def update_dashboard(self, task):
        """更新Dashboard"""
        print(f"[Hook] Updating dashboard for {task.get('task_id')}")


def main():
    parser = argparse.ArgumentParser(description="Task Workflow Engine")
    parser.add_argument("--task", required=True, help="Task ID")
    parser.add_argument("--event", required=True, help="Event name")
    parser.add_argument("--project", default=".", help="Project path")
    args = parser.parse_args()

    engine = TaskWorkflow(args.project)
    # 加载任务...（实际实现需接入任务存储）
    task = {"task_id": args.task, "status": "running"}
    result = engine.transition(task, args.event)
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
