//==============================================================================
// Module: uart_top
// Description: UART Top Level Module - Full-featured UART controller
// Company: [Company Name]
// Author: [Author Name]
// Email: [Email]
//==============================================================================
// Version History:
//   v0.1.0 - 2026-04-03 - Initial version
//            - Basic TX/RX functionality
//            - Configurable baud rate
//   v0.2.0 - 2026-04-15 - Added FIFO support
//            - 16-byte TX/RX FIFO
//            - FIFO threshold interrupts
//   v0.3.0 - 2026-04-28 - Added DMA interface
//            - Burst transfer support
//            - Fixed framing error handling
//==============================================================================

`ifndef UART_TOP_SV
`define UART_TOP_SV

module uart_top #(
    parameter DATA_WIDTH = 8,
    parameter FIFO_DEPTH = 16,
    parameter ADDR_WIDTH = 8
)(
    // System Interface
    input  wire                  clk,
    input  wire                  rst_n,
    
    // APB Bus Interface
    input  wire [ADDR_WIDTH-1:0] paddr,
    input  wire                  pwrite,
    input  wire                  psel,
    input  wire                  penable,
    input  wire [31:0]           pwdata,
    output wire [31:0]           prdata,
    output wire                  pready,
    output wire                  pslverr,
    
    // UART Interface
    input  wire                  rx,
    output wire                  tx,
    
    // Interrupts
    output wire                  irq_tx,
    output wire                  irq_rx,
    output wire                  irq_err,
    
    // DMA Interface (optional)
    output wire                  dma_tx_req,
    output wire                  dma_rx_req,
    input  wire                  dma_tx_ack,
    input  wire                  dma_rx_ack
);

    //==========================================================================
    // Internal Signals
    //==========================================================================
    wire [DATA_WIDTH-1:0] tx_fifo_wdata;
    wire [DATA_WIDTH-1:0] tx_fifo_rdata;
    wire                  tx_fifo_wr;
    wire                  tx_fifo_rd;
    wire                  tx_fifo_full;
    wire                  tx_fifo_empty;
    wire [$clog2(FIFO_DEPTH):0] tx_fifo_count;
    
    wire [DATA_WIDTH-1:0] rx_fifo_wdata;
    wire [DATA_WIDTH-1:0] rx_fifo_rdata;
    wire                  rx_fifo_wr;
    wire                  rx_fifo_rd;
    wire                  rx_fifo_full;
    wire                  rx_fifo_empty;
    wire [$clog2(FIFO_DEPTH):0] rx_fifo_count;
    
    wire [15:0]           baud_div;
    wire [1:0]            data_bits;
    wire                  stop_bits;
    wire                  parity_en;
    wire                  parity_odd;
    wire                  tx_en;
    wire                  rx_en;
    
    wire                  tx_busy;
    wire                  rx_busy;
    wire                  rx_framing_err;
    wire                  rx_parity_err;
    wire                  rx_overrun_err;
    
    //==========================================================================
    // Register Block
    //==========================================================================
    uart_regs u_regs (
        .clk             (clk),
        .rst_n           (rst_n),
        // APB interface
        .paddr           (paddr),
        .pwrite          (pwrite),
        .psel            (psel),
        .penable         (penable),
        .pwdata          (pwdata),
        .prdata          (prdata),
        .pready          (pready),
        .pslverr         (pslverr),
        // Control outputs
        .baud_div        (baud_div),
        .data_bits       (data_bits),
        .stop_bits       (stop_bits),
        .parity_en       (parity_en),
        .parity_odd      (parity_odd),
        .tx_en           (tx_en),
        .rx_en           (rx_en),
        // Status inputs
        .tx_fifo_count   (tx_fifo_count),
        .rx_fifo_count   (rx_fifo_count),
        .tx_fifo_full    (tx_fifo_full),
        .rx_fifo_full    (rx_fifo_full),
        .tx_fifo_empty   (tx_fifo_empty),
        .rx_fifo_empty   (rx_fifo_empty),
        .tx_busy         (tx_busy),
        .rx_busy         (rx_busy),
        .framing_err     (rx_framing_err),
        .parity_err      (rx_parity_err),
        .overrun_err     (rx_overrun_err),
        // FIFO interface
        .tx_fifo_wr      (tx_fifo_wr),
        .tx_fifo_wdata   (tx_fifo_wdata),
        .rx_fifo_rd      (rx_fifo_rd),
        .rx_fifo_rdata   (rx_fifo_rdata)
    );
    
    //==========================================================================
    // TX FIFO
    //==========================================================================
    uart_fifo #(
        .DEPTH           (FIFO_DEPTH),
        .WIDTH           (DATA_WIDTH)
    ) u_tx_fifo (
        .clk             (clk),
        .rst_n           (rst_n),
        .wr_en           (tx_fifo_wr),
        .wr_data         (tx_fifo_wdata),
        .rd_en           (tx_fifo_rd),
        .rd_data         (tx_fifo_rdata),
        .full            (tx_fifo_full),
        .empty           (tx_fifo_empty),
        .count           (tx_fifo_count)
    );
    
    //==========================================================================
    // RX FIFO
    //==========================================================================
    uart_fifo #(
        .DEPTH           (FIFO_DEPTH),
        .WIDTH           (DATA_WIDTH)
    ) u_rx_fifo (
        .clk             (clk),
        .rst_n           (rst_n),
        .wr_en           (rx_fifo_wr),
        .wr_data         (rx_fifo_wdata),
        .rd_en           (rx_fifo_rd),
        .rd_data         (rx_fifo_rdata),
        .full            (rx_fifo_full),
        .empty           (rx_fifo_empty),
        .count           (rx_fifo_count)
    );
    
    //==========================================================================
    // UART Transmitter
    //==========================================================================
    uart_tx u_tx (
        .clk             (clk),
        .rst_n           (rst_n),
        .en              (tx_en),
        .baud_div        (baud_div),
        .data_bits       (data_bits),
        .stop_bits       (stop_bits),
        .parity_en       (parity_en),
        .parity_odd      (parity_odd),
        .tx_data         (tx_fifo_rdata),
        .tx_start        (!tx_fifo_empty && tx_en),
        .tx_done         (tx_fifo_rd),
        .tx              (tx),
        .busy            (tx_busy)
    );
    
    //==========================================================================
    // UART Receiver
    //==========================================================================
    uart_rx u_rx (
        .clk             (clk),
        .rst_n           (rst_n),
        .en              (rx_en),
        .baud_div        (baud_div),
        .data_bits       (data_bits),
        .stop_bits       (stop_bits),
        .parity_en       (parity_en),
        .parity_odd      (parity_odd),
        .rx              (rx),
        .rx_data         (rx_fifo_wdata),
        .rx_valid        (rx_fifo_wr),
        .busy            (rx_busy),
        .framing_err     (rx_framing_err),
        .parity_err      (rx_parity_err),
        .overrun_err     (rx_overrun_err)
    );
    
    //==========================================================================
    // Interrupt Generation
    //==========================================================================
    assign irq_tx = tx_fifo_empty || (tx_fifo_count < 4);  // TX FIFO below threshold
    assign irq_rx = !rx_fifo_empty || (rx_fifo_count > 12); // RX FIFO above threshold
    assign irq_err = rx_framing_err || rx_parity_err || rx_overrun_err;
    
    //==========================================================================
    // DMA Interface
    //==========================================================================
    assign dma_tx_req = tx_fifo_count < 8;   // Request more data when TX FIFO has space
    assign dma_rx_req = rx_fifo_count > 8;   // Request read when RX FIFO has data

endmodule : uart_top

`endif // UART_TOP_SV
