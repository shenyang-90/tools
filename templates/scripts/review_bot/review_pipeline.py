#!/usr/bin/env python3
"""
templates/scripts/review_bot/review_pipeline.py - AI Yang 并行质量检查流水线

Usage:
    # 完整流水线（推荐）
    python3 review_pipeline.py --stage IDR --project /path/to/project --task TASK-001

    # 指定检查项
    python3 review_pipeline.py --stage EDR --checks "FileExistence,DocStructure,Coverage"

    # 单检查项调试
    python3 review_pipeline.py --stage PAD --check-only FileExistence

    # 并行度控制
    python3 review_pipeline.py --stage IDR --parallel 4 --timeout 300

Integration:
    from review_pipeline import ReviewPipeline
    pipeline = ReviewPipeline(project_path)
    report = pipeline.run_gate_review("IDR", task_info)
"""

import json
import os
import sys
import argparse
import subprocess
import tempfile
import concurrent.futures
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Dict, Optional, Callable
from enum import Enum


class Severity(Enum):
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    INFO = "info"


class GateDecision(Enum):
    PASS = "PASS"
    CONDITIONAL = "CONDITIONAL"
    FAIL = "FAIL"


@dataclass
class CheckItem:
    """单个检查项的结果"""
    check_name: str
    passed: bool
    severity: Severity
    message: str
    details: Optional[Dict] = None
    evidence: Optional[str] = None  # 引用文件路径或日志片段


@dataclass
class CheckReport:
    """单个检查器的完整报告"""
    agent_name: str
    stage: str
    elapsed_seconds: float
    items: List[CheckItem] = field(default_factory=list)
    summary: str = ""
    raw_output: str = ""

    @property
    def all_passed(self) -> bool:
        return all(i.passed for i in self.items)

    @property
    def critical_count(self) -> int:
        return sum(1 for i in self.items if not i.passed and i.severity == Severity.CRITICAL)

    @property
    def major_count(self) -> int:
        return sum(1 for i in self.items if not i.passed and i.severity == Severity.MAJOR)


@dataclass
class PipelineReport:
    """流水线汇总报告"""
    stage: str
    task_id: str
    timestamp: str
    project_path: str
    reports: List[CheckReport] = field(default_factory=list)
    decision: GateDecision = GateDecision.PASS
    total_elapsed: float = 0.0

    def to_dict(self) -> Dict:
        return {
            "stage": self.stage,
            "task_id": self.task_id,
            "timestamp": self.timestamp,
            "project_path": str(self.project_path),
            "decision": self.decision.value,
            "total_elapsed": self.total_elapsed,
            "summary": {
                "total_checks": len(self.reports),
                "passed": sum(1 for r in self.reports if r.all_passed),
                "failed": sum(1 for r in self.reports if not r.all_passed),
                "critical_issues": sum(r.critical_count for r in self.reports),
                "major_issues": sum(r.major_count for r in self.reports),
            },
            "reports": [
                {
                    "agent": r.agent_name,
                    "passed": r.all_passed,
                    "elapsed": r.elapsed_seconds,
                    "critical": r.critical_count,
                    "major": r.major_count,
                    "items": [
                        {
                            "check": i.check_name,
                            "passed": i.passed,
                            "severity": i.severity.value,
                            "message": i.message,
                            "details": i.details,
                            "evidence": i.evidence,
                        }
                        for i in r.items
                    ],
                }
                for r in self.reports
            ],
        }


# ==============================================================================
# 检查器注册表 —— 每个检查器是一个可独立运行的函数
# ==============================================================================

