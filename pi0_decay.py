#python code to have the pdf distribution of E1E2 in pi0 decay in two photons
#The energy of the photons id uniform between a minimum and a maximum
import ROOT
import math

rand=ROOT.TRandom3()

E0=10
p=6

min=(E0-p)/2
max=(E0+p)/2


histo_uniform=ROOT.TH1F("histo_uniform","Distribution of E1",100,min,max)
histo_function=ROOT.TH1F("histo_function","Distribution of E1(E0-E1)",100,min,E0*E0/2)

for i in range(0,10000):
    rn=rand.Uniform(min,max)
    histo_uniform.Fill(rn)
    histo_function.Fill(rn*(E0-rn))


print "E1 can be between ",min," and", max
print "Now consider E1(E0-E1)" 
print "The maximum of E1(E0-E1) will be at ",E0*E0/4
print "If I am right, I'd expect a distribution peaked around",E0*E0/4

file_pi0=ROOT.TFile("file_pi0.root","RECREATE")
histo_uniform.Write()
histo_function.Write()

