# IDR (Implementation Design Review) Checklist - Module Level

> 适用于IDR阶段的模块级评审，包含42项详细检查项
> 命名规范: `IDR_Checklist_[ModuleName]_v[X.X]_[YYYYMMDD].md`

---

## 基本信息

| 字段 | 值 |
|------|-----|
| **评审阶段** | IDR - Implementation Design Review |
| **模块名称** | {{MODULE_NAME}} |
| **项目名称** | {{PROJECT_NAME}} |
| **评审日期** | {{DATE}} |
| **版本** | {{VERSION}} |
| **评审人** | {{REVIEWERS}} |
| **评审结果** | ☐ PASS / ☐ CONDITIONAL / ☐ FAIL |

---

## 检查项汇总表

| 类别 | Critical | Major | Minor | 总计 | 符合 | 不符合 | 不适用 | 符合率 |
|------|----------|-------|-------|------|------|--------|--------|--------|
| Common Design | 6 | 10 | 2 | 18 | | | | |
| Common Low Power | 1 | 1 | 0 | 2 | | | | |
| Common CDC | 5 | 4 | 0 | 9 | | | | |
| Common DFT | 3 | 10 | 0 | 13 | | | | |
| **总计** | **15** | **25** | **2** | **42** | | | | |

**通过标准**:
- 🔴 **Critical (15项)**: 必须全部符合
- 🟡 **Major (25项)**: 符合率 >= 80% (至少20项符合)
- 🟢 **Minor (2项)**: 无硬性要求

---

## Common Design

### 1. 🔴 第三方IP配置工程及源代码 [Critical]
- **描述**: 第三方IP的配置工程及源代码，需要在 `/pub/lib1/ip/project` 目录
- **参考文档**: `Database/Docs/Design/Third_Party_IP_Integration.md`
- **验证方法**: 检查IP目录结构和配置文件
- **验收标准**: 所有第三方IP已正确配置并放入指定目录
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 2. 🔴 Memory Wrapper控制信号连接 [Critical]
- **描述**: Memory Wrapper的控制信号（时钟复位、ECC、AutoClear、Memory Cell控制信号等）连接正确，并且有对应验证用例覆盖
- **参考文档**: `Database/Docs/Design/Memory_Wrapper_Spec.md`
- **验证方法**: 检查RTL连接和验证用例覆盖报告
- **验收标准**: 所有控制信号正确连接，验证用例覆盖率>90%
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 3. 🔴 顶层模块命名规则 [Critical]
- **描述**: 顶层模块名不能与模块内部的子模块例化名重复，会影响powerpro的分析结果
- **参考文档**: `Database/Docs/Design/Coding_Style_Guide.md`
- **验证方法**: 运行命名检查脚本
- **验收标准**: 无命名冲突，powerpro分析无相关Warning
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 4. 🔴 IO Skew约束 [Critical]
- **描述**: IO Skew约束完整正确
- **参考文档**: `Database/Docs/Design/IO_Constraints.md`
- **验证方法**: 检查SDC约束文件
- **验收标准**: 所有IO的skew约束已定义，满足时序要求
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 5. 🔴 Common模块例化规则 - 时钟复位 [Critical]
- **描述**: StandardCell、DelayChain、ClockMonitor、ClkGen需要例化Common模块，时钟路径的例化需要增加前缀 `i_done_clk_`，复位路径的例化需要增加前缀 `i_done_rst_`
- **参考文档**: `Database/Docs/Design/Common_Cell_Usage.md`
- **验证方法**: 检查RTL代码命名
- **验收标准**: 所有Common模块例化符合命名规范
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 6. 🔴 ECO Cell例化规则 [Critical]
- **描述**: 每个模块必须例化ECO Cell，并且增加前缀 `i_dont_eco_`；ECO Cell中的复位有效电平，与模块中一致
- **参考文档**: `Database/Docs/Design/ECO_Cell_Guide.md`
- **验证方法**: 检查RTL代码
- **验收标准**: 每个模块包含ECO Cell，命名和复位电平正确
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 7. 🟡 时钟作为数据使用 [Major]
- **描述**: 时钟作为数据使用，在触发器前需例化Common模块databuffer，前缀`i_dont_data_buffer_`，通知STA、PR工程师
- **参考文档**: `Database/Docs/Design/Clock_as_Data.md`
- **验证方法**: 检查RTL代码和STA/PR通知记录
- **验收标准**: 所有时钟作为数据使用的地方已例化databuffer并通知后端
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 8. 🟡 OTP Preload时序确认 [Major]
- **描述**: 确认模块输入的OTP Preload bit与模块输入的时钟、复位、其他控制信号的时序要求
- **参考文档**: `Database/Docs/Design/OTP_Timing_Spec.md`
- **验证方法**: 检查时序分析报告
- **验收标准**: OTP Preload时序满足setup/hold要求
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 9. 🟡 Harden模块时钟规则 [Major]
- **描述**: Harden模块禁止有多个同频且同步的输入时钟，禁止有多个同频且同步的输出时钟
- **参考文档**: `Database/Docs/Design/Harden_Module_Spec.md`
- **验证方法**: 检查Harden模块接口定义
- **验收标准**: Harden模块时钟接口符合规则
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 10. 🟡 Harden模块复位同步 [Major]
- **描述**: Harden模块输入的复位需要在Harden内部增加复位同步
- **参考文档**: `Database/Docs/Design/Harden_Module_Spec.md`
- **验证方法**: 检查Harden RTL代码
- **验收标准**: Harden内部包含复位同步逻辑
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 11. 🟡 ROM Code Size处理 [Major]
- **描述**: ROM Code Size大于ROM Compiler最大size时，需要生成多个不同文件名的ROM Micro，并且每个ROM Micro的初始化文件不同
- **参考文档**: `Database/Docs/Design/ROM_Integration_Guide.md`
- **验证方法**: 检查ROM配置和初始化文件
- **验收标准**: 大容量ROM正确分割，初始化文件独立
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 12. 🟡 Analog SerDes/LVDS TX/RX设计 [Major]
- **描述**: Analog SerDes/LVDS的TX和RX设计：
  1. TX功能逻辑和测试逻辑（PRBS、内部回环）切换后，需要增加一级寄存器输出
  2. RX输入到Digital后增加一级寄存器后，连接到功能逻辑和测试逻辑
  3. TX和RX的并行接口，增加bit顺序控制寄存器
