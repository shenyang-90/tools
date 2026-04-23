#!/usr/bin/env python3
"""
Scripts/review_bot/review_bot.py - Review Bot 自动化检查引擎模板

Usage:
    python3 review_bot.py --stage IDR --project /path/to/project --task TASK_ID
    python3 review_bot.py --all --project /path/to/project
    python3 review_bot.py --stage IDR --checks "LintCheck,CoverageCheck"
"""

import json
import os
import re
import subprocess
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional


@dataclass
class CheckResult:
    check_name: str
    passed: bool
    message: str
    details: Optional[Dict] = None

    def to_dict(self):
        return {"check": self.check_name, "passed": self.passed, "message": self.message, "details": self.details}


class ReviewBot:
    """自动化Review检查引擎"""

    CRITICAL_CHECKS = ["FileExists", "CoverageCheck", "LintErrorCheck", "TimingCheck", "PVCheck"]

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.report_path = self.project_path / "ProjectMgmt" / "Reviews"

    def on_task_reviewing(self, task: Dict) -> Dict:
        """任务进入REVIEWING状态时自动触发"""
        stage = self._detect_stage_from_task(task)
        return self.execute_review(stage, task)

    def execute_review(self, stage: str, task: Dict) -> Dict:
        """执行阶段检查"""
        checks = self._get_checks_for_stage(stage)
        results = [check.run(self.project_path, task) for check in checks]

        report = self._generate_report(stage, task, results)
        self._save_report(stage, report)
        return report

    def _get_checks_for_stage(self, stage: str) -> List:
        """每个阶段对应的检查项"""
        CHECKS = {
            "PCD": [FileExistsCheck("ProjectMgmt/Planning/MRD.md"), MarkdownLintCheck()],
            "PAD": [FileExistsCheck("docs/Arch/Architecture_Spec.md"), TraceabilityCheck()],
            "EDR": [FileExistsCheck("docs/Design/Design_Spec.md"),
                    SectionCheck("docs/Design/Design_Spec.md",
                                 required=["Overview", "Functions", "Registers", "Block Design", "Interface", "History"]),
                    FileExistsCheck("design/ip/Module_Name/synthesis.sdc"),
                    FileExistsCheck("design/ip/Module_Name/power_intent.upf")],
            "IDR": [RTLExistenceCheck("design/RTL/"), CoverageCheck(min_line=90, min_toggle=85, min_fsm=95),
                    LintCheck(errors_max=0, warnings_max=10), BugCheck(no_critical_major=True)],
            "FDR": [FileExistsCheck("design/GDS/top.gds"), TimingCheck(setup_slack_min=0, hold_slack_min=0),
                    PVCheck(drc_clean=True, lvs_clean=True)]
        }
        return CHECKS.get(stage, [])

    def _generate_report(self, stage: str, task: Dict, results: List[CheckResult]) -> Dict:
        passed = [r for r in results if r.passed]
        failed = [r for r in results if not r.passed]
        critical_failed = [r for r in failed if any(c in r.check_name for c in self.CRITICAL_CHECKS)]

        all_passed = len(failed) == 0
        critical_passed = len(critical_failed) == 0

        if all_passed:
            recommendation = "PASS"
        elif critical_passed:
            recommendation = "CONDITIONAL"
        else:
            recommendation = "FAIL"

        return {
            "stage": stage, "task_id": task.get("id"), "timestamp": datetime.now().isoformat(),
            "summary": {"total": len(results), "passed": len(passed), "failed": len(failed), "critical_failed": len(critical_failed)},
            "all_passed": all_passed, "critical_passed": critical_passed,
            "recommendation": recommendation, "results": [r.to_dict() for r in results]
        }

    def _save_report(self, stage: str, report: Dict):
        stage_dir = self.report_path / stage
        stage_dir.mkdir(parents=True, exist_ok=True)

        md = self._generate_markdown_report(stage, report)
        (stage_dir / f"REVIEW_{stage}_Report.md").write_text(md)

        with open(stage_dir / f"REVIEW_{stage}_Report.json", 'w') as f:
            json.dump(report, f, indent=2)

    def _generate_markdown_report(self, stage: str, report: Dict) -> str:
        lines = [f"# {stage} Review Report", "", f"**Task ID**: {report['task_id']}",
                 f"**Timestamp**: {report['timestamp']}", f"**Recommendation**: {report['recommendation']}", "",
                 "## Summary", "", f"- **Total**: {report['summary']['total']}",
                 f"- **Passed**: {report['summary']['passed']} ✅",
                 f"- **Failed**: {report['summary']['failed']} ❌",
                 f"- **Critical Failed**: {report['summary']['critical_failed']}", "", "## Detailed Results", "",
                 "| Check | Status | Message |", "|-------|--------|---------|"]
        for r in report['results']:
            status = "✅ PASS" if r['passed'] else "❌ FAIL"
            lines.append(f"| {r['check']} | {status} | {r['message']} |")
        lines.extend(["", "## Sign-off", "", "| Role | Decision | Date |", "|------|----------|------|",
                      f"| Review Bot | {report['recommendation']} | {report['timestamp'][:10]} |",
                      "| AI Yang | ☐ | |", "| 实体Yang | ☐ | |"])
        return '\n'.join(lines)

    def _detect_stage_from_task(self, task: Dict) -> str:
        return task.get("stage", "IDR")


