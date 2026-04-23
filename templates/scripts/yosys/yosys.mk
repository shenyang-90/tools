# Scripts/synth/yosys.mk - Yosys综合模板

OUT_DIR         ?= ../../Temp/Yosys
RTL_DIR         ?= ../design/RTL
TOP             ?= $(RTL_TOP)

.PHONY: synth synth_opt clean

synth:
	@mkdir -p $(OUT_DIR)
	@echo "[Yosys] Synthesizing $(TOP)..."
	$(YOSYS) -p "
		read_verilog $(RTL_DIR)/*.v;
		synth -top $(TOP);
		dfflibmap -liberty $(STD_CELL_LIB);
		abc -liberty $(STD_CELL_LIB);
		clean;
		write_verilog $(OUT_DIR)/$(TOP)_synth.v;
		write_sdc $(OUT_DIR)/$(TOP).sdc;
	" 2>&1 | tee $(OUT_DIR)/yosys.log
	@echo "[Yosys] Synthesis complete"

synth_opt: synth
	@echo "[Yosys] Optimizing..."
	$(YOSYS) -p "
		read_verilog $(OUT_DIR)/$(TOP)_synth.v;
		read_liberty $(STD_CELL_LIB);
		opt;
		techmap;
		opt;
		write_verilog $(OUT_DIR)/$(TOP)_opt.v;
	" 2>&1 | tee $(OUT_DIR)/yosys_opt.log
	@echo "[Yosys] Optimization complete"

clean:
	@rm -rf $(OUT_DIR)
	@echo "[Yosys] Cleaned"
