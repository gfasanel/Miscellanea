#!/usr/bin/python
import math, os
import ROOT
from DataFormats.FWLite import Events, Handle

#more info at https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookFWLitePython
#more info at https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD#MC_Truth
# http://cmslxr.fnal.gov/source/DataFormats/FWLite/interface/Event.h
# http://cmslxr.fnal.gov/lxr/
# dataset=/*DYToEE*/Phys14DR*/*AODSIM
# https://cmsweb.cern.ch/das/request?input=dataset%3D%2FDYToEE_Tune4C_13TeV-pythia8%2FPhys14DR-AVE20BX25_tsg_PHYS14_25_V3-v1%2FAODSIM&instance=prod%2Fglobal

######################Parsing arguments in python#####################
import sys,getopt #to handle arguments in python

def main(argv):# defining the main function, called later
   try:
      opts, args = getopt.getopt(argv,"un:",["file_number=","usage"])
      #getopt takes three args: a list (argv),short options, long options
      #short options that requires an argument are followed by :, long options requiring an argument are followed by =
   except getopt.GetoptError:
      print("something went wrong")
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-u': # I really don't get why it doesn't work with "-h" ??????
         print('python Z_pt1_pt2_plotter.py -n <file_number>')
         print('or, if you prefer')
         print('python Z_pt1_pt2_plotter.py --file_number=<file_number>')
         sys.exit(0)
      elif opt in ("-n","--file_number"):
         global _N #defining a global variable _N
         _N=arg

if __name__ == "__main__": #Qui non capisco cosa faccia? pero' sicuramente sotto chiamo main con la lista degli argomenti
   main(sys.argv[1:]) #argomento 0 e' il plotter.py, percio' lo scarti e ti prendi gli altri che seguono

########################################################################
#def isAncestor(a,p) :
#   if a == p : 
#      return True
#   for i in xrange(0,p.numberOfMothers()) :
#      if isAncestor(a,p.mother(i)) :
#         return True
#   return False

###Defining classes#############
class gen_electron:
    def __init__(self, px,py,pz,E):#This is the constructor
        self.p4 = ROOT.TLorentzVector(px,py,pz,E)
        self.region = 'none'
        if abs(self.p4.Eta()) < 1.4442:
            self.region =  'barrel'
        elif abs(self.p4.Eta())>1.566  and abs(self.p4.Eta())<2.5:
            self.region = 'endcap'

class Zboson_object:
    def __init__(self, e1, e2):#This is the constructor
        self.e1 = e1
        self.e2 = e2
        self.p4 = e1.p4 + e2.p4
        self.regions = 'none'
        if self.e1.region=='barrel' and self.e2.region=='barrel':
            self.regions = 'BB'
        elif self.e1.region=='barrel' and self.e2.region=='endcap':
            self.regions = 'BE'
        elif self.e1.region=='endcap' and self.e2.region=='barrel':
            self.regions = 'BE'
        elif self.e1.region=='endcap' and self.e2.region=='endcap':
            self.regions = 'EE'

#MiniAOD M-50
sample_location= 'root://xrootd.unl.edu//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/MINIAODSIM/PU20bx25_tsg_castor_PHYS14_25_V1-v1/10000/'
filename=['12BA0756-4681-E411-9C3D-002590A88812.root',
          '1CFCCDC3-4381-E411-AC51-001E67396A22.root',
          '20678BB9-6E84-E411-8354-001E67397751.root',
          '3CCA8B48-6A84-E411-857C-001E67397756.root',
          '420FF764-3082-E411-9A15-002590A36FB2.root',
          '4AD60677-4581-E411-8943-0025B3E0654E.root',
          '620EEEAE-4E81-E411-A175-002590A88812.root',
          '6235AC67-2D82-E411-B094-002590200838.root',
          '90FB27D8-2E82-E411-8ECC-002590A36FB2.root',
          '9660E98A-7A84-E411-B008-001E67397B11.root']