class FileExistsCheck:
    def __init__(self, relative_path: str):
        self.path = relative_path
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        fp = project_path / self.path
        exists = fp.exists()
        return CheckResult(f"FileExists: {self.path}", exists, f"{'Found' if exists else 'Missing'}: {self.path}", {"path": str(fp), "exists": exists})


class SectionCheck:
    def __init__(self, doc_path: str, required: List[str]):
        self.doc_path = doc_path
        self.required = required
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        fp = project_path / self.doc_path
        if not fp.exists():
            return CheckResult(f"SectionCheck: {self.doc_path}", False, f"Document not found: {self.doc_path}")
        content = fp.read_text()
        missing = [s for s in self.required if not re.search(rf"^##\s+(\d+\.\s+)?{re.escape(s)}", content, re.MULTILINE | re.IGNORECASE)]
        passed = len(missing) == 0
        return CheckResult(f"SectionCheck: {self.doc_path}", passed, f"Missing sections: {missing}" if missing else "All required sections present", {"required": self.required, "missing": missing})


class CoverageCheck:
    def __init__(self, min_line: int = 90, min_toggle: int = 85, min_fsm: int = 95):
        self.min_line = min_line
        self.min_toggle = min_toggle
        self.min_fsm = min_fsm
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        cov_db = project_path / "Verification/Coverage/coverage_report.json"
        if not cov_db.exists():
            return CheckResult("CoverageCheck", False, "Coverage report not found")
        data = json.loads(cov_db.read_text())
        line_cov = data.get("line", 0)
        toggle_cov = data.get("toggle", 0)
        fsm_cov = data.get("fsm", 0)
        passed = line_cov >= self.min_line and toggle_cov >= self.min_toggle and fsm_cov >= self.min_fsm
        return CheckResult("CoverageCheck", passed, f"Line: {line_cov}%, Toggle: {toggle_cov}%, FSM: {fsm_cov}%", {"line": line_cov, "toggle": toggle_cov, "fsm": fsm_cov})


class LintCheck:
    def __init__(self, errors_max: int = 0, warnings_max: int = 0):
        self.errors_max = errors_max
        self.warnings_max = warnings_max
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        result = subprocess.run(["make", "lint"], cwd=project_path / "tools", capture_output=True, text=True)
        errors = result.stdout.count("ERROR") + result.stderr.count("ERROR")
        warnings = result.stdout.count("WARNING") + result.stderr.count("WARNING")
        passed = errors <= self.errors_max and warnings <= self.warnings_max
        return CheckResult("LintCheck", passed, f"Errors: {errors}, Warnings: {warnings}", {"errors": errors, "warnings": warnings})