def check_file_existence(project_path: Path, stage: str) -> CheckReport:
    """检查所有约定交付物是否存在且非空"""
    report = CheckReport(agent_name="FileExistenceAgent", stage=stage, elapsed_seconds=0.0)

    DELIVERABLES = {
        "PCD": ["README.md", "ProjectMgmt/Planning/MRD.md"],
        "PAD": ["docs/Arch/Architecture_Spec.md", "docs/FuSa/Safety_Concept.md"],
        "EDR": [
            "docs/Design/Design_Spec.md",
            "docs/Verification/Verification_Plan.md",
            "design/ip/Module_Name/synthesis.sdc",
            "design/ip/Module_Name/power_intent.upf",
        ],
        "IDR": [
            "design/RTL/",
            "Verification/Coverage/coverage_report.json",
            "tools/lint_report.md",
        ],
        "FDR": [
            "design/GDS/top.gds",
            "design/STA/sta_signoff.rpt",
            "design/PV/drc.rpt",
            "design/PV/lvs.rpt",
        ],
    }

    required = DELIVERABLES.get(stage, [])
    start = datetime.now()

    for rel_path in required:
        full = project_path / rel_path
        exists = full.exists()
        is_empty = False
        if exists and full.is_file():
            is_empty = full.stat().st_size == 0

        if not exists:
            report.items.append(CheckItem(
                check_name=f"FileExists: {rel_path}",
                passed=False,
                severity=Severity.CRITICAL,
                message=f"Missing: {rel_path}",
                evidence=str(full),
            ))
        elif is_empty:
            report.items.append(CheckItem(
                check_name=f"FileNotEmpty: {rel_path}",
                passed=False,
                severity=Severity.MAJOR,
                message=f"Empty file: {rel_path}",
                evidence=str(full),
            ))
        else:
            report.items.append(CheckItem(
                check_name=f"FileExists: {rel_path}",
                passed=True,
                severity=Severity.INFO,
                message=f"OK: {rel_path}",
            ))

    if not report.items:
        report.items.append(CheckItem(
            check_name="Deliverables",
            passed=True,
            severity=Severity.INFO,
            message="No deliverables defined for this stage",
        ))

    report.elapsed_seconds = (datetime.now() - start).total_seconds()
    return report


def check_doc_structure(project_path: Path, stage: str) -> CheckReport:
    """解析 Markdown 文档，检查章节完整性"""
    report = CheckReport(agent_name="DocStructureAgent", stage=stage, elapsed_seconds=0.0)
    start = datetime.now()

    SECTIONS = {
        "Design_Spec": [
            "Overview", "Functions", "Registers",
            "Block Design", "Interface", "Timing", "Power", "History",
        ],
        "Verification_Plan": [
            "Scope", "Test Strategy", "Coverage Plan",
            "Testbench Architecture", "Testcases", "Schedule", "History",
        ],
    }

    import re

    for doc_name, required in SECTIONS.items():
        # 查找文档（支持模糊匹配）
        candidates = list(project_path.rglob(f"*{doc_name}*")) + list(project_path.rglob(f"*design*spec*"))
        doc = None
        for c in candidates:
            if c.suffix == ".md":
                doc = c
                break

        if not doc or not doc.exists():
            report.items.append(CheckItem(
                check_name=f"DocExists: {doc_name}",
                passed=False,
                severity=Severity.CRITICAL,
                message=f"{doc_name} not found",
            ))
            continue

        content = doc.read_text()
        missing = []
        for sec in required:
            # 匹配 ## 开头的章节标题
            pattern = rf"^##\s+(\d+\.\s+)?{re.escape(sec)}"
            if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                missing.append(sec)

        if missing:
            report.items.append(CheckItem(
                check_name=f"Sections: {doc_name}",
                passed=False,
                severity=Severity.MAJOR,
                message=f"Missing sections: {', '.join(missing)}",
                details={"required": required, "missing": missing},
                evidence=str(doc),
            ))
        else:
            report.items.append(CheckItem(
                check_name=f"Sections: {doc_name}",
                passed=True,
                severity=Severity.INFO,
                message=f"All {len(required)} sections present",
                evidence=str(doc),
            ))

    report.elapsed_seconds = (datetime.now() - start).total_seconds()
    return report


