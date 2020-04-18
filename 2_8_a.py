from ROOT import TCanvas, gROOT, TGraph, TFile, gStyle, TLegend,TGraphErrors
import pandas as pd
import array as arr
import math 
import time
import numpy as np
from statistics import variance, mean 
import sys

fields = ['x', 'y']

df = pd.read_csv('dataset.csv', skipinitialspace=True, usecols=fields)
derecha = df['x'].tolist()
izquierda = df['y'].tolist()

N = 1001
i = 0
x, y = arr.array( 'd' ), arr.array( 'd' )


while i < N:
	x.append(i*.002 -1)
	y.append(math.sin(x[i]*math.pi))
        i+=1

c1 = TCanvas('c1','c1', 900, 600 )

gr = TGraph(N,x,y)
gr.SetLineColor( 4 )
gr.SetTitle( 'H0 = b' )
gr.GetXaxis().SetTitle( 'x' )
gr.GetYaxis().SetTitle( 'sin(pi*x)' )
gr.Draw( 'AC' )


varianza = arr.array( 'd' )
j = 0

promedio = list()
bias = 0.0
while j < N-1:
	c1.Update()
	b1 = 	float(derecha[j])+float(derecha[j])/2
	#b1 = y1+y2/2
        promedio.append(b1)
	i=0
	x, y, prom = arr.array( 'd' ),arr.array( 'd' ), arr.array( 'd' )
        a = mean(promedio)
	while i < N:
		x.append(i*.002 -1)
		y.append(b1)
		prom.append(a)
		i+=1
	g1 = TGraph(N,x,y)
	g1.Draw('same')
        g0 = TGraph(N,x,prom)
        g0.Draw('same')
	g0.SetLineColor(2)
	j+=1

        varianza.append((b1-mean(promedio))**2)       
        bias += (mean(promedio)-math.sin((j*.002 -1)*math.pi))**2


var = mean(varianza)
std = math.sqrt(var)
bias = bias/(N-1)
print "varianza", var
print "std ", std
print "bias", bias


c1.Update()



i=0
q, u,z,w, zero = arr.array( 'd' ), arr.array( 'd' ), arr.array( 'd' ), arr.array( 'd' ), arr.array( 'd' )
while i < N:
	q.append(i*.002 -1)
	zero.append(0)
	u.append(prom[i]+std)
	z.append(prom[i]-std)
	w.append(math.sin(x[i]*math.pi))
	i+=1





ge = TGraphErrors(1000, x, prom, zero, z);
ge.SetFillColor(6);
ge.SetFillStyle(3005);
ge.Draw("a3 same");
ge = TGraphErrors(1000, x, prom, zero, u);
ge.SetFillColor(6);
ge.SetFillStyle(3005);
ge.Draw("a3 same");

ge.SetMinimum(-1.2)
ge.SetMaximum(1.5)

gr = TGraph(N,x,w)
gr.SetLineColor( 4 )
gr.SetTitle( 'H0 = b' )
gr.GetXaxis().SetTitle( 'x' )
gr.GetYaxis().SetTitle( 'sin(pi*x)' )
gr.Draw( 'same' )

g0 = TGraph(N,x,prom)
g0.Draw('same')
g0.SetLineColor(2)



legend = TLegend(0.1,0.7,0.48,0.9)
legend.SetHeader("Process class","C") # option "C" allows to center the header
legend.AddEntry(gr,"f(x) ","f")
legend.AddEntry(g0,"promedio de g(x)","f")
legend.AddEntry(g1,"g(x)","f")
legend.AddEntry(c1,"Varianza: "+str(var),"f")
legend.AddEntry(c1,"Bias: "+str(bias),"f")
legend.Draw()

c1.SaveAs("resultadoS.png")
time.sleep(4)