class BugCheck:
    def __init__(self, no_critical_major: bool = True):
        self.no_critical_major = no_critical_major
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        p1_dir = project_path / "ProjectMgmt/Bugs/P1_Critical"
        p2_dir = project_path / "ProjectMgmt/Bugs/P2_Major"
        p1_count = len(list(p1_dir.glob("*.md"))) if p1_dir.exists() else 0
        p2_count = len(list(p2_dir.glob("*.md"))) if p2_dir.exists() else 0
        passed = (p1_count == 0 and p2_count == 0) if self.no_critical_major else True
        return CheckResult("BugCheck", passed, f"P1: {p1_count}, P2: {p2_count}", {"p1": p1_count, "p2": p2_count})


class TimingCheck:
    def __init__(self, setup_slack_min: float = 0, hold_slack_min: float = 0):
        self.setup_slack_min = setup_slack_min
        self.hold_slack_min = hold_slack_min
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        sta_report = project_path / "design/STA/sta_signoff.rpt"
        if not sta_report.exists():
            return CheckResult("TimingCheck", False, "STA report not found")
        content = sta_report.read_text()
        setup_slack = self._extract_slack(content, "Setup")
        hold_slack = self._extract_slack(content, "Hold")
        passed = setup_slack >= self.setup_slack_min and hold_slack >= self.hold_slack_min
        return CheckResult("TimingCheck", passed, f"Setup: {setup_slack}ns, Hold: {hold_slack}ns", {"setup": setup_slack, "hold": hold_slack})
    def _extract_slack(self, content: str, timing_type: str) -> float:
        pattern = rf"{timing_type}.*slack.*=\s*([-\d.]+)"
        match = re.search(pattern, content, re.IGNORECASE)
        return float(match.group(1)) if match else float('-inf')


class PVCheck:
    def __init__(self, drc_clean: bool = True, lvs_clean: bool = True, antenna_clean: bool = True):
        self.drc_clean = drc_clean
        self.lvs_clean = lvs_clean
        self.antenna_clean = antenna_clean
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        pv_dir = project_path / "design/PV"
        drc_ok = self._check_clean(pv_dir / "drc.rpt") or not self.drc_clean
        lvs_ok = self._check_clean(pv_dir / "lvs.rpt") or not self.lvs_clean
        ant_ok = self._check_clean(pv_dir / "antenna.rpt") or not self.antenna_clean
        passed = drc_ok and lvs_ok and ant_ok
        return CheckResult("PVCheck", passed, f"DRC: {drc_ok}, LVS: {lvs_ok}, Antenna: {ant_ok}")
    def _check_clean(self, report: Path) -> bool:
        if not report.exists():
            return False
        return "ERROR" not in report.read_text().upper()


class RTLExistenceCheck:
    def __init__(self, rtl_dir: str):
        self.rtl_dir = rtl_dir
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        rtl = project_path / self.rtl_dir
        has_files = any(rtl.rglob("*.v")) or any(rtl.rglob("*.sv"))
        return CheckResult("RTLExistenceCheck", has_files, f"RTL files {'found' if has_files else 'missing'} in {self.rtl_dir}")


class MarkdownLintCheck:
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        return CheckResult("MarkdownLintCheck", True, "Placeholder")


class TraceabilityCheck:
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        return CheckResult("TraceabilityCheck", True, "Placeholder")


def main():
    parser = argparse.ArgumentParser(description="Review Bot - Automated Review Engine")
    parser.add_argument("--stage", help="Review stage (PCD/PAD/EDR/IDR/FDR)")
    parser.add_argument("--project", default=".", help="Project path")
    parser.add_argument("--task", help="Task ID")
    parser.add_argument("--all", action="store_true", help="Run all stages")
    parser.add_argument("--checks", help="Comma-separated list of specific checks")
    parser.add_argument("--dry-run", action="store_true", help="Generate report without saving")
    args = parser.parse_args()

    bot = ReviewBot(args.project)
    if args.all:
        for stage in ["PCD", "PAD", "EDR", "IDR", "FDR"]:
            bot.execute_review(stage, {"id": args.task or "unknown", "stage": stage})
    elif args.stage:
        bot.execute_review(args.stage, {"id": args.task or "unknown", "stage": args.stage})
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