- **参考文档**: `Database/Docs/Design/SerDes_Design_Guide.md`
- **验证方法**: 检查RTL代码
- **验收标准**: TX/RX数据路径包含寄存器隔离，bit顺序可配置
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 13. 🟡 Analog SerDes/LVDS测试电路 [Major]
- **描述**: Analog SerDes/LVDS的TX和RX增加测试电路：
  1. TX发送PRBS，输出给Analog的并行接口，确认LSB、MSB；需要考虑FPGA眼图测试工具bit顺序
  2. RX检查PRBS，输入的Analog并行接口，确认LSB、MSB
  3. TX和RX回环，如果TX和RX时钟异步，需要增加异步FIFO
  4. TX测试enable和RX测试enable需要不同寄存器bit控制
- **参考文档**: `Database/Docs/Design/SerDes_Test_Circuit.md`
- **验证方法**: 检查测试电路RTL和验证用例
- **验收标准**: PRBS生成/检查、回环测试、独立控制位实现
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 14. 🟡 For循环使用限制 [Major]
- **描述**: 除Generate外，禁止使用For循环
- **参考文档**: `Database/Docs/Design/Coding_Style_Guide.md`
- **验证方法**: Lint工具检查
- **验收标准**: 无非法For循环使用
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 15. 🟡 特殊pattern保护状态 [Major]
- **描述**: 寄存器中特殊pattern保护的enable/disable状态，需要增加enable/disable的状态bit
- **参考文档**: `Database/Docs/Design/State_Machine_Design.md`
- **验证方法**: 检查状态机RTL
- **验收标准**: 所有保护状态有独立的状态bit
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 16. 🟡 Security域寄存器配置 [Major]
- **描述**: security相关的时钟、复位、电源、ANA ISO相关控制寄存器需要放到security domain
- **参考文档**: `Database/Docs/Design/Security_Architecture.md`
- **验证方法**: 检查寄存器映射和安全区域划分
- **验收标准**: Security相关寄存器位于security domain
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 17. 🟡 Analog Digital Interface隔离控制 [Major]
- **描述**: Analog digital interface的isolation控制
- **参考文档**: `Database/Docs/Design/Isolation_Control.md`
- **验证方法**: 检查UPF/CPF和RTL实现
- **验收标准**: Isolation控制逻辑正确实现
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 18. 🟢 Memory Wrapper/Common Cell控制信号检查 [Minor]
- **描述**: 检查memory wrapper/common cell的控制信号连接正确
- **参考文档**: `Database/Docs/Design/Common_Cell_Checklist.md`
- **验证方法**: 检查RTL连接
- **验收标准**: 控制信号连接正确
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