print str(sample_location+filename[int(_N)])


events = Events(str(sample_location+filename[int(_N)]))

# create handle outside of loop
ele_handle  = Handle ('std::vector<pat::Electron>')
ele_label = ("slimmedElectrons")

gen_handle  = Handle ('std::vector<reco::GenParticle>')
gen_label = ("prunedGenParticles") # pruned particles point to high level objectes, even the not stable ones
#packed contain only (and all) the status 1 particles (stable)

#gen_packed_handle  = Handle ('std::vector<pat::PackedGenParticle>')
#gen_packed_label = ("packedGenParticles") #packed contain only (and all) the status 1 particles (stable)


ROOT.gROOT.SetBatch()        # don't pop up canvases
ROOT.gROOT.SetStyle('Plain') # white background

# loop over events

#loopo sugli eventi e a evento fissato mi prendo la collezione degli elettroni

# Per le regioni uso i dizionari
pt_regions=['0_10','10_20','20_30','30_60','60_100','100_200']# just the label of the regions

regions={}
regions['0_10']=dict(name='ptEE0_10',ptmin=0.,ptmax=10.)
regions['10_20']=dict(name='ptEE10_20',ptmin=10.,ptmax=20.)
regions['20_30']=dict(name='ptEE20_30',ptmin=20.,ptmax=30.)
regions['30_60']=dict(name='ptEE30_60',ptmin=30.,ptmax=60.)
regions['60_100']=dict(name='ptEE60_100',ptmin=60.,ptmax=100.)
regions['100_200']=dict(name='ptEE100_200',ptmin=100.,ptmax=200.)

detector_regions=['BB','BE','EE']
hist={}# Ho bisogno di tutta una serie di istogrammi che dipendono dalla variabile, dalla regione in pt e dalla regione del detector
hist['pt1_reco']={}
hist['pt2_reco']={}
hist['pt1_Over_pt2_reco']={}
hist['pt1_gen']={}
hist['pt2_gen']={}
hist['pt1_Over_pt2_gen']={}

for det in detector_regions:
   hist['pt1_reco'][det]={}
   hist['pt2_reco'][det]={}
   hist['pt1_Over_pt2_reco'][det]={}
   hist['pt1_gen'][det]={}
   hist['pt2_gen'][det]={}
   hist['pt1_Over_pt2_gen'][det]={}

histo_ptZ_gen=ROOT.TH1F("ptZ_gen","ptZ_gen",100,0,100)
histo_massZ_gen=ROOT.TH1F("massZ_gen","massZ_gen",150,0,150)
histo_eta0_gen=ROOT.TH1F("eta0_gen","eta0_gen",100,-10,10)
histo_eta1_gen=ROOT.TH1F("eta1_gen","eta1_gen",100,-10,10)

#histo_ptZ_reco=ROOT.TH1F("ptZ_reco","ptZ_reco",100,0,100)
for region in pt_regions:
   print regions[region]['name']
   for det in detector_regions:
      hist['pt1_reco'][det][regions[region]['name']]=ROOT.TH1F(str('pt1_reco_'+det+'_'+regions[region]['name']),str('pt1_reco_'+det+'_'+regions[region]['name']),100,0,100)
      print str('pt1_reco_'+det+'_'+regions[region]['name'])
      hist['pt2_reco'][det][regions[region]['name']]=ROOT.TH1F(str('pt2_reco_'+det+'_'+regions[region]['name']),str('pt2_reco_'+det+'_'+regions[region]['name']),100,0,100)
      hist['pt1_Over_pt2_reco'][det][regions[region]['name']]=ROOT.TH1F(str('pt1_Over_pt2_reco_'+det+'_'+regions[region]['name']),str('pt1_Over_pt2_reco_'+det+'_'+regions[region]['name']),100,0,3)

      hist['pt1_gen'][det][regions[region]['name']]=ROOT.TH1F(str('pt1_gen_'+det+'_'+regions[region]['name']),str('pt1_gen_'+det+'_'+regions[region]['name']),100,0,100)
      hist['pt2_gen'][det][regions[region]['name']]=ROOT.TH1F(str('pt2_gen_'+det+'_'+regions[region]['name']),str('pt2_gen_'+det+'_'+regions[region]['name']),100,0,100)
      hist['pt1_Over_pt2_gen'][det][regions[region]['name']]=ROOT.TH1F(str('pt1_Over_pt2_gen_'+det+'_'+regions[region]['name']),str('pt1_Over_pt2_gen_'+det+'_'+regions[region]['name']),100,0,3)

