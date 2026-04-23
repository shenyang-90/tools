#!/usr/bin/env python3
"""
templates/agent/agent.py - Coding Yang 本地Agent模板

Usage:
    python3 agent.py
"""

import os
import json
import asyncio
import websockets
from pathlib import Path
from datetime import datetime


class CodingYangAgent:
    """Coding Yang本地Agent"""

    def __init__(self):
        self.agent_id = "coding_yang"
        self.gateway_url = os.getenv("OPENCLAW_GATEWAY")
        self.workspace = Path(os.getenv("WORKSPACE", "/workspace"))
        self.active_tasks = {}

    async def run(self):
        """主循环"""
        async with websockets.connect(self.gateway_url) as ws:
            await self._register(ws)
            while True:
                message = await ws.recv()
                await self._handle_message(ws, json.loads(message))

    async def _register(self, ws):
        await ws.send(json.dumps({
            "type": "register",
            "agent_id": self.agent_id,
            "capabilities": ["rtl_coding", "simulation", "lint", "synthesis", "debug"],
            "eda_tools": self._detect_eda_tools()
        }))

    def _detect_eda_tools(self):
        tools = []
        for name, cmd in [("iverilog", "iverilog -V"), ("verilator", "verilator --version"),
                          ("yosys", "yosys -V"), ("openroad", "openroad -version")]:
            if self._cmd_exists(name):
                tools.append({"name": name, "type": "simulation"})
        for name in ["vcs", "dc_shell", "innovus", "pt_shell", "tessent"]:
            if self._cmd_exists(name):
                tools.append({"name": name, "type": "commercial", "license": "checked"})
        return tools

    async def _handle_message(self, ws, message):
        msg_type = message.get("type")
        if msg_type == "task_assign":
            await self._handle_task_assign(ws, message)
        elif msg_type == "task_cancel":
            await self._handle_task_cancel(ws, message)
        elif msg_type == "status_query":
            await self._handle_status_query(ws, message)

    async def _handle_task_assign(self, ws, message):
        task = message["task"]
        task_id = task["task_id"]
        self.active_tasks[task_id] = {"task": task, "status": "accepted", "start_time": datetime.now().isoformat()}
        await ws.send(json.dumps({"type": "task_accepted", "task_id": task_id, "agent_id": self.agent_id}))
        asyncio.create_task(self._execute_task(ws, task))

    async def _execute_task(self, ws, task):
        task_id = task["task_id"]
        try:
            self.active_tasks[task_id]["status"] = "running"
            # 实际执行任务...
            result = {"status": "success", "message": "Task completed"}
            await ws.send(json.dumps({"type": "task_completed", "task_id": task_id, "result": result}))
        except Exception as e:
            await ws.send(json.dumps({"type": "task_failed", "task_id": task_id, "error": str(e)}))
        finally:
            del self.active_tasks[task_id]

    def _cmd_exists(self, cmd):
        return os.system(f"which {cmd} > /dev/null 2>&1") == 0


if __name__ == "__main__":
    agent = CodingYangAgent()
    asyncio.run(agent.run())