def check_code_quality(project_path: Path, stage: str) -> CheckReport:
    """对 RTL 执行静态 Lint 检查"""
    report = CheckReport(agent_name="CodeQualityAgent", stage=stage, elapsed_seconds=0.0)
    start = datetime.now()

    if stage not in ("IDR", "FDR"):
        report.items.append(CheckItem(
            check_name="CodeQuality",
            passed=True,
            severity=Severity.INFO,
            message="Code quality checks not required for this stage",
        ))
        report.elapsed_seconds = 0.0
        return report

    # 尝试运行 make lint
    tools_dir = project_path / "tools"
    lint_report = project_path / "tools/lint_report.md"

    if tools_dir.exists():
        try:
            result = subprocess.run(
                ["make", "lint"],
                cwd=tools_dir,
                capture_output=True,
                text=True,
                timeout=300,
            )
            errors = result.stdout.count("ERROR") + result.stderr.count("ERROR")
            warnings = result.stdout.count("WARNING") + result.stderr.count("WARNING")

            report.items.append(CheckItem(
                check_name="LintErrors",
                passed=errors == 0,
                severity=Severity.CRITICAL if errors > 0 else Severity.INFO,
                message=f"Errors: {errors}, Warnings: {warnings}",
                details={"errors": errors, "warnings": warnings},
                evidence=str(lint_report) if lint_report.exists() else result.stdout[:500],
            ))
        except Exception as e:
            report.items.append(CheckItem(
                check_name="LintExecution",
                passed=False,
                severity=Severity.MAJOR,
                message=f"Lint execution failed: {e}",
            ))
    else:
        report.items.append(CheckItem(
            check_name="ToolsDir",
            passed=False,
            severity=Severity.MAJOR,
            message="tools/ directory not found",
        ))

    report.elapsed_seconds = (datetime.now() - start).total_seconds()
    return report


def check_coverage(project_path: Path, stage: str) -> CheckReport:
    """验证覆盖率报告是否达到阈值"""
    report = CheckReport(agent_name="CoverageAgent", stage=stage, elapsed_seconds=0.0)
    start = datetime.now()

    if stage not in ("IDR", "FDR"):
        report.items.append(CheckItem(
            check_name="Coverage",
            passed=True,
            severity=Severity.INFO,
            message="Coverage checks not required for this stage",
        ))
        report.elapsed_seconds = 0.0
        return report

    cov_file = project_path / "Verification/Coverage/coverage_report.json"
    if not cov_file.exists():
        report.items.append(CheckItem(
            check_name="CoverageReport",
            passed=False,
            severity=Severity.CRITICAL,
            message="Coverage report not found",
            evidence=str(cov_file),
        ))
        report.elapsed_seconds = (datetime.now() - start).total_seconds()
        return report

    try:
        data = json.loads(cov_file.read_text())
        thresholds = {"line": 90, "toggle": 85, "fsm": 95, "branch": 90}

        for metric, threshold in thresholds.items():
            value = data.get(metric, 0)
            passed = value >= threshold
            severity = Severity.INFO if passed else Severity.CRITICAL
            report.items.append(CheckItem(
                check_name=f"Coverage:{metric}",
                passed=passed,
                severity=severity,
                message=f"{metric.capitalize()}: {value}% (threshold: {threshold}%)",
                details={"value": value, "threshold": threshold},
                evidence=str(cov_file),
            ))
    except Exception as e:
        report.items.append(CheckItem(
            check_name="CoverageParse",
            passed=False,
            severity=Severity.CRITICAL,
            message=f"Failed to parse coverage report: {e}",
        ))

    report.elapsed_seconds = (datetime.now() - start).total_seconds()
    return report