---

## Common Low Power

### 19. 🔴 Analog非AON信号连接 [Critical]
- **描述**: Analog非AON信号同时连接到digital AON和digital非AON，digital AON前不需要加AON buffer
- **参考文档**: `Database/Docs/Design/Low_Power_Design.md`
- **验证方法**: 检查电源域连接和UPF
- **验收标准**: AON路径正确，无不必要的buffer
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 20. 🟡 Analog AON信号连接 [Major]
- **描述**: Analog AON信号同时连接到digital AON和digital非AON，digital设计需要保证AON输出后给非AON，digital非AON不直接连接analog AON
- **参考文档**: `Database/Docs/Design/Low_Power_Design.md`
- **验证方法**: 检查电源域连接
- **验收标准**: AON信号正确路由，无非AON直接连接
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

---

## Common CDC

### 21. 🔴 HWE2 ASYNC表格 [Critical]
- **描述**: HWE2 ASYNC表格完整正确
- **参考文档**: `Database/Docs/Design/CDC_Spec.md`
- **验证方法**: 检查CDC分析工具和表格
- **验收标准**: 所有跨时钟域信号已记录并检查
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 22. 🔴 data_sync_level复位值确认 [Critical]
- **描述**: 确认data_sync_level2level的复位值
- **参考文档**: `Database/Docs/Design/CDC_Sync_Cell.md`
- **验证方法**: 检查RTL代码
- **验收标准**: 复位值定义正确，符合设计要求
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 23. 🔴 Toggle信号复位处理 [Critical]
- **描述**: Toggle类型的控制信号，控制逻辑和被控制逻辑，如果复位源不同，需要保证控制逻辑被复位，被控制逻辑不受影响。例如：memory wrapper中的refresh enable信号是toggle类型，refresh enable寄存器被复位时可能产生一次toggle，memory wrapper如果不是同一个复位源，会触发一次非预期的memory refresh
- **参考文档**: `Database/Docs/Design/CDC_Toggle_Signal.md`
- **验证方法**: 检查跨复位域的toggle信号
- **验收标准**: Toggle信号复位处理正确，无异常触发
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 24. 🔴 格雷码异步接口 [Critical]
- **描述**: 使用格雷码的异步接口，格雷码必须寄存器输出
- **参考文档**: `Database/Docs/Design/Gray_Code_CDC.md`
- **验证方法**: 检查RTL代码
- **验收标准**: 格雷码信号已寄存
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 25. 🔴 Spyglass环境检查 [Critical]
- **描述**: 确认Spyglass环境无BlackBox
- **参考文档**: `Database/Docs/Design/Spyglass_Setup.md`
- **验证方法**: 运行Spyglass检查
- **验收标准**: 无BlackBox相关的Error/Warning
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 26. 🟡 异步FIFO使用规则 [Major]
- **描述**: 异步FIFO必须使用Common模块，并且FIFO读写1个cycle不能2笔或更多
- **参考文档**: `Database/Docs/Design/Async_FIFO_Usage.md`
- **验证方法**: 检查FIFO实现和时序
- **验收标准**: 使用Common FIFO，无背靠背写入
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 27. 🟡 异步FIFO约束 [Major]
- **描述**: 异步FIFO必须增加完整约束，参考Design Rule-异步FIFO约束，约束增加到spec.tcl
- **参考文档**: `Database/Docs/Design/Async_FIFO_Constraints.md`
- **验证方法**: 检查SDC约束文件
- **验收标准**: 所有异步FIFO约束完整
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 28. 🟡 data_sync_pulse2pulse复位要求 [Major]
- **描述**: IP中若使用common模块中的data_sync_pulse2pulse，需在手册中注明新一次的data_i操作（如软件配某个寄存器的行为），必须在对应时钟域下的复位释放1us后才可以重新进行。若tx,rx的复位由同一个复位源经过两个时钟同步后驱动，则声明模块的该复位释放1us后才可以重新进行传输
- **参考文档**: `Database/Docs/Design/Pulse_Sync_Reset.md`
- **验证方法**: 检查IP手册和RTL实现
- **验收标准**: 手册已注明复位要求，实现符合要求
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 29. 🟢 异步FIFO深度检查 [Minor]
- **描述**: 异步FIFO深度满足设计要求，无溢出/欠载风险
- **参考文档**: `Database/Docs/Design/Async_FIFO_Depth.md`
- **验证方法**: 检查FIFO深度计算
- **验收标准**: FIFO深度正确，已考虑burst情况
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

