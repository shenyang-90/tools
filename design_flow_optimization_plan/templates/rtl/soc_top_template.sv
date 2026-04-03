//==============================================================================
// Module: soc_top
// Description: SoC Top Level Module
// Company: [Company Name]
// Author: [Author Name]
// Email: [Email]
//==============================================================================
// Version History:
//   v0.1.0 - 2026-04-03 - Initial version
//            - Created top-level SoC integration
//   v0.2.0 - 2026-04-10 - Added safety monitor interface
//            - Integrated safety_monitor module
//            - Added fault injection ports
//   v0.3.0 - 2026-04-15 - Fixed clock domain crossing issue
//            - Added synchronizer for async reset
//            - Updated clock gating scheme
//==============================================================================

`ifndef SOC_TOP_SV
`define SOC_TOP_SV

module soc_top #(
    parameter ADDR_WIDTH = 32,
    parameter DATA_WIDTH = 32,
    parameter NUM_IRQ    = 32
)(
    // Clock & Reset
    input  wire clk_sys,
    input  wire clk_peri,
    input  wire rst_n,
    
    // Debug Interface
    input  wire jtag_tck,
    input  wire jtag_tms,
    input  wire jtag_tdi,
    output wire jtag_tdo,
    
    // UART Interface
    input  wire uart_rx,
    output wire uart_tx,
    
    // SPI Interface
    output wire spi_sck,
    output wire spi_csn,
    output wire spi_mosi,
    input  wire spi_miso,
    
    // I2C Interface
    inout  wire i2c_scl,
    inout  wire i2c_sda,
    
    // GPIO
    input  wire [15:0] gpio_in,
    output wire [15:0] gpio_out,
    output wire [15:0] gpio_oe,
    
    // Interrupt
    input  wire [NUM_IRQ-1:0] irq_ext,
    
    // Safety Signals
    input  wire safety_error_in,
    output wire safety_error_out,
    output wire safety_reset_req
);

    //==========================================================================
    // Internal Signals
    //==========================================================================
    wire [ADDR_WIDTH-1:0] cpu_addr;
    wire [DATA_WIDTH-1:0] cpu_wdata;
    wire [DATA_WIDTH-1:0] cpu_rdata;
    wire                  cpu_we;
    wire [3:0]            cpu_be;
    wire                  cpu_req;
    wire                  cpu_ack;
    
    wire [31:0]           irq_combined;
    wire                  irq_pending;
    
    // Clock/Reset Distribution
    wire clk_core;
    wire clk_bus;
    wire rst_n_sync;
    
    //==========================================================================
    // Clock & Reset Controller
    //==========================================================================
    clk_rst_ctrl u_clk_rst (
        .clk_sys     (clk_sys),
        .clk_peri    (clk_peri),
        .rst_n       (rst_n),
        .clk_core    (clk_core),
        .clk_bus     (clk_bus),
        .rst_n_sync  (rst_n_sync)
    );
    
    //==========================================================================
    // CPU Core (Placeholder)
    //==========================================================================
    // [TODO: Integrate actual CPU core]
    // For now, using a simple placeholder
    
    //==========================================================================
    // Bus Matrix
    //==========================================================================
    bus_matrix u_bus_matrix (
        .clk         (clk_bus),
        .rst_n       (rst_n_sync),
        // CPU interface
        .m_addr      (cpu_addr),
        .m_wdata     (cpu_wdata),
        .m_rdata     (cpu_rdata),
        .m_we        (cpu_we),
        .m_be        (cpu_be),
        .m_req       (cpu_req),
        .m_ack       (cpu_ack),
        // Peripheral interfaces...
    );
    
    //==========================================================================
    // UART Controller
    //==========================================================================
    uart_top u_uart (
        .clk         (clk_peri),
        .rst_n       (rst_n_sync),
        .rx          (uart_rx),
        .tx          (uart_tx),
        // Bus interface...
    );
    
    //==========================================================================
    // SPI Controller
    //==========================================================================
    spi_top u_spi (
        .clk         (clk_peri),
        .rst_n       (rst_n_sync),
        .sck         (spi_sck),
        .csn         (spi_csn),
        .mosi        (spi_mosi),
        .miso        (spi_miso),
        // Bus interface...
    );
    
    //==========================================================================
    // Safety Monitor
    //==========================================================================
    safety_monitor u_safety (
        .clk         (clk_core),
        .rst_n       (rst_n_sync),
        .error_in    (safety_error_in),
        .error_out   (safety_error_out),
        .reset_req   (safety_reset_req),
        // Internal monitoring signals...
    );
    
    //==========================================================================
    // Interrupt Controller
    //==========================================================================
    assign irq_combined = {irq_ext, 16'h0000};  // [TODO: Define IRQ mapping]
    
    //==========================================================================
    // IO Mux
    //==========================================================================
    io_mux u_iomux (
        .clk         (clk_peri),
        .rst_n       (rst_n_sync),
        .gpio_in     (gpio_in),
        .gpio_out    (gpio_out),
        .gpio_oe     (gpio_oe),
        // Alternative function selection...
    );

endmodule : soc_top

`endif // SOC_TOP_SV
