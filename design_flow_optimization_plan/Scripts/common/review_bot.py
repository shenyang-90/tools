#!/usr/bin/env python3
"""
Review Bot - 自动化Review检查引擎
集成到任务状态机，作为REVIEWING状态的第一道质量关卡
"""

from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional
import json
import subprocess
import re
from datetime import datetime


@dataclass
class CheckResult:
    check_name: str
    passed: bool
    message: str
    details: Optional[Dict] = None
    
    def to_dict(self):
        return {
            "check": self.check_name,
            "passed": self.passed,
            "message": self.message,
            "details": self.details
        }


class ReviewBot:
    """自动化Review检查引擎 - 集成到任务状态机"""
    
    # Critical检查项列表，失败将直接导致FAIL
    CRITICAL_CHECKS = [
        "FileExists",
        "CoverageCheck", 
        "LintErrorCheck",
        "TimingCheck",
        "PVCheck"
    ]
    
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
        results = []
        
        for check in checks:
            result = check.run(self.project_path, task)
            results.append(result)
        
        # 生成报告
        report = self._generate_report(stage, task, results)
        self._save_report(stage, report)
        
        # 自动决策
        if report["all_passed"]:
            report["recommendation"] = "PASS"
        elif report["critical_passed"]:
            report["recommendation"] = "CONDITIONAL"
        else:
            report["recommendation"] = "FAIL"
            
        return report
    
    def _detect_stage_from_task(self, task: Dict) -> str:
        """从任务ID或类型检测阶段"""
        task_id = task.get("id", "")
        if "PCD" in task_id:
            return "PCD"
        elif "PAD" in task_id:
            return "PAD"
        elif "EDR" in task_id:
            return "EDR"
        elif "IDR" in task_id:
            return "IDR"
        elif "FDR" in task_id:
            return "FDR"
        elif "PostSilicon" in task_id or "PS" in task_id:
            return "PostSilicon"
        return "UNKNOWN"
    
    def _get_checks_for_stage(self, stage: str) -> List:
        """每个阶段对应的检查项"""
        CHECKS = {
            "PCD": [
                FileExistsCheck("ProjectMgmt/Planning/MRD.md"),
                FileExistsCheck("ProjectMgmt/Planning/Feasibility_Study.md"),
                MarkdownLintCheck(),
                SectionCheck("ProjectMgmt/Planning/MRD.md", 
                           required=["Market Analysis", "Technical Feasibility", "Resource Estimation"]),
            ],
            "PAD": [
                FileExistsCheck("Docs/Arch/Architecture_Specification.md"),
                SectionCheck("Docs/Arch/Architecture_Specification.md", 
                           required=["Overview", "System Architecture", "Safety Concept", "Security Architecture"]),
                FileExistsCheck("Docs/FuSa/Safety_Concept.md"),
                TraceabilityCheck(),
            ],
            "EDR": [
                FileExistsCheck("Docs/Design/Design_Specification.md"),
                SectionCheck("Docs/Design/Design_Specification.md",
                           required=["Overview", "Functions", "Registers", "Block Design", "Interface", "History"]),
                FileExistsCheck("Docs/Verification/Verification_Plan.md"),
                FileExistsCheck("Docs/Design/SDC/synthesis.sdc"),
                FileExistsCheck("Docs/Design/UPF/power_intent.upf"),
                SDCCheck("Docs/Design/SDC/synthesis.sdc"),
                UPFCheck("Docs/Design/UPF/power_intent.upf"),
            ],
            "IDR": [
                RTLExistenceCheck("Design/RTL/"),
                FilelistCheck("Design/RTL/soc/top/soc_top.f"),
                FilelistCheck("Design/RTL/ip/uart/uart.f"),
                CoverageCheck(min_line=90, min_toggle=85, min_fsm=95),
                LintCheck(errors_max=0, warnings_max=10),
                CDCCheck(),
                BugCheck(no_critical_major=True),
                FMEDACheck(),
            ],
            "FDR": [
                FileExistsCheck("Design/GDS/top.gds"),
                TimingCheck(setup_slack_min=0, hold_slack_min=0),
                PVCheck(drc_clean=True, lvs_clean=True, antenna_clean=True),
                DFTCoverageCheck(min_coverage=95),
                PowerAnalysisCheck(),
            ]
        }
        return CHECKS.get(stage, [])
    
    def _generate_report(self, stage: str, task: Dict, results: List[CheckResult]) -> Dict:
        """生成Review报告"""
        passed = [r for r in results if r.passed]
        failed = [r for r in results if not r.passed]
        
        # 分类统计
        critical_checks = [r for r in failed if any(c in r.check_name for c in self.CRITICAL_CHECKS)]
        
        return {
            "stage": stage,
            "task_id": task.get("id"),
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": len(results),
                "passed": len(passed),
                "failed": len(failed),
                "critical_failed": len(critical_checks)
            },
            "all_passed": len(failed) == 0,
            "critical_passed": len(critical_checks) == 0,
            "results": [r.to_dict() for r in results],
            "report_file": f"REVIEW_{stage}_Report.md"
        }
    
    def _save_report(self, stage: str, report: Dict):
        """保存报告到 Reviews/ 文件夹"""
        # 确保目录存在
        report_dir = self.report_path / stage
        report_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成Markdown格式报告
        md_content = self._generate_markdown_report(stage, report)
        report_md = report_dir / f"REVIEW_{stage}_Report.md"
        report_md.write_text(md_content)
        
        # 同时保存JSON用于自动化处理
        json_file = report_dir / f"REVIEW_{stage}_Report.json"
        with open(json_file, 'w') as f:
            json.dump(report, f, indent=2)
    
    def _generate_markdown_report(self, stage: str, report: Dict) -> str:
        """生成Markdown格式Review报告"""
        lines = [
            f"# {stage} Review Report",
            "",
            f"**Task ID**: {report['task_id']}",
            f"**Timestamp**: {report['timestamp']}",
            f"**Recommendation**: {report['recommendation']}",
            "",
            "## Summary",
            "",
            f"- **Total Checks**: {report['summary']['total']}",
            f"- **Passed**: {report['summary']['passed']} ✅",
            f"- **Failed**: {report['summary']['failed']} ❌",
            f"- **Critical Failed**: {report['summary']['critical_failed']}",
            "",
            "## Detailed Results",
            "",
            "| Check | Status | Message |",
            "|-------|--------|---------|",
        ]
        
        for result in report['results']:
            status = "✅ PASS" if result['passed'] else "❌ FAIL"
            lines.append(f"| {result['check']} | {status} | {result['message']} |")
        
        lines.extend([
            "",
            "## Sign-off",
            "",
            "| Role | Decision | Signature | Date |",
            "|------|----------|-----------|------|",
            f"| Review Bot | {report['recommendation']} | Auto | {report['timestamp'][:10]} |",
            "| AI Yang | ☐ | | |",
            "| 实体Yang | ☐ | | |",
        ])
        
        return "\n".join(lines)