# loop over the events
counter = 0
counter_none=0

uniform_test=ROOT.TH1F("uniform_test","uniform_test",100,0,1)
gauss_test=ROOT.TH1F("gauss_test","gauss_test",100,0,1)
rand=ROOT.TRandom3()
rand_gauss=ROOT.TRandom3()

for iev,event in enumerate(events):

    uniform_test.Fill(rand.Uniform(0,1)) #x_min,x_max
    gauss_test.Fill(rand_gauss.Gaus(0.5,0.1)) #mean,sigma
    counter =counter +1
    #if iev > 100: break #For quick tests
    #print iev #Ti stampa il numero dell'evento che stai considerando
    # use getByLabel, just like in cmsRun
    event.getByLabel (ele_label,ele_handle)
    event.getByLabel (gen_label,gen_handle)
    #event.getByLabel (gen_packed_label,gen_packed_handle)
    # get the product
    electrons = ele_handle.product()
    gen_particles = gen_handle.product() # These are the pruned ==> use these ones
    #gen_particles = gen_packed_handle.product() These are the packed


    gen0=0
    gen1=0
    ismatched0=0
    ismatched1=0

    pt1=9999
    pt2=-1
    pt1_gen=9999
    pt2_gen=-1
    vector_Z_gen = ROOT.TLorentzVector(0,0,0,0)

    detector_descriptor='none'
    eta0_gen=-100
    eta1_gen=-100

    for igen, genParticle in enumerate(gen_particles): #loop over generated particles
        if (abs(genParticle.pdgId())==11 and genParticle.mother(0).pdgId()==23 ):# it must be an electron, daughter of a Z boson
            if(gen0==0):
                #print "Electron 0: ID, Mother ID", genParticle.pdgId(),genParticle.mother().pdgId()
                gen_electron0= gen_electron(genParticle.px(),genParticle.py(),genParticle.pz(),genParticle.energy())
                #print 'gen px,py,pz,E',gen_electron0.p4.Px(),gen_electron0.p4.Py(),gen_electron0.p4.Pz(),gen_electron0.p4.E()
                gen0=1
                pt1_gen=genParticle.pt()
                eta0_gen=genParticle.eta()
                #print pt1_gen

                for iele, electron in enumerate(electrons): #loop over reconstructed
                    vector_reco = ROOT.TLorentzVector(electron.px(),electron.py(),electron.pz(),electron.energy())
                    dr=999
                    #dr=vector_reco.DeltaR(vector_gen)
                    dr=vector_reco.DeltaR(gen_electron0.p4)
                    if dr<0.15:
                        ismatched0=1 #This tells if the gen0 is reconstructed
                        pt1=vector_reco.Pt()
                    if(ismatched0): 
                       break # This breaks the reconstuction loop
                    
            elif (gen0==1 and gen1==0):
                #print "Electron 1: ID, Mother ID", genParticle.pdgId(),genParticle.mother().pdgId()
                gen_electron1= gen_electron(genParticle.px(),genParticle.py(),genParticle.pz(),genParticle.energy())
                gen1=1
                pt2_gen=genParticle.pt()
                eta1_gen=genParticle.eta()
                #print eta1_gen

                Z=Zboson_object(gen_electron0,gen_electron1)
                vector_Z_gen.SetPxPyPzE(genParticle.mother(0).px(),genParticle.mother(0).py(),genParticle.mother(0).pz(),genParticle.mother(0).energy())
                detector_descriptor=Z.regions
                if(detector_descriptor=='none'):
                   counter_none=counter_none + 1
                   #print "region is none"
                   #print eta0_gen
                   #print eta1_gen

                for iele, electron in enumerate(electrons): #loop over reconstructed
                    vector_reco1 = ROOT.TLorentzVector(electron.px(),electron.py(),electron.pz(),electron.energy())
                    dr=999
                    dr=vector_reco1.DeltaR(gen_electron1.p4)
                    if dr<0.15:
                        ismatched1=1 #This tells if the gen1 is reconstructed
                        pt2=vector_reco1.Pt()
                    if(ismatched1):
                       break #this breaks the reconstruction loop
                if(ismatched0 and ismatched1):break # This breaks the loop over the generated: 

    if (gen0 and gen1):
        histo_eta0_gen.Fill(eta0_gen)
        histo_eta1_gen.Fill(eta1_gen)

        for region in pt_regions: 
            if ( vector_Z_gen.Pt() >= regions[region]['ptmin'] and vector_Z_gen.Pt() < regions[region]['ptmax'] and detector_descriptor!='none'):
                if(pt1_gen < pt2_gen): #swap if 2 is the leading
                   temp=pt1_gen
                   pt1_gen=pt2_gen
                   pt2_gen=temp

                hist['pt1_gen'][detector_descriptor][regions[region]['name']].Fill(pt1_gen)
                hist['pt2_gen'][detector_descriptor][regions[region]['name']].Fill(pt2_gen)
                hist['pt1_Over_pt2_gen'][detector_descriptor][regions[region]['name']].Fill(pt1_gen/pt2_gen)
                histo_massZ_gen.Fill(vector_Z_gen.M())
                histo_ptZ_gen.Fill(vector_Z_gen.Pt())

    if (ismatched0 and ismatched1):
        for region in pt_regions: 
            if (vector_Z_gen.Pt() >= regions[region]['ptmin'] and vector_Z_gen.Pt() < regions[region]['ptmax'] and detector_descriptor!='none'):
                if(pt1 < pt2): #swap if 2 is the leading
                   temp=pt1
                   pt1=pt2
                   pt2=temp
                hist['pt1_reco'][detector_descriptor][regions[region]['name']].Fill(pt1)
                hist['pt2_reco'][detector_descriptor][regions[region]['name']].Fill(pt2)
                hist['pt1_Over_pt2_reco'][detector_descriptor][regions[region]['name']].Fill(pt1/pt2)

# draw everything and save the histos

print "Total number of events",counter
print "Total number of events outside the acceptance",counter_none



#If directory doesn't exist, then create it
if not os.path.exists('~/scratch1/www/Pt1Pt2/pt1_pt2_plots'):
   os.makedirs('~/scratch1/www/Pt1Pt2/pt1_pt2_plots')
   
#file = ROOT.TFile('histograms.root','RECREATE')
file = ROOT.TFile(str('histograms_'+_N+'.root'),'RECREATE')

for region in pt_regions:
    for det in detector_regions:
       hist['pt1_gen'][det][regions[region]['name']].Write()
       hist['pt2_gen'][det][regions[region]['name']].Write()
       hist['pt1_Over_pt2_gen'][det][regions[region]['name']].Write()
###RECO
       hist['pt1_reco'][det][regions[region]['name']].Write()
       hist['pt2_reco'][det][regions[region]['name']].Write()
       hist['pt1_Over_pt2_reco'][det][regions[region]['name']].Write()

histo_ptZ_gen.Write()
histo_massZ_gen.Write()
histo_eta0_gen.Write()
histo_eta1_gen.Write()
uniform_test.Write()
gauss_test.Write()