def check_bug_status(project_path: Path, stage: str) -> CheckReport:
    """检查 Bug 清理状态"""
    report = CheckReport(agent_name="BugStatusAgent", stage=stage, elapsed_seconds=0.0)
    start = datetime.now()

    p1_dir = project_path / "ProjectMgmt/Bugs/P1_Critical"
    p2_dir = project_path / "ProjectMgmt/Bugs/P2_Major"

    p1_open = 0
    p2_open = 0

    if p1_dir.exists():
        p1_open = len([f for f in p1_dir.glob("*.md") if "CLOSED" not in f.read_text()[:2000]])
    if p2_dir.exists():
        p2_open = len([f for f in p2_dir.glob("*.md") if "CLOSED" not in f.read_text()[:2000]])

    # P1: 零容忍
    report.items.append(CheckItem(
        check_name="Bug:P1_Critical",
        passed=p1_open == 0,
        severity=Severity.CRITICAL if p1_open > 0 else Severity.INFO,
        message=f"P1 Critical open: {p1_open}",
        details={"p1_open": p1_open},
    ))

    # P2: IDR/FDR 阶段必须关闭
    if stage in ("IDR", "FDR"):
        report.items.append(CheckItem(
            check_name="Bug:P2_Major",
            passed=p2_open == 0,
            severity=Severity.CRITICAL if p2_open > 0 else Severity.INFO,
            message=f"P2 Major open: {p2_open}",
            details={"p2_open": p2_open},
        ))
    else:
        report.items.append(CheckItem(
            check_name="Bug:P2_Major",
            passed=True,
            severity=Severity.INFO,
            message=f"P2 Major open: {p2_open} (not required for {stage})",
        ))

    report.elapsed_seconds = (datetime.now() - start).total_seconds()
    return report


def check_traceability(project_path: Path, stage: str) -> CheckReport:
    """验证需求→设计→验证链路完整性"""
    report = CheckReport(agent_name="TraceabilityAgent", stage=stage, elapsed_seconds=0.0)
    start = datetime.now()

    # 简化的实现：检查关键文档间是否有交叉引用
    arch = project_path / "docs/Arch/Architecture_Spec.md"
    design = project_path / "docs/Design/Design_Spec.md"
    verify = project_path / "docs/Verification/Verification_Plan.md"

    arch_reqs = []
    design_refs = []
    verify_refs = []

    import re

    if arch.exists():
        content = arch.read_text()
        arch_reqs = re.findall(r"REQ-\d+", content)

    if design.exists():
        content = design.read_text()
        design_refs = re.findall(r"REQ-\d+", content)

    if verify.exists():
        content = verify.read_text()
        verify_refs = re.findall(r"REQ-\d+", content)

    missing_in_design = set(arch_reqs) - set(design_refs)
    missing_in_verify = set(arch_reqs) - set(verify_refs)

    if missing_in_design:
        report.items.append(CheckItem(
            check_name="Traceability:Arch→Design",
            passed=False,
            severity=Severity.MAJOR,
            message=f"Requirements missing in Design Spec: {missing_in_design}",
        ))
    else:
        report.items.append(CheckItem(
            check_name="Traceability:Arch→Design",
            passed=True,
            severity=Severity.INFO,
            message=f"All {len(arch_reqs)} requirements traced to Design Spec",
        ))

    if missing_in_verify:
        report.items.append(CheckItem(
            check_name="Traceability:Arch→Verify",
            passed=False,
            severity=Severity.MAJOR,
            message=f"Requirements missing in Verification Plan: {missing_in_verify}",
        ))
    else:
        report.items.append(CheckItem(
            check_name="Traceability:Arch→Verify",
            passed=True,
            severity=Severity.INFO,
            message=f"All {len(arch_reqs)} requirements traced to Verification Plan",
        ))

    report.elapsed_seconds = (datetime.now() - start).total_seconds()
    return report


