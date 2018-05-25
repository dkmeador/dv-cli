
{## Set some useful default variables ##}

{%- macro comment_bar(level="h1") %}
{%- if level == "h1" %}
  {{- "//" ~ '*'*70 }}
{%- elif level == "h2" %}
  {{- "//" ~ '/'*70 }}
{%- elif level == "h3" %}
  {{- "//" ~ '-'*70 }}
{%- elif level == "h4" %}
  {{- "//" ~ '+'*70 }}
{%- else %}
  {{- "//" ~ '*'*70 }}
{%- endif %}
{%- endmacro %}

{%- macro comment_bar(pre='//', mid='/'*70, post='') %}
  {{- pre ~ mid ~ post }}
{%- endmacro %}

{## Format a string as comments ##}
{%- macro string2comments(str, wid=80, wrap="//",ind=4) %}
{{ wrap|indent(ind,true) }} {{ str|wordwrap(width=wid, break_long_words=True, wrapstring=('\n'+wrap))|indent(ind) }}
{%- endmacro %}

{## Macro to define reference to a uvm object or component ##}
{%- macro object_ref(item) %}
    // Reference: {{ item.name }}
    //
   {#- Added Docs for child instance -#}
   {%- for str in item.docs %}
     {{- string2comments(str) }}
   {%- endfor %}
   {%  set parent = ',this' if item.is_comp else '' %}
    {{ item.type }} {{ item.name }};
 {%- endmacro %}



{## Macro to instance to a uvm object or component ##}
{%- macro object_inst(item) %}
    // Instance: {{ item.name }}
  {{- ("\nif (" + item.enable + ")") | indent(4,true) if item.enable }}
    {%- set parent = ',this' if item.is_comp else '' %}
      {{ item.name }} = {{ item.type }}::type_id::create($sformat("{{ item.name }}"{{ parent }}));
{%- endmacro %}
