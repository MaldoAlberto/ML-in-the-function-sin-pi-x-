from ROOT import TCanvas, gROOT, TGraph, TFile, gStyle, TLegend, TGraphErrors
import pandas as pd
import array as arr
import math 
import time
import numpy as np
from statistics import variance, mean 
fields = ['x', 'y']


df = pd.read_csv('uno.csv', skipinitialspace=True, usecols=fields)
derecha = df['x'].tolist()
izquierda = df['y'].tolist()


N = 1000
i = 0
x, y = arr.array( 'd' ), arr.array( 'd' )
while i < N:
	x.append(i*.002 -1)
	y.append(math.sin(x[i]*math.pi))
        i+=1

c1 = TCanvas('c1','c1', 900, 600 )

gr = TGraph(N,x,y)
gr.SetLineColor( 4 )
gr.SetTitle( 'H1 = ax+b' )
gr.GetXaxis().SetTitle( 'x' )
gr.GetYaxis().SetTitle( 'sin(pi*x)' )
gr.Draw( 'AC' )
gr.SetMinimum(-2.5)
gr.SetMaximum(2.5)


varianza = arr.array( 'd' )
j = 0

#promediox0,promediox1 = 0,0
m1,b1 = list(), list()
bias = 0.0
while j < N:
	c1.Update()
	var = 0
	x1 = float(derecha[j])
	x2 = float(izquierda[j])
	y1 = math.sin(x1*math.pi)
	y2 = math.sin(x2*math.pi)
	m1.append((y2-y1)/(x2-x1))
	b1.append(y2 -m1[j]*x2) 

	m = mean(m1)
	b = mean(b1)

	i=0
	x, z,prom =arr.array( 'd' ), arr.array( 'd' ), arr.array( 'd' )
	while i < N:
		x.append(i*.002 -1)
		z.append(m1[j]*x[i]+b1[j])
		prom.append(m*x[i]+b)
		i+=1
	
	g1 = TGraph(N,x,z)
	g1.Draw('same')
	g0 = TGraph(N,x,prom)
        g0.Draw('same')
	g0.SetLineColor(2) 
       
        var =  (z[j]-prom[j])**2
        varianza.append(var)
        bias += (prom[j]-math.sin((j*.002 -1)*math.pi))**2
	j+=1

#print var/1000

vari = mean(varianza)
bias = bias/N
print "varianza", vari
print "bias", bias
print "error ",bias+vari

i=0
u,v, w, zero = arr.array( 'd' ), arr.array( 'd' ), arr.array( 'd' ), arr.array( 'd' )
while i < N:
	zero.append(0)
	u.append(prom[i]-math.sqrt(vari))
	v.append(prom[i]+math.sqrt(vari))
	i+=1



ge = TGraphErrors(N, x, prom, zero, u);
ge.SetFillColor(6);
ge.SetFillStyle(3005);
ge.Draw("a3 same");
ge = TGraphErrors(N, x, prom, zero, v);
ge.SetFillColor(6);
ge.SetFillStyle(3005);
ge.Draw("a3 same");
ge.SetMinimum(-2.2)
ge.SetMaximum(2.5)



g1 = TGraph(N,x,y)
g1.Draw('same')
g1.SetLineColor(4)

g0 = TGraph(N,x,prom)
g0.Draw('same')
g0.SetLineColor(2)






legend = TLegend(0.1,0.7,0.48,0.9)
legend.SetHeader("Process class","C") # option "C" allows to center the header
legend.AddEntry(gr,"f(x) ","f")
legend.AddEntry(g0,"promedio de g(x)","f")
legend.AddEntry(g1,"g(x)","f")
legend.AddEntry(c1,"Varianza: "+str(vari),"f")
legend.AddEntry(c1,"Bias: "+str(bias),"f")
legend.Draw()
c1.SaveAs("resultado2.png")
time.sleep(4)