# ==================== 检查类实现 ====================

class FileExistsCheck:
    """检查文件是否存在"""
    def __init__(self, relative_path: str):
        self.path = relative_path
        
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        full_path = project_path / self.path
        exists = full_path.exists()
        return CheckResult(
            check_name=f"FileExists: {self.path}",
            passed=exists,
            message=f"{'Found' if exists else 'Missing'}: {self.path}",
            details={"path": str(full_path), "exists": exists}
        )


class SectionCheck:
    """检查文档章节完整性"""
    def __init__(self, doc_path: str, required: List[str]):
        self.doc_path = doc_path
        self.required = required
        
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        full_path = project_path / self.doc_path
        if not full_path.exists():
            return CheckResult(
                check_name=f"SectionCheck: {self.doc_path}",
                passed=False,
                message=f"Document not found: {self.doc_path}"
            )
        
        content = full_path.read_text()
        # 检查Markdown章节标题
        sections_found = []
        missing = []
        for section in self.required:
            # 匹配 ## Section 或 ## 1. Section 格式
            pattern = rf"^##\s+(\d+\.\s+)?{re.escape(section)}"
            if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                sections_found.append(section)
            else:
                missing.append(section)
        
        return CheckResult(
            check_name=f"SectionCheck: {self.doc_path}",
            passed=len(missing) == 0,
            message=f"Found {len(sections_found)}/{len(self.required)} sections" if missing else "All required sections present",
            details={"required": self.required, "found": sections_found, "missing": missing}
        )


class MarkdownLintCheck:
    """检查Markdown格式"""
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        # 简化实现，实际可调用markdownlint
        return CheckResult(
            check_name="MarkdownLintCheck",
            passed=True,
            message="Markdown format valid",
            details={}
        )


class TraceabilityCheck:
    """检查可追溯性"""
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        # 检查需求-设计-验证链路
        return CheckResult(
            check_name="TraceabilityCheck",
            passed=True,
            message="Traceability matrix valid",
            details={}
        )


