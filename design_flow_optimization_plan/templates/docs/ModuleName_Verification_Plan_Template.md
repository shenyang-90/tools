# Verification Plan

**Project**: [Project Name]  
**Module**: [Module Name]  
**Version**: v0.1.0  
**Author**: [Author Name]  
**Date**: 2026-04-03  

---

## 1. Overview

### 1.1 Purpose
[Describe the purpose of this verification plan]

### 1.2 Scope
[Define what is in scope and out of scope for verification]

### 1.3 Verification Strategy
[High-level verification strategy: simulation, formal, emulation, etc.]

---

## 2. Testbench Architecture

### 2.1 Testbench Block Diagram
```
+------------------+        +------------------+        +------------------+
|   Test Sequence  |------>|   DUT (Device   |------>|   Scoreboard     |
|                  |        |   Under Test)    |        |   & Checker      |
+------------------+        +------------------+        +------------------+
         |                           |                           |
         v                           v                           v
+------------------+        +------------------+        +------------------+
|   Configuration  |        |   Interface      |        |   Coverage       |
|   Database       |        |   Agents         |        |   Collection     |
+------------------+        +------------------+        +------------------+
```

### 2.2 Components Description

#### 2.2.1 Interface Agents
| Agent | Protocol | Description |
|-------|----------|-------------|
| apb_agent | APB4 | APB bus interface |
| uart_agent | UART | UART serial interface |

#### 2.2.2 Sequences
[Description of test sequences]

#### 2.2.3 Scoreboard
[Description of scoreboard and checking strategy]

---

## 3. Test Plan

### 3.1 Test Categories

#### 3.1.1 Sanity Tests
| Test Name | Description | Pass Criteria |
|-----------|-------------|---------------|
| tc_sanity_reset | Verify reset behavior | DUT returns to known state |
| tc_sanity_reg_access | Verify register read/write | All registers accessible |

#### 3.1.2 Feature Tests
| Test Name | Feature | Description | Pass Criteria |
|-----------|---------|-------------|---------------|
| tc_feature_tx | TX operation | Verify TX functionality | Data transmitted correctly |
| tc_feature_rx | RX operation | Verify RX functionality | Data received correctly |
| tc_feature_fifo | FIFO operation | Verify FIFO behavior | No overflow/underflow |
| tc_feature_irq | Interrupts | Verify interrupt generation | Correct IRQ timing |

#### 3.1.3 Error Tests
| Test Name | Error Scenario | Description | Pass Criteria |
|-----------|----------------|-------------|---------------|
| tc_err_framing | Framing error | Inject framing error | Error detected and reported |
| tc_err_overrun | Overrun error | Cause RX overrun | Error detected and reported |

#### 3.1.4 Stress Tests
| Test Name | Description | Pass Criteria |
|-----------|-------------|---------------|
| tc_stress_rand | Random traffic | 1M transactions without error |
| tc_stress_concurrent | Concurrent operations | All operations complete |

### 3.2 Regression Strategy

#### 3.2.1 Smoke Regression
- Duration: 15 minutes
- Tests: Sanity tests + basic feature tests
- Frequency: Every commit

#### 3.2.2 Nightly Regression
- Duration: 4 hours
- Tests: Full feature tests + random tests
- Frequency: Nightly

#### 3.2.3 Weekly Regression
- Duration: 24 hours
- Tests: All tests including stress tests
- Frequency: Weekly

---

## 4. Coverage Plan

### 4.1 Code Coverage
| Metric | Target | Method |
|--------|--------|--------|
| Line Coverage | 95% | Simulation |
| Toggle Coverage | 90% | Simulation |
| Branch Coverage | 90% | Simulation |
| FSM Coverage | 100% | Simulation |
| Expression Coverage | 85% | Simulation |

### 4.2 Functional Coverage

#### 4.2.1 Configuration Coverage
| Covergroup | Bins | Description |
|------------|------|-------------|
| cg_baud_rate | 8 | All supported baud rates |
| cg_data_bits | 4 | 5, 6, 7, 8 data bits |
| cg_parity | 3 | None, Odd, Even parity |

#### 4.2.2 Operation Coverage
| Covergroup | Bins | Description |
|------------|------|-------------|
| cg_tx_status | 4 | TX idle, busy, done, error |
| cg_rx_status | 4 | RX idle, receiving, done, error |
| cg_fifo_level | 8 | FIFO fill levels |

### 4.3 Coverage Closure Criteria
- All coverpoints hit at least once
- All coverage targets met
- Review and waive any uncovered code with justification

---

## 5. Verification Environment

### 5.1 Tools and Versions
| Tool | Version | Purpose |
|------|---------|---------|
| Simulator | Xcelium 23.03 | Simulation |
| Coverage | IMC 23.03 | Coverage analysis |
| Lint | SpyGlass 5.6 | Static checking |
| CDC | Questa CDC 2023.1 | CDC checking |

### 5.2 Compilation Options
```
+define+UVM_NO_DEPRECATED
+incdir+$(UVM_HOME)/src
$(UVM_HOME)/src/uvm_pkg.sv
-timescale 1ns/1ps
-access +rwc
- Coverage options
-coverage line+tgl+cond+fsm+branch
```

---

## 6. Sign-off Criteria

| Criteria | Target | Status |
|----------|--------|--------|
| All tests pass | 100% | ☐ |
| Code coverage | >= 95% | ☐ |
| Functional coverage | >= 95% | ☐ |
| Lint clean | 0 errors | ☐ |
| CDC clean | 0 errors | ☐ |
| Reviews complete | All | ☐ |

---

## 7. History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v0.1.0 | 2026-04-03 | [Author] | Initial version |
| v0.2.0 | 2026-04-15 | [Author] | Added coverage plan |
| v0.3.0 | 2026-04-28 | [Author] | Updated regression strategy |

---

*End of Document*
