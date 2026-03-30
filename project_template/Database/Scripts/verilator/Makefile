# Verilator Makefile

VERILATOR = {{VERILATOR_PATH}}
RTL_TOP = {{RTL_TOP}}
TB_TOP = {{TB_TOP}}
RTL_DIR = ../../DesignData/RTL
TB_DIR = ../../Verification/Env

# 使用系统默认路径
ifeq ($(VERILATOR),{{VERILATOR_PATH}})
    VERILATOR = verilator
endif

.PHONY: lint compile simulate clean

lint:
	$(VERILATOR) --lint-only -Wall \
		-y $(RTL_DIR) \
		$(RTL_DIR)/$(RTL_TOP).v

compile:
	$(VERILATOR) --cc --exe --build --trace \
		-y $(RTL_DIR) \
		-I $(RTL_DIR) \
		-Mdir obj_dir \
		--top-module $(RTL_TOP) \
		$(RTL_DIR)/$(RTL_TOP).v \
		$(TB_DIR)/$(TB_TOP).cpp

simulate: compile
	./obj_dir/V$(RTL_TOP)

clean:
	rm -rf obj_dir trace.vcd

all: lint compile simulate
