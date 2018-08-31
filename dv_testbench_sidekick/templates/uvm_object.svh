{% import 'macros.svh' as macro %}

{%- block header %}
{% endblock %}

{{ macro.comment_bar(mid='*') }}
// Class: {{ class_name }}
{%- if class_docstring %} {{class_docstring}} {% endif %}
{{ macro.comment_bar(mid='*') }}


class {{ class_name }} {% if  parent_class_name %}extends {{parent_class_name}}{% endif %};

{%- block    factory_registration %}
{{ macro.comment_bar(text=" factory registration ", mid='*') }}
    `uvm_object_utils({{ class_name }})
{% endblock factory_registration %}

{%- block    state_variable_decl %}
{{ macro.comment_bar(text=" State Variables and objects ", mid='*') }}
{% endblock state_variable_decl %}

{%- block    rand_variable_decl %}
   {{ macro.comment_bar(text=" Random Variables ", mid='*') }}
{% endblock rand_variable_decl %}

{{ macro.comment_bar(text=" Components ", mid='*') }}
{%- for comp in child_comps %}
{{ macro.object_ref(comp) }}
{%- endfor %}

{{ macro.comment_bar(text=" Objects ", mid='*') }}
{%- for comp in child_objects %}
{{ macro.object_ref(comp) }}
{%- endfor %}

{%- block constructor %}
    // ************************************************************************
    // Constructor: new
    //
    // Creates and initializes an instance of this class
    //
    // Arguments:
    //
    //    name   - name of the instance
    //
    // ************************************************************************
    function new(string name);
        super.new(name);
    endfunction
{% endblock constructor %}


{%- block build %}
   // function: build
   //
   // Build all child objects
   virtual function void build();
      // Build Objects
{%-   for item in child_objects %}
{{ macro.object_inst(comp) }}
{%-   endfor %}

   endfunction : build_phase
{%- endblock build %}

{%- block functions %}{% endblock functions %}

{%- block tasks %}{% endblock tasks %}

endclass


{%- block footer %}
{% endblock %}
