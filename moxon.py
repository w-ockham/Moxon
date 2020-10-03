#!/usr/bin/env python3
# coding: utf-8
import cgi
import cgitb
import math

def moxon(dw,wl):
    d1 = 0.4342945 * math.log(dw)
    if d1 < -6 :
        note = "Wire diameter too small, results uncertain"
    elif d1 > -2 :
        note = "Wire diameter too large, results uncertain"
    else:
        note = None

    a = -0.0008571428571*(d1 * d1) - 0.009571428571 * d1 + 0.3398571429
    b = -0.002142857143 *(d1 * d1) - 0.02035714286  * d1 + 0.008285714286
    c =  0.001809523381 *(d1 * d1) + 0.01780952381  * d1 + 0.05164285714
    d =  0.001 * d1 + 0.07178571429
    e =  b + c + d

    return {'a':round(a*wl,1),'b':round(b*wl,1),
            'c':round(c*wl,1),'d':round(d*wl,1),
            'e':round(e*wl,1),'note':note}

def showForm(mesg):
    res = '''Content-Type:text/html

<html>
<head>
<title> Moxon Calculator </title>
</head>
<body>
<h1> Moxon Calculator </h1>
<font color="red">''' + mesg + '''</font>
<form method="post" action='/cgi-bin/moxon.py'>
<table border="0">
 <tr>
    <td align="right">Frequency in MHz</td>
    <td><input name="freq" size="10" maxlength="10"></td>
 </tr>
 <tr>
    <td align="right">Wire Diameter in millimeters</td>
    <td><input name="diameter" size="10" maxlength="10"></td>
 </tr>
 </table>
 <button type="submit">Calculate</button>
</form>
</body>
</html>
'''.strip()

    print(res)
    
def showResult(freq,d,res):
    res = '''Content-Type:text/html

<html>
<head>
<title> Moxon Calculator </title>
</head>
<body>
<h1> Moxon Calculator </h1>
<table border="1">
 <tr>
    <th align="right">Frequency(MHz)</th>
    <td>''' + str(freq) + '''</td>
 </tr>
 <tr>
    <th align="right">Diameter(mm)</th>
    <td>''' + str(d) + '''</td>
 </tr>
 <tr>
    <th align="right">A(mm)</th>
    <td>''' + str(res['a']) + '''</td>
 </tr>
 <tr>
    <th align="right">B(mm)</th>
    <td>''' + str(res['b']) + '''</td>
 </tr>
 <tr>
    <th align="right">C(mm)</th>
    <td>''' + str(res['c']) + '''</td>
 </tr>
 <tr>
    <th align="right">D(mm)</th>
    <td>''' + str(res['d']) + '''</td>
 </tr>
 <tr>
    <th align="right">E(mm)</td>
    <td>''' + str(res['e']) + '''</td>
 </tr>
 </table>
 <img src="/img/moxgen-1.gif"/>
</body>
</html>
'''.strip()

    print(res)
    
def main():

    form = cgi.FieldStorage()
    
    f = form.getvalue('freq',None)
    d = form.getvalue('diameter',None)

    if f:
        try:
            frequency = float(f)
            wd = float(d)
            wl = 299792.5 / frequency
            dw = wd / wl
            showResult(frequency,d,moxon(dw,wl))
        except:
            showForm('Invalid Parameter.<br>Input Frequency and Wire Diameter.')
    else:
        showForm('Input Frequency and Wire Diameter.')

if __name__ == '__main__':
    main()

