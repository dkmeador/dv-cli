{%- import "macros.svh" as macro -%}
{## Set some useful default variables ##}
{{ macro.comment_bar(mid='*'*70) }}
//
// Class: {{ name }}
//
// Purpose:
//
//  The stated purpose of this test is ...
//
// Targeted Features:
//
//  - Feature 1
//  - Feature 2
//
// Test Procedure:
//
//  Step 1 - Bring device out of reset
//  Step 2 - Configure device
//
{{ macro.comment_bar(mid='*'*70) }}

class {{ name }} extends {{ parent_class or 'uvm_test' }};

    `uvm_component_utils({{ name }})

    {{ macro.comment_bar(mid='/'*70) }}
    // Function: new
    {{ macro.comment_bar(mid='/'*70) }}
    function new(string name="{{ name }}" , uvm_component parent = null);
        super.new(name,parent)
    endfunction


    {{ macro.comment_bar(mid='/'*70) }}
    // Task : run_phase
    //
    //  The uvm run_phase. Start the test procedure here.
    {{ macro.comment_bar(mid='/'*70) }}
    task run_phase(uvm_phase phase);
        super.run_phase(phase);
        phase.raise_objection(this, "Running {{ name }}");

        `uvm_error(get_name(), "TODO: This test has not been written yet");

        phase.drop_objection(this, "Finished {{ name }}");

    endtask : run_phase


endclass : {{ name }}