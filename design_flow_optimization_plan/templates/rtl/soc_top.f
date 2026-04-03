# soc_top.f - SoC Top Level Filelist
# Generated: 2026-04-03
# Project: [Project Name]

#==============================================================================
# Common RTL
#==============================================================================
+incdir+../rtl/common
../rtl/common/clk_rst_ctrl.sv
../rtl/common/bus_matrix.sv
../rtl/common/safety_monitor.sv
../rtl/common/io_mux.sv

#==============================================================================
# SoC Subsystem
#==============================================================================
+incdir+../rtl/soc/top
../rtl/soc/top/soc_top.sv

# CPU Core (external)
# - Replace with actual CPU RTL
# ../rtl/cpu/cpu_core.sv

#==============================================================================
# IP Blocks
#==============================================================================
# UART
-f ../rtl/ip/uart/uart.f

# SPI
-f ../rtl/ip/spi/spi.f

# I2C
-f ../rtl/ip/i2c/i2c.f

# [Add more IP filelists as needed]