def check_toolchain(project_path: Path, stage: str) -> CheckReport:
    """验证 EDA 工具链可用性"""
    report = CheckReport(agent_name="ToolchainAgent", stage=stage, elapsed_seconds=0.0)
    start = datetime.now()

    tools = ["iverilog", "verilator", "make"]
    for tool in tools:
        try:
            result = subprocess.run([tool, "--version"], capture_output=True, timeout=5)
            available = result.returncode == 0
        except Exception:
            available = False

        report.items.append(CheckItem(
            check_name=f"Tool:{tool}",
            passed=available,
            severity=Severity.MAJOR if not available else Severity.INFO,
            message=f"{tool}: {'available' if available else 'not found'}",
        ))

    # 检查 Makefile 存在性
    makefile = project_path / "tools/Makefile"
    report.items.append(CheckItem(
        check_name="MakefileExists",
        passed=makefile.exists(),
        severity=Severity.CRITICAL if not makefile.exists() else Severity.INFO,
        message="tools/Makefile found" if makefile.exists() else "tools/Makefile missing",
        evidence=str(makefile),
    ))

    report.elapsed_seconds = (datetime.now() - start).total_seconds()
    return report


def check_naming_convention(project_path: Path, stage: str) -> CheckReport:
    """检查命名规范合规性"""
    report = CheckReport(agent_name="NamingConventionAgent", stage=stage, elapsed_seconds=0.0)
    start = datetime.now()

    import re

    issues = []
    rtl_dir = project_path / "design/RTL"
    if rtl_dir.exists():
        for f in rtl_dir.rglob("*"):
            if f.is_file():
                # 模块名检查：应为 PascalCase
                if f.suffix in (".v", ".sv"):
                    content = f.read_text()
                    modules = re.findall(r"module\s+(\w+)", content)
                    for m in modules:
                        if not re.match(r"^[A-Z][a-zA-Z0-9_]*$", m):
                            issues.append(f"Module name '{m}' in {f} not PascalCase")

    if issues:
        report.items.append(CheckItem(
            check_name="Naming:RTL",
            passed=False,
            severity=Severity.MINOR,
            message=f"{len(issues)} naming issues found",
            details={"issues": issues[:10]},
        ))
    else:
        report.items.append(CheckItem(
            check_name="Naming:RTL",
            passed=True,
            severity=Severity.INFO,
            message="All RTL module names follow PascalCase",
        ))

    report.elapsed_seconds = (datetime.now() - start).total_seconds()
    return report


# ==============================================================================
# 检查器注册表
# ==============================================================================

CHECK_REGISTRY: Dict[str, Callable[[Path, str], CheckReport]] = {
    "FileExistence": check_file_existence,
    "DocStructure": check_doc_structure,
    "CodeQuality": check_code_quality,
    "Coverage": check_coverage,
    "BugStatus": check_bug_status,
    "Traceability": check_traceability,
    "Toolchain": check_toolchain,
    "NamingConvention": check_naming_convention,
}

# 各阶段默认启用的检查器
STAGE_DEFAULT_CHECKS = {
    "PCD": ["FileExistence", "DocStructure"],
    "PAD": ["FileExistence", "DocStructure", "Traceability"],
    "EDR": ["FileExistence", "DocStructure", "Traceability", "BugStatus"],
    "IDR": ["FileExistence", "DocStructure", "CodeQuality", "Coverage", "BugStatus", "Toolchain", "NamingConvention"],
    "FDR": ["FileExistence", "DocStructure", "CodeQuality", "Coverage", "BugStatus", "Toolchain"],
}


# ==============================================================================
# 流水线核心
# ==============================================================================

