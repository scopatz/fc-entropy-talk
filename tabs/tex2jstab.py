#! /usr/bin/env python 

"""Don't forget to include the following style somewhere!

<style type="text/css">
table.tftable {color:#333333;width:80%;border-width: 1px;border-color: #a9a9a9;border-collapse: collapse;text-align:center; margin: auto;}
table.tftable th {background-color:#b8b8b8;border-width: 1px;padding: 4px;border-style: solid;border-color: #a9a9a9;text-align:left;}
table.tftable tr {background-color:#ffffff;text-align:center;}
table.tftable td {border-width: 1px;padding: 4px;border-style: solid;border-color: #a9a9a9;text-align:center;}
</style>
"""
import re
import sys
from hashlib import md5

#align_r = re.compile('\\begin{tabular}{(.*?)}', re.DOTALL)
align_r = re.compile('\\\\begin{tabular}{(.*?)}', re.DOTALL)
body_r = re.compile('\\\\begin{tabular}{.*?}(.*?)\\\\end{tabular}', re.DOTALL)
bold_r = re.compile('\\\\textbf{(.*)}', re.DOTALL)
nuc_r = re.compile('\\\\nuc{([A-Za-z]*?)}{([0-9]*?)}')
supernum_r = re.compile('\\\\superscript{([eE\-+0-9\.]*?)}')


def texparse(tex):
    tab = {}
    tab['id'] = 'tab' + md5(tex).hexdigest()
    tab['colalign'] = list(align_r.search(tex).group(1).replace('|', ''))
    body = body_r.search(tex).group(1)
    body = body.replace('\\hline', '').replace("\\&", "__and__")
    body = body.replace('\\%', '%')
    rows = [[d.strip().replace('__and__', '&') for d in r.split('&')] \
                        for r in body.split('\\\\') if 0 < len(r.strip())]
    # strip or replace \textbf and \nuc{}{}
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            m = supernum_r.search(rows[i][j])
            while m is not None:
                old = m.group(0)
                new = "$^{{{0}}}$".format(m.group(1))
                rows[i][j] = rows[i][j].replace(old, new)
                m = supernum_r.search(rows[i][j])

            m = nuc_r.search(rows[i][j])
            while m is not None:
                old = m.group(0)
                new = "$^{{{1}}}${0}".format(m.group(1), m.group(2))
                rows[i][j] = rows[i][j].replace(old, new)
                m = nuc_r.search(rows[i][j])

            m = bold_r.search(rows[i][j])
            if m is not None:
                if i == 0:
                    rows[i][j] = m.group(1)
                else:
                    rows[i][j] = '<b>' + m.group(1) + '</b>'
    tab['rows'] = rows
    return tab

jstemplate = """<script type="text/javascript">
    window.onload=function(){{
    var tfrow = document.getElementById('{id}').rows.length;
    var tbRow=[];
    for (var i=1;i<tfrow;i++) {{
        tbRow[i]=document.getElementById('{id}').rows[i];
        tbRow[i].onmouseover = function(){{
          this.style.backgroundColor = '#f3f8aa';
        }};
        tbRow[i].onmouseout = function() {{
          this.style.backgroundColor = '#ffffff';
        }};
    }}
}};
</script>

<table id="{id}" class="tftable" border="1">
{headers}
{rows}
</table>"""

def jstab(tab):
    hrow = tab['rows'][0]
    body = tab['rows'][1:]
    align = tab['colalign']
    headers = "<tr><th>"
    headers += "</th><th>".join(hrow)
    headers += "</th></tr>"
    rows = []
    for brow in body:
        assert len(brow) == len(align)
        r = "<tr>"
        for a, d in zip(align, brow):
            if a == 'l':
                r += '<td style="text-align:left;">' + d + '</td>'
            elif a == 'r':
                r += '<td style="text-align:right;">' + d + '</td>'
            else:
                r += '<td>' + d + '</td>'
        r += "</tr>"
        rows.append(r)
    rows = '\n'.join(rows)
    js = jstemplate.format(id=tab['id'], headers=headers, rows=rows)
    return js

def main():
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        texraw = f.read()
    tab = texparse(texraw)
    js = jstab(tab)
    print js

if __name__ == '__main__':
    main()