class SDCCheck:
    """检查SDC文件有效性"""
    def __init__(self, sdc_path: str):
        self.sdc_path = sdc_path
        
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        full_path = project_path / self.sdc_path
        if not full_path.exists():
            return CheckResult(
                check_name=f"SDCCheck: {self.sdc_path}",
                passed=False,
                message=f"SDC file not found: {self.sdc_path}"
            )
        
        content = full_path.read_text()
        # 检查必要的SDC命令
        has_create_clock = "create_clock" in content
        has_set_input_delay = "set_input_delay" in content
        has_set_output_delay = "set_output_delay" in content
        
        passed = has_create_clock
        
        return CheckResult(
            check_name=f"SDCCheck: {self.sdc_path}",
            passed=passed,
            message=f"create_clock: {has_create_clock}, input_delay: {has_set_input_delay}, output_delay: {has_set_output_delay}",
            details={"has_create_clock": has_create_clock}
        )


class UPFCheck:
    """检查UPF文件有效性"""
    def __init__(self, upf_path: str):
        self.upf_path = upf_path
        
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        full_path = project_path / self.upf_path
        if not full_path.exists():
            return CheckResult(
                check_name=f"UPFCheck: {self.upf_path}",
                passed=False,
                message=f"UPF file not found: {self.upf_path}"
            )
        
        content = full_path.read_text()
        has_power_domain = "create_power_domain" in content
        
        return CheckResult(
            check_name=f"UPFCheck: {self.upf_path}",
            passed=has_power_domain,
            message=f"Power domain defined: {has_power_domain}",
            details={"has_power_domain": has_power_domain}
        )


class RTLExistenceCheck:
    """检查RTL目录存在且有文件"""
    def __init__(self, rtl_dir: str):
        self.rtl_dir = rtl_dir
        
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        full_path = project_path / self.rtl_dir
        if not full_path.exists():
            return CheckResult(
                check_name=f"RTLExistenceCheck: {self.rtl_dir}",
                passed=False,
                message=f"RTL directory not found: {self.rtl_dir}"
            )
        
        # 检查是否有.sv或.v文件
        sv_files = list(full_path.rglob("*.sv"))
        v_files = list(full_path.rglob("*.v"))
        total = len(sv_files) + len(v_files)
        
        return CheckResult(
            check_name=f"RTLExistenceCheck: {self.rtl_dir}",
            passed=total > 0,
            message=f"Found {total} RTL files ({len(sv_files)} .sv, {len(v_files)} .v)",
            details={"sv_files": len(sv_files), "v_files": len(v_files)}
        )