class ReviewPipeline:
    """AI Yang 并行质量检查流水线"""

    def __init__(self, project_path: str, parallel: int = 4, timeout: int = 300):
        self.project_path = Path(project_path)
        self.parallel = parallel
        self.timeout = timeout

    def run_gate_review(
        self,
        stage: str,
        task_info: Optional[Dict] = None,
        checks: Optional[List[str]] = None,
    ) -> PipelineReport:
        """
        执行完整的 Gate Review 流水线。

        Args:
            stage: PCD / PAD / EDR / IDR / FDR
            task_info: 任务信息字典，用于 report 中的 task_id
            checks: 指定检查器列表，None 则使用阶段默认值
        """
        task_id = task_info.get("task_id", "unknown") if task_info else "unknown"
        check_names = checks or STAGE_DEFAULT_CHECKS.get(stage, ["FileExistence"])

        start_time = datetime.now()
        report = PipelineReport(
            stage=stage,
            task_id=task_id,
            timestamp=start_time.isoformat(),
            project_path=str(self.project_path),
        )

        print(f"[Pipeline] Stage={stage} Task={task_id}")
        print(f"[Pipeline] Running {len(check_names)} checks in parallel (max={self.parallel})")

        # 并行执行所有检查器
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.parallel) as executor:
            future_map = {}
            for name in check_names:
                if name not in CHECK_REGISTRY:
                    print(f"[Pipeline] Warning: unknown check '{name}', skipping")
                    continue
                future = executor.submit(self._run_check_with_timeout, name, stage)
                future_map[future] = name

            for future in concurrent.futures.as_completed(future_map):
                name = future_map[future]
                try:
                    check_report = future.result(timeout=self.timeout)
                    report.reports.append(check_report)
                    status = "✅ PASS" if check_report.all_passed else "❌ FAIL"
                    print(f"[Pipeline] {name}: {status} ({check_report.elapsed_seconds:.1f}s)")
                except Exception as e:
                    print(f"[Pipeline] {name}: 💥 ERROR - {e}")
                    report.reports.append(CheckReport(
                        agent_name=name,
                        stage=stage,
                        elapsed_seconds=0.0,
                        items=[CheckItem(
                            check_name="Execution",
                            passed=False,
                            severity=Severity.CRITICAL,
                            message=f"Check execution failed: {e}",
                        )],
                    ))

        # 决策逻辑
        report.total_elapsed = (datetime.now() - start_time).total_seconds()
        report.decision = self._compute_decision(report)

        print(f"[Pipeline] Total elapsed: {report.total_elapsed:.1f}s")
        print(f"[Pipeline] Decision: {report.decision.value}")

        return report

    def _run_check_with_timeout(self, check_name: str, stage: str) -> CheckReport:
        """包装检查器执行，支持超时"""
        func = CHECK_REGISTRY[check_name]
        return func(self.project_path, stage)

    def _compute_decision(self, report: PipelineReport) -> GateDecision:
        """根据检查结果计算 Gate 决策"""
        total_critical = sum(r.critical_count for r in report.reports)
        total_major = sum(r.major_count for r in report.reports)
        all_passed = all(r.all_passed for r in report.reports)

        if all_passed:
            return GateDecision.PASS
        elif total_critical == 0:
            return GateDecision.CONDITIONAL
        else:
            return GateDecision.FAIL

    def save_report(self, report: PipelineReport, output_dir: Optional[Path] = None) -> Path:
        """保存报告到文件"""
        out = output_dir or self.project_path / "ProjectMgmt/Reviews" / report.stage
        out.mkdir(parents=True, exist_ok=True)

        # JSON 报告
        json_path = out / f"REVIEW_{report.stage}_Pipeline_Report.json"
        with open(json_path, "w") as f:
            json.dump(report.to_dict(), f, indent=2, ensure_ascii=False)

        # Markdown 报告
        md_path = out / f"REVIEW_{report.stage}_Pipeline_Report.md"
        md_path.write_text(self._generate_markdown(report))

        print(f"[Pipeline] Report saved: {md_path}")
        return md_path

    def _generate_markdown(self, report: PipelineReport) -> str:
        """生成 Markdown 格式报告"""
        lines = [
            f"# {report.stage} Pipeline Review Report",
            "",
            f"**Task ID**: {report.task_id}",
            f"**Timestamp**: {report.timestamp}",
            f"**Decision**: {report.decision.value}",
            f"**Total Elapsed**: {report.total_elapsed:.1f}s",
            "",
            "## Summary",
            "",
        ]

        summary = report.to_dict()["summary"]
        lines.extend([
            f"- **Total Checks**: {summary['total_checks']}",
            f"- **Passed**: {summary['passed']} ✅",
            f"- **Failed**: {summary['failed']} ❌",
            f"- **Critical Issues**: {summary['critical_issues']}",
            f"- **Major Issues**: {summary['major_issues']}",
            "",
            "## Detailed Results",
            "",
            "| Agent | Status | Critical | Major | Elapsed |",
            "|-------|--------|----------|-------|---------|",
        ])

        for r in report.reports:
            status = "✅" if r.all_passed else "❌"
            lines.append(f"| {r.agent_name} | {status} | {r.critical_count} | {r.major_count} | {r.elapsed_seconds:.1f}s |")

        lines.extend(["", "## Issue Details", ""])

        for r in report.reports:
            failed_items = [i for i in r.items if not i.passed]
            if failed_items:
                lines.append(f"### {r.agent_name}")
                for item in failed_items:
                    lines.append(f"- **{item.check_name}** ({item.severity.value})")
                    lines.append(f"  - {item.message}")
                    if item.evidence:
                        lines.append(f"  - Evidence: `{item.evidence}`")
                lines.append("")

        lines.extend([
            "",
            "## Sign-off",
            "",
            "| Role | Decision | Date |",
            "|------|----------|------|",
            f"| Review Bot | {report.decision.value} | {report.timestamp[:10]} |",
            "| AI Yang | ☐ | |",
            "| 实体Yang | ☐ | |",
            "",
            "---",
            "*Generated by review_pipeline.py*",
        ])

        return "\n".join(lines)


