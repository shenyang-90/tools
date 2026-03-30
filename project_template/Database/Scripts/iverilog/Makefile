# Icarus Verilog Makefile

IVERILOG = {{IVERILOG_PATH}}
VVP = {{VVP_PATH}}
GTKWAVE = {{GTKWAVE_PATH}}

# 使用系统默认路径
ifeq ($(IVERILOG),{{IVERILOG_PATH}})
    IVERILOG = iverilog
endif
ifeq ($(VVP),{{VVP_PATH}})
    VVP = vvp
endif
ifeq ($(GTKWAVE),{{GTKWAVE_PATH}})
    GTKWAVE = gtkwave
endif

RTL_TOP = {{RTL_TOP}}
TB_TOP = {{TB_TOP}}
RTL_DIR = ../../DesignData/RTL
TB_DIR = ../../Verification/Env

.PHONY: compile simulate waveform clean

compile:
	$(IVERILOG) -g2012 -o sim.out \
		-y $(RTL_DIR) \
		-I $(RTL_DIR) \
		$(TB_DIR)/$(TB_TOP).sv \
		$(RTL_DIR)/$(RTL_TOP).v

simulate: compile
	$(VVP) -n sim.out -lxt2

waveform:
	$(GTKWAVE) dump.vcd &

clean:
	rm -f sim.out dump.vcd

all: compile simulate
