# GHDL Makefile

GHDL = {{GHDL_PATH}}
GTKWAVE = {{GTKWAVE_PATH}}
RTL_TOP = {{RTL_TOP}}
TB_TOP = {{TB_TOP}}
RTL_DIR = ../../DesignData/RTL
TB_DIR = ../../Verification/Env
WORK_DIR = work

# 使用系统默认路径
ifeq ($(GHDL),{{GHDL_PATH}})
    GHDL = ghdl
endif
ifeq ($(GTKWAVE),{{GTKWAVE_PATH}})
    GTKWAVE = gtkwave
endif

.PHONY: compile elaborate simulate waveform clean

compile:
	mkdir -p $(WORK_DIR)
	$(GHDL) --workdir=$(WORK_DIR) --remove 2>/dev/null || true
	$(GHDL) --workdir=$(WORK_DIR) -a $(RTL_DIR)/{{RTL_TOP}}.vhd
	$(GHDL) --workdir=$(WORK_DIR) -a $(TB_DIR)/{{TB_TOP}}.vhd

elaborate: compile
	$(GHDL) --workdir=$(WORK_DIR) -e $(TB_TOP)

simulate: elaborate
	$(GHDL) --workdir=$(WORK_DIR) -r $(TB_TOP) --wave=wave.ghw --vcd=dump.vcd

waveform:
	$(GTKWAVE) wave.ghw 2>/dev/null || $(GTKWAVE) dump.vcd

clean:
	rm -rf $(WORK_DIR) wave.ghw dump.vcd

all: compile elaborate simulate