# ==============================================================================
# CLI 入口
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="AI Yang Review Pipeline")
    parser.add_argument("--stage", choices=["PCD", "PAD", "EDR", "IDR", "FDR"], help="Review stage")
    parser.add_argument("--project", default=".", help="Project path")
    parser.add_argument("--task", default="unknown", help="Task ID")
    parser.add_argument("--checks", help="Comma-separated check names (default: stage defaults)")
    parser.add_argument("--check-only", help="Run single check only (for debugging)")
    parser.add_argument("--parallel", type=int, default=4, help="Max parallel workers")
    parser.add_argument("--timeout", type=int, default=300, help="Per-check timeout (seconds)")
    parser.add_argument("--output", help="Report output directory (default: ProjectMgmt/Reviews/<STAGE>/)")
    parser.add_argument("--dry-run", action="store_true", help="Run checks but don't save report")
    parser.add_argument("--list-checks", action="store_true", help="List all available checks and exit")

    args = parser.parse_args()

    if args.list_checks:
        print("Available checks:")
        for name in CHECK_REGISTRY:
            print(f"  - {name}")
        print("\nStage defaults:")
        for stage, checks in STAGE_DEFAULT_CHECKS.items():
            print(f"  {stage}: {', '.join(checks)}")
        return

    pipeline = ReviewPipeline(
        project_path=args.project,
        parallel=args.parallel,
        timeout=args.timeout,
    )

    checks = None
    if args.check_only:
        checks = [args.check_only]
    elif args.checks:
        checks = [c.strip() for c in args.checks.split(",")]

    if not args.stage:
        parser.error("--stage is required unless --list-checks is used")

    report = pipeline.run_gate_review(
        stage=args.stage,
        task_info={"task_id": args.task},
        checks=checks,
    )

    if not args.dry_run:
        out_dir = Path(args.output) if args.output else None
        pipeline.save_report(report, output_dir=out_dir)

    # 返回码：PASS=0, CONDITIONAL=1, FAIL=2
    rc = {GateDecision.PASS: 0, GateDecision.CONDITIONAL: 1, GateDecision.FAIL: 2}
    sys.exit(rc[report.decision])


if __name__ == "__main__":
    main()