---

## Common DFT

### 30. 🔴 Spyglass DFT Waive同步 [Critical]
- **描述**: Spyglass DFT Warning/Error waive项同步给DFT工程师
- **参考文档**: `Database/Docs/DFT/DFT_Waive_Policy.md`
- **验证方法**: 检查waive list和DFT沟通记录
- **验收标准**: 所有waive项已通知DFT并获确认
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 31. 🔴 DFT信号命名规则 [Critical]
- **描述**: Top级模块DFT信号命名规则: `ate_test_mode`/`pon_bist_mode`/`run_bist_mode`/`age_bist_mode`/`dft_50m_clk`/`scan_enable`；非Top级模块DFT信号命名: `test_mode`/`scan_enable`/`dft_50m_clk`
- **参考文档**: `Database/Docs/DFT/DFT_Naming_Convention.md`
- **验证方法**: 检查RTL代码命名
- **验收标准**: 所有DFT信号命名符合规范
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 32. 🔴 下降沿时钟DFT处理 [Critical]
- **描述**: 下降沿有效的时钟，不需要DFT处理（tessent工具自动处理）
- **参考文档**: `Database/Docs/DFT/DFT_Clock_Handling.md`
- **验证方法**: 检查时序约束和DFT设置
- **验收标准**: 下降沿时钟未手动插入DFT逻辑
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 33. 🟡 门控时钟TE/SE连接 [Major]
- **描述**: SDC中Generated clock前的门控时钟，TE/SE pin连接test_mode；Generated clock后的门控时钟、手动例化的门控时钟，TE/SE pin tie 0
- **参考文档**: `Database/Docs/DFT/Clock_Gating_DFT.md`
- **验证方法**: 检查RTL代码和SDC
- **验收标准**: 门控时钟TE/SE连接正确
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 34. 🟡 时钟分频DFT切换 [Major]
- **描述**: 时钟分频值，使用test_mode切换成最小分频，功能下最快频率；时钟切换控制，使用test_mode切换成功能下最高频率时钟
- **参考文档**: `Database/Docs/DFT/Clock_Divider_DFT.md`
- **验证方法**: 检查RTL代码
- **验收标准**: 分频和切换逻辑有DFT控制
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 35. 🟡 PAD输入时钟DFT切换 [Major]
- **描述**: PAD输入时钟，在DFT模式需要切换为dft_50m_clk或功能模式相同频率的时钟
- **参考文档**: `Database/Docs/DFT/PAD_Clock_DFT.md`
- **验证方法**: 检查时钟切换逻辑
- **验收标准**: PAD时钟在DFT模式正确切换
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 36. 🟡 SerDes RX恢复时钟DFT切换 [Major]
- **描述**: SerDes RX恢复时钟，在DFT模式需要切换为SerDes TX固定时钟；无对应SerDes TX，切换为功能模式相同频率的时钟
- **参考文档**: `Database/Docs/DFT/SerDes_Clock_DFT.md`
- **验证方法**: 检查时钟切换逻辑
- **验收标准**: RX恢复时钟在DFT模式正确切换
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 37. 🟡 时钟作为数据DFT通知 [Major]
- **描述**: 作为数据使用的时钟，同步给DFT工程师
- **参考文档**: `Database/Docs/DFT/Clock_as_Data_DFT.md`
- **验证方法**: 检查DFT沟通记录
- **验收标准**: DFT工程师已收到通知并确认
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 38. 🟡 复位电平一致性 [Major]
- **描述**: 同一个模块，只能使用同一种复位电平，高有效或低有效，否则需同步给DFT工程师
- **参考文档**: `Database/Docs/DFT/Reset_Polarity_DFT.md`
- **验证方法**: 检查RTL代码
- **验收标准**: 复位电平一致或已通知DFT
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 39. 🟡 直接输入复位DFT处理 [Major]
- **描述**: 模块直接输入的复位（外部时钟复位模块已增加复位同步），不需要DFT处理
- **参考文档**: `Database/Docs/DFT/Reset_DFT_Handling.md`
- **验证方法**: 检查复位路径
- **验收标准**: 直接输入复位未重复插入DFT逻辑
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 40. 🟡 寄存器输出复位DFT处理 [Major]
- **描述**: 模块输入的复位后，增加了寄存器输出的复位，直接控制其他寄存器，不需要DFT处理
- **参考文档**: `Database/Docs/DFT/Reset_DFT_Handling.md`
- **验证方法**: 检查复位路径
- **验收标准**: 寄存器输出复位未重复插入DFT逻辑
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 41. 🟡 组合逻辑复位DFT切换 [Major]
- **描述**: 模块输入的复位后，增加了组合逻辑的复位，使用test_mode切换到输入复位
- **参考文档**: `Database/Docs/DFT/Reset_DFT_Handling.md`
- **验证方法**: 检查复位路径和DFT切换逻辑
- **验收标准**: 组合逻辑复位有DFT切换
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 42. 🟢 DFT信号完整性检查 [Minor]
- **描述**: 检查所有DFT信号完整连接，无悬空
- **参考文档**: `Database/Docs/DFT/DFT_Signal_Checklist.md`
- **验证方法**: 检查RTL连接
- **验收标准**: 所有DFT信号正确连接
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