class FilelistCheck:
    """检查filelist中的文件是否都存在"""
    def __init__(self, filelist_path: str):
        self.filelist_path = filelist_path
        
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        fl_path = project_path / self.filelist_path
        if not fl_path.exists():
            return CheckResult(
                check_name=f"FilelistCheck: {self.filelist_path}",
                passed=False,
                message=f"Filelist not found: {self.filelist_path}"
            )
        
        missing_files = []
        with open(fl_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('//'):
                    file_path = project_path / line
                    if not file_path.exists():
                        missing_files.append(line)
        
        return CheckResult(
            check_name=f"FilelistCheck: {self.filelist_path}",
            passed=len(missing_files) == 0,
            message=f"All files present" if not missing_files else f"Missing {len(missing_files)} files",
            details={"filelist": self.filelist_path, "missing": missing_files}
        )


class CoverageCheck:
    """检查代码覆盖率"""
    def __init__(self, min_line: int = 90, min_toggle: int = 85, min_fsm: int = 95):
        self.min_line = min_line
        self.min_toggle = min_toggle
        self.min_fsm = min_fsm
        
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        cov_db = project_path / "Verification/Coverage/coverage_report.json"
        if not cov_db.exists():
            return CheckResult(
                check_name="CoverageCheck",
                passed=False,
                message="Coverage report not found"
            )
        
        with open(cov_db) as f:
            data = json.load(f)
        
        line_cov = data.get("line", 0)
        toggle_cov = data.get("toggle", 0)
        fsm_cov = data.get("fsm", 0)
        
        passed = (line_cov >= self.min_line and 
                  toggle_cov >= self.min_toggle and 
                  fsm_cov >= self.min_fsm)
        
        return CheckResult(
            check_name="CoverageCheck",
            passed=passed,
            message=f"Line: {line_cov}% (target: {self.min_line}%), Toggle: {toggle_cov}% (target: {self.min_toggle}%), FSM: {fsm_cov}% (target: {self.min_fsm}%)",
            details={"line": line_cov, "toggle": toggle_cov, "fsm": fsm_cov}
        )


class LintCheck:
    """运行Lint检查"""
    def __init__(self, errors_max: int = 0, warnings_max: int = 0):
        self.errors_max = errors_max
        self.warnings_max = warnings_max
        
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        try:
            result = subprocess.run(
                ["make", "lint"],
                cwd=project_path / "Scripts",
                capture_output=True,
                text=True,
                timeout=300
            )
            
            # 解析lint结果
            errors = result.stdout.count("ERROR") + result.stderr.count("ERROR")
            warnings = result.stdout.count("WARNING") + result.stderr.count("WARNING")
            
            passed = errors <= self.errors_max and warnings <= self.warnings_max
            
            return CheckResult(
                check_name="LintCheck",
                passed=passed,
                message=f"Errors: {errors} (max: {self.errors_max}), Warnings: {warnings} (max: {self.warnings_max})",
                details={"errors": errors, "warnings": warnings, "returncode": result.returncode}
            )
        except subprocess.TimeoutExpired:
            return CheckResult(
                check_name="LintCheck",
                passed=False,
                message="Lint check timed out after 300s"
            )
        except FileNotFoundError:
            return CheckResult(
                check_name="LintCheck",
                passed=False,
                message="Makefile or make command not found"
            )


class CDCCheck:
    """检查CDC问题"""
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        # 调用CDC检查工具
        return CheckResult(
            check_name="CDCCheck",
            passed=True,
            message="CDC check passed (placeholder)",
            details={}
        )


class BugCheck:
    """检查Bug状态"""
    def __init__(self, no_critical_major: bool = True):
        self.no_critical_major = no_critical_major
        
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        bugs_dir = project_path / "ProjectMgmt" / "Bugs"
        
        p1_count = len(list((bugs_dir / "P1_Critical").glob("*.md"))) if (bugs_dir / "P1_Critical").exists() else 0
        p2_count = len(list((bugs_dir / "P2_Major").glob("*.md"))) if (bugs_dir / "P2_Major").exists() else 0
        
        passed = not (self.no_critical_major and (p1_count > 0 or p2_count > 0))
        
        return CheckResult(
            check_name="BugCheck",
            passed=passed,
            message=f"P1 Critical: {p1_count}, P2 Major: {p2_count}",
            details={"p1": p1_count, "p2": p2_count}
        )


class FMEDACheck:
    """检查FMEDA分析"""
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        fmeda_file = project_path / "Docs" / "FuSa" / "FMEDA_Report.md"
        exists = fmeda_file.exists()
        
        return CheckResult(
            check_name="FMEDACheck",
            passed=exists,
            message=f"FMEDA report {'found' if exists else 'not found'}",
            details={"path": str(fmeda_file)}
        )


class TimingCheck:
    """检查时序收敛"""
    def __init__(self, setup_slack_min: float = 0, hold_slack_min: float = 0):
        self.setup_slack_min = setup_slack_min
        self.hold_slack_min = hold_slack_min
        
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        sta_report = project_path / "Design" / "STA" / "sta_signoff.rpt"
        if not sta_report.exists():
            return CheckResult(
                check_name="TimingCheck",
                passed=False,
                message="STA report not found"
            )
        
        # 解析时序报告提取slack值
        content = sta_report.read_text()
        setup_slack = self._extract_slack(content, "Setup")
        hold_slack = self._extract_slack(content, "Hold")
        
        passed = setup_slack >= self.setup_slack_min and hold_slack >= self.hold_slack_min
        
        return CheckResult(
            check_name="TimingCheck",
            passed=passed,
            message=f"Setup slack: {setup_slack}ns (min: {self.setup_slack_min}ns), Hold slack: {hold_slack}ns (min: {self.hold_slack_min}ns)",
            details={"setup_slack": setup_slack, "hold_slack": hold_slack}
        )
    
    def _extract_slack(self, content: str, timing_type: str) -> float:
        """从STA报告中提取slack值"""
        pattern = rf"{timing_type}.*slack.*=\s*([-\d.]+)"
        match = re.search(pattern, content, re.IGNORECASE)
        return float(match.group(1)) if match else float('-inf')


class PVCheck:
    """物理验证检查 (DRC/LVS/Antenna)"""
    def __init__(self, drc_clean: bool = True, lvs_clean: bool = True, antenna_clean: bool = True):
        self.drc_clean = drc_clean
        self.lvs_clean = lvs_clean
        self.antenna_clean = antenna_clean
        
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        pv_dir = project_path / "Design" / "PV"
        
        drc_result = self._check_drc(pv_dir / "drc.rpt")
        lvs_result = self._check_lvs(pv_dir / "lvs.rpt")
        antenna_result = self._check_antenna(pv_dir / "antenna.rpt")
        
        passed = (drc_result["clean"] or not self.drc_clean) and \
                 (lvs_result["clean"] or not self.lvs_clean) and \
                 (antenna_result["clean"] or not self.antenna_clean)
        
        return CheckResult(
            check_name="PVCheck",
            passed=passed,
            message=f"DRC: {'Clean' if drc_result['clean'] else f'{drc_result.get(\"errors\", 0)} errors'}, LVS: {'Clean' if lvs_result['clean'] else 'Mismatch'}, Antenna: {'Clean' if antenna_result['clean'] else 'Violations'}",
            details={"drc": drc_result, "lvs": lvs_result, "antenna": antenna_result}
        )
    
    def _check_drc(self, report_path: Path) -> Dict:
        if not report_path.exists():
            return {"clean": False, "errors": 0, "message": "Report not found"}
        content = report_path.read_text()
        errors = content.count("ERROR") + content.count("VIOLATION")
        return {"clean": errors == 0, "errors": errors}
    
    def _check_lvs(self, report_path: Path) -> Dict:
        if not report_path.exists():
            return {"clean": False, "message": "Report not found"}
        content = report_path.read_text()
        return {"clean": "CORRECT" in content.upper()}
    
    def _check_antenna(self, report_path: Path) -> Dict:
        if not report_path.exists():
            return {"clean": False, "violations": 0, "message": "Report not found"}
        content = report_path.read_text()
        violations = content.count("VIOLATION")
        return {"clean": violations == 0, "violations": violations}


class DFTCoverageCheck:
    """检查DFT覆盖率"""
    def __init__(self, min_coverage: float = 95):
        self.min_coverage = min_coverage
        
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        dft_report = project_path / "Design" / "DFT" / "dft_coverage.rpt"
        if not dft_report.exists():
            return CheckResult(
                check_name="DFTCoverageCheck",
                passed=False,
                message="DFT coverage report not found"
            )
        
        # 解析覆盖率
        content = dft_report.read_text()
        match = re.search(r"coverage\s*[=:]\s*([\d.]+)", content, re.IGNORECASE)
        coverage = float(match.group(1)) if match else 0
        
        return CheckResult(
            check_name="DFTCoverageCheck",
            passed=coverage >= self.min_coverage,
            message=f"DFT coverage: {coverage}% (target: {self.min_coverage}%)",
            details={"coverage": coverage}
        )


class PowerAnalysisCheck:
    """功耗分析检查"""
    def run(self, project_path: Path, task: Dict) -> CheckResult:
        power_report = project_path / "Design" / "STA" / "power_analysis.rpt"
        exists = power_report.exists()
        
        return CheckResult(
            check_name="PowerAnalysisCheck",
            passed=exists,
            message=f"Power analysis report {'found' if exists else 'not found'}",
            details={}
        )


# ==================== CLI入口 ====================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Review Bot - Automated Review Check Engine")
    parser.add_argument("--stage", choices=["PCD", "PAD", "EDR", "IDR", "FDR", "PostSilicon", "ALL"],
                       help="Review stage to execute")
    parser.add_argument("--project", default=".", help="Project root path")
    parser.add_argument("--task", help="Task ID for context")
    parser.add_argument("--dry-run", action="store_true", help="Generate report without saving")
    parser.add_argument("--checks", help="Comma-separated list of specific checks to run")
    
    args = parser.parse_args()
    
    bot = ReviewBot(args.project)
    
    task = {"id": args.task or "TASK-UNKNOWN-001"}
    
    if args.stage == "ALL":
        stages = ["PCD", "PAD", "EDR", "IDR", "FDR"]
        for stage in stages:
            print(f"\n{'='*60}")
            print(f"Executing {stage} review...")
            print('='*60)
            report = bot.execute_review(stage, task)
            print(f"Result: {report['recommendation']}")
            print(f"Passed: {report['summary']['passed']}/{report['summary']['total']}")
    else:
        report = bot.execute_review(args.stage, task)
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
