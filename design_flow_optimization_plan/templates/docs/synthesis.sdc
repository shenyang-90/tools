#===============================================================================
# synthesis.sdc - Synthesis Constraints
# Project: [Project Name]
# Module: Top Level
# Version: v0.1.0
# Date: 2026-04-03
#===============================================================================

#===============================================================================
# Clock Definitions
#===============================================================================

# System Clock (100 MHz)
create_clock -name clk_sys -period 10.0 [get_ports clk_sys]
set_clock_uncertainty -setup 0.2 [get_clocks clk_sys]
set_clock_uncertainty -hold 0.1 [get_clocks clk_sys]
set_clock_transition 0.1 [get_clocks clk_sys]

# Peripheral Clock (50 MHz)
create_clock -name clk_peri -period 20.0 [get_ports clk_peri]
set_clock_uncertainty -setup 0.2 [get_clocks clk_peri]
set_clock_uncertainty -hold 0.1 [get_clocks clk_peri]
set_clock_transition 0.1 [get_clocks clk_peri]

# Core Clock (200 MHz)
create_clock -name clk_core -period 5.0 [get_ports clk_core]
set_clock_uncertainty -setup 0.15 [get_clocks clk_core]
set_clock_uncertainty -hold 0.08 [get_clocks clk_core]
set_clock_transition 0.08 [get_clocks clk_core]

# JTAG Clock (10 MHz, asynchronous)
create_clock -name jtag_tck -period 100.0 [get_ports jtag_tck]
set_clock_groups -asynchronous -group [get_clocks jtag_tck]

#===============================================================================
# Clock Relationships
#===============================================================================

# Declare clock groups
set_clock_groups -asynchronous \
    -group [get_clocks clk_sys] \
    -group [get_clocks clk_peri] \
    -group [get_clocks jtag_tck]

# Clock domain crossing paths
set_false_path -from [get_clocks clk_sys] -to [get_clocks jtag_tck]
set_false_path -from [get_clocks jtag_tck] -to [get_clocks clk_sys]

#===============================================================================
# Input/Output Delays
#===============================================================================

# System inputs
set_input_delay -clock clk_sys -max 2.0 [get_ports rst_n]
set_input_delay -clock clk_sys -min 0.0 [get_ports rst_n]

# UART interface
set_input_delay -clock clk_peri -max 3.0 [get_ports uart_rx]
set_input_delay -clock clk_peri -min 0.0 [get_ports uart_rx]
set_output_delay -clock clk_peri -max 3.0 [get_ports uart_tx]
set_output_delay -clock clk_peri -min 0.0 [get_ports uart_tx]

# SPI interface
set_output_delay -clock clk_peri -max 2.0 [get_ports spi_*]
set_output_delay -clock clk_peri -min 0.0 [get_ports spi_*]
set_input_delay -clock clk_peri -max 4.0 [get_ports spi_miso]
set_input_delay -clock clk_peri -min 0.0 [get_ports spi_miso]

# GPIO
set_input_delay -clock clk_peri -max 3.0 [get_ports gpio_in[*]]
set_output_delay -clock clk_peri -max 3.0 [get_ports gpio_out[*]]

#===============================================================================
# Timing Exceptions
#===============================================================================

# Reset paths
set_false_path -from [get_ports rst_n]
set_false_path -to [get_ports rst_n]

# Static configuration registers
set_false_path -to [get_registers *config_reg*]

# Test mode signals
set_false_path -from [get_ports test_mode]

#===============================================================================
# Design Constraints
#===============================================================================

# Maximum transition time
set_max_transition 0.3 [current_design]

# Maximum fanout
set_max_fanout 20 [current_design]

# Maximum capacitance
set_max_capacitance 0.5 [all_outputs]

#===============================================================================
# Area Constraints
#===============================================================================

# Maximum area (optional)
# set_max_area 100000

#===============================================================================
# Power Constraints
#===============================================================================

# Clock gating
set_clock_gating_style -minimum_bitwidth 4 \
    -positive_edge_logic { integrated } \
    -control_point before

# Multibit banking
set_multibit_mapping -mode non_timing_driven

#===============================================================================
# DFT Constraints
#===============================================================================

# Scan configuration
set_dft_configuration -scan enable
set_scan_configuration -chain_count 8

# Test clock
#create_clock -name scan_clk -period 50.0 [get_ports scan_clk]

# Scan inputs/outputs
#set_scan_signal test_si [get_ports scan_si]
#set_scan_signal test_so [get_ports scan_so]
#set_scan_signal test_se [get_ports scan_en]

#===============================================================================
# DRV Constraints (Design Rule Violations)
#===============================================================================

# Max transition
set_max_transition 0.4 [all_outputs]

# Max fanout
set_max_fanout 30 [all_outputs]

#===============================================================================
# Case Analysis (Modes)
#===============================================================================

# Functional mode (default)
# set_case_analysis 0 [get_ports test_mode]

# Test mode
# set_case_analysis 1 [get_ports test_mode]

#===============================================================================
# End of File
#===============================================================================