---

## IDR 评审结论

| 级别 | 检查项 | 符合 | 不符合 | 不适用 | 符合率 | 要求 |
|------|--------|------|--------|--------|--------|------|
| 🔴 Critical | 15 | ___ | ___ | ___ | ___% | 必须 100% |
| 🟡 Major | 25 | ___ | ___ | ___ | ___% | ≥ 80% |
| 🟢 Minor | 2 | ___ | ___ | ___ | ___% | 无要求 |
| **总计** | **42** | ___ | ___ | ___ | ___% | - |

**通过标准检查**:
- [ ] 🔴 Critical (15项): 全部符合 ___ / 15
- [ ] 🟡 Major (25项): 符合率 ≥ 80% (至少20项) ___ / 25

**评审结论**: ☐ 通过 / ☐ 有条件通过 / ☐ 不通过

**条件通过的前提条件** (如选择有条件通过):
| 序号 | 待完成项 | 责任人 | 截止日期 |
|------|---------|--------|---------|
| 1 | | | |
| 2 | | | |
| 3 | | | |

---

## 签字确认

| 角色 | 签名 | 日期 |
|------|------|------|
| 数字设计负责人 | ___________ | ___________ |
| 验证负责人 | ___________ | ___________ |
| DFT负责人 | ___________ | ___________ |
| 项目经理 | ___________ | ___________ |
| AI Yang (Quality Gatekeeper) | ☐ | ___________ |
| 实体Yang (最终批准) | ☐ | ___________ |

---

## 附录

### IDR Review 9个Phase参考

| Phase | 交付物 | 负责人 | 检查内容 |
|------|--------|--------|---------|
| **Phase 1** | Reference manual改动项 | IP/Project | 文档改动项确认 |
| **Phase 2** | Reference manual example章节 | IP/Project | example中每一步是否独立、可以被中断？ |
| **Phase 3** | Codebeamer HWE2改动项 | IP/Project | 改动、新增的feature；SRAM/ROM、FIFO大小配置 |
| **Phase 4** | 面积、时序 | IP/Project | SRAM scan、Area、Timing、SDC/UPF/DC、OPT-1206/1207 |
| **Phase 5** | Spyglass | IP/Project | Async处理、Warning/Error检查、DFT Async_07/Clock_11 |
| **Phase 6** | PowerPro | IP/Project | 功耗仿真、clock ungated列表 |
| **Phase 7** | DFT | IP/Project | Testmode/Agingmode/BIST mask、时钟复位处理 |
| **Phase 8** | DFMEA + IO Skew + Code Review | IP/Project | 风险评估、IO时序、代码审查 |
| **Phase 9** | IDR Checklist | IP/Project | 模块级Checklist + Module Level Design Rule |

---

## 历史版本记录

| 版本 | 日期 | 变更说明 | 作者 |
|------|------|---------|------|
| v1.0 | | 首次创建 IDR Checklist | |

---

*此Checklist基于 workflow/SOC_DESIGN_WORKFLOW.md 定义*
*42项检查涵盖Common Design、Low Power、CDC、DFT四大类别*
