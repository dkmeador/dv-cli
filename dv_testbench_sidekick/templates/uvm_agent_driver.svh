{%- import "macros.svh" as macro -%}
{## Set some useful default variables ##}
{{ macro.comment_bar(mid='*'*70) }}
//
// Class: {{ name }}
//
// Purpose:
//
//  Drive interface pins based on a uvm_sequence_item
//
{{ macro.comment_bar(mid='*'*70) }}

class {{name}} extends uvm_driver #({{sequence_item}});

    `uvm_component_utils ({{name}})

    function new (string name = "{{name}}", uvm_component parent);
        super.new (name,parent);
     endfunction

    task run_phase (uvm_phase);
        super.run_phase (phase);
        forever begin
            `uvm_info (get_name(), $sformatf("Waiting for data from sequencer"), UVM_HIGH);
            seq_item_port.get_next_item (req);
            drive_item (req);
            seq_item_port.item_done();
         end
     endtask

     virtual task drive_item (my_data data_obj);
        // Drive the interface
        `uvm_info (get_name(), $sformatf("Sending %s",data_obj.convert2string()), UVM_HIGH);
     endtask

endclass
