#more info at https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookFWLitePython
#more info at https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD#MC_Truth
import math, os
import ROOT
from DataFormats.FWLite import Events, Handle

events = Events("root://xrootd.unl.edu//store/mc/Phys14DR/DYToEE_Tune4C_13TeV-pythia8/AODSIM/AVE20BX25_tsg_PHYS14_25_V3-v1/10000/0CCBF0FA-2289-E411-A5D4-003048F0E55A.root") #Questi sono gli AOD

#events = Events("root://xrootd.unl.edu//store/mc/Phys14DR/DYToEE_Tune4C_13TeV-pythia8/MINIAODSIM/AVE20BX25_tsg_PHYS14_25_V3-v1/10000/CE81818A-A289-E411-B899-003048D3CD6C.root") #i miniAOD non riesce ad aprirmeli

# create handle outside of loop
ele_handle  = Handle ('std::vector<reco::GsfElectron>')
ele_label = ("gedGsfElectrons")

gen_handle  = Handle ('std::vector<reco::GenParticle>')
gen_label = ("genParticles")


ROOT.gROOT.SetBatch()        # don't pop up canvases
ROOT.gROOT.SetStyle('Plain') # white background

#PtDummyHist = ROOT.TH1F ("PtDummmy", "PtDummy", 100, 0, 3)

# loop over events

#loopo sugli eventi e a evento fissato mi prendo la collezione degli elettroni

# Per le regioni uso i dizionari
pt_regions=['0_30','30_60','60_100','100_200']# just the label of the regions

regions={}
regions['0_30']=dict(name='ptEE0_30',ptmin=0.,ptmax=30.)
regions['30_60']=dict(name='ptEE30_60',ptmin=30.,ptmax=60.)
regions['60_100']=dict(name='ptEE60_100',ptmin=60.,ptmax=100.)
regions['100_200']=dict(name='ptEE100_200',ptmin=100.,ptmax=200.)


hist={}# Ho bisogno di tutta una serie di istogramma che dipendono dalla variabile e dalla regione
hist['pt1_reco']={}
hist['pt2_reco']={}
hist['pt1_Over_pt2_reco']={}
hist['pt1_gen']={}
hist['pt2_gen']={}
hist['pt1_Over_pt2_gen']={}

for region in pt_regions:
    print regions[region]['name']
    hist['pt1_reco'][regions[region]['name']]=ROOT.TH1F(str('pt1_reco_'+regions[region]['name']),str('pt1_reco_'+regions[region]['name']),100,regions[region]['ptmin'],regions[region]['ptmax'])
    hist['pt2_reco'][regions[region]['name']]=ROOT.TH1F(str('pt2_reco_'+regions[region]['name']),str('pt2_reco_'+regions[region]['name']),100,regions[region]['ptmin'],regions[region]['ptmax'])
    hist['pt1_Over_pt2_reco'][regions[region]['name']]=ROOT.TH1F(str('pt1_Over_pt2_reco_'+regions[region]['name']),str('pt1_Over_pt2_reco_'+regions[region]['name']),100,0,3)

    hist['pt1_gen'][regions[region]['name']]=ROOT.TH1F(str('pt1_gen_'+regions[region]['name']),str('pt1_gen_'+regions[region]['name']),100,regions[region]['ptmin'],regions[region]['ptmax'])
    hist['pt2_gen'][regions[region]['name']]=ROOT.TH1F(str('pt2_gen_'+regions[region]['name']),str('pt2_gen_'+regions[region]['name']),100,regions[region]['ptmin'],regions[region]['ptmax'])
    hist['pt1_Over_pt2_gen'][regions[region]['name']]=ROOT.TH1F(str('pt1_Over_pt2_gen_'+regions[region]['name']),str('pt1_Over_pt2_gen_'+regions[region]['name']),100,0,3)

canvas={}# a comparison plot for each region
for region in pt_regions:
    canvas[str(region)]=ROOT.TCanvas(str(region),str(region))



# loop over the events
for iev,event in enumerate(events):
    #if iev > 100: break
    pt1=9999
    pt2=-1
    pt1_gen=9999
    pt2_gen=-1
    #print iev #Ti stampa il numero dell'evento che stai considerando
    # use getByLabel, just like in cmsRun
    event.getByLabel (ele_label,ele_handle)
    event.getByLabel (gen_label,gen_handle)
    # get the product
    electrons = ele_handle.product()
    gen_particles = gen_handle.product()

    gen0=0
    gen1=0
    ismatched0=0
    ismatched1=0

    for igen, genParticle in enumerate(gen_particles):#loopo sulle particelle generate
        if (abs(genParticle.pdgId())==11 and genParticle.mother().pdgId()==23 ):# se si tratta di un elettrone di madre Z
            vector_gen = ROOT.TLorentzVector(genParticle.px(),genParticle.py(),genParticle.pz(),genParticle.energy())
            if(gen0==0):
                gen0=1
                pt1_gen=genParticle.pt()
                for iele, electron in enumerate(electrons): #loop over reconstructed
                    vector_reco = ROOT.TLorentzVector(electron.px(),electron.py(),electron.pz(),electron.energy())
                    dr=999
                    dr=vector_reco.DeltaR(vector_gen)
                    if dr<0.15: # matching avvenuto
                        ismatched0=1 #This tells if the gen0 is reconstructed
                        pt1=vector_reco.Pt()
                    
            elif (gen0==1 and gen1==0):
                gen1=1
                pt2_gen=genParticle.pt()
                for iele, electron in enumerate(electrons): #loop over reconstructed
                    vector_reco = ROOT.TLorentzVector(electron.px(),electron.py(),electron.pz(),electron.energy())
                    dr=999
                    dr=vector_reco.DeltaR(vector_gen)
                    if dr<0.15: # matching avvenuto
                        ismatched1=1
                        pt2=vector_reco.Pt()
                    break #hai trovato due elettroni e visto se vengono ricostruiti: puoi chiudere il ciclo sulle generate
            vector_Z_gen = ROOT.TLorentzVector(genParticle.mother().px(),genParticle.mother().py(),genParticle.mother().pz(),genParticle.mother().energy())
    #print 'pt1,pt2',pt1,pt2
    #print 'pt1_gen,pt2_gen',pt1_gen,pt2_gen
    if (gen0 and gen1):
        for region in pt_regions: 
            if ((vector_Z_gen.Pt()) >= regions[region]['ptmin'] and (vector_Z_gen.Pt()) < regions[region]['ptmax']):
                hist['pt1_gen'][regions[region]['name']].Fill(pt1_gen)
                hist['pt2_gen'][regions[region]['name']].Fill(pt2_gen)
                hist['pt1_Over_pt2_gen'][regions[region]['name']].Fill(pt1_gen/pt2_gen)
    if (ismatched0 and ismatched1):
        for region in pt_regions: 
            if ((vector_Z_gen.Pt()) >= regions[region]['ptmin'] and (vector_Z_gen.Pt()) < regions[region]['ptmax']):
                hist['pt1_reco'][regions[region]['name']].Fill(pt1_gen)
                hist['pt2_reco'][regions[region]['name']].Fill(pt2_gen)
                hist['pt1_Over_pt2_reco'][regions[region]['name']].Fill(pt1_gen/pt2_gen)

# draw everything and save the histos

#If directory doesn't exist, then create it
if not os.path.exists('~/scratch1/www/Pt1Pt2/pt1_pt2_plots'):
    os.makedirs('~/scratch1/www/Pt1Pt2/pt1_pt2_plots')

file = ROOT.TFile('histograms.root','RECREATE')
for region in pt_regions:
###GEN
    hist['pt1_gen'][regions[region]['name']].Write()
    hist['pt2_gen'][regions[region]['name']].Write()
    hist['pt1_Over_pt2_gen'][regions[region]['name']].Write()
    canvas[str(region)].cd()
    hist['pt1_Over_pt2_reco'][regions[region]['name']].Draw()
    hist['pt1_Over_pt2_gen'][regions[region]['name']].SetLineColor(ROOT.kRed)
    hist['pt1_Over_pt2_gen'][regions[region]['name']].Draw()
    canvas[str(region)].SaveAs(str('~/scratch1/www/Pt1Pt2/pt1_pt2_plots/'+region+'_gen.png'))
    canvas[str(region)].Write()
###RECO
    hist['pt1_reco'][regions[region]['name']].Write()
    hist['pt2_reco'][regions[region]['name']].Write()
    hist['pt1_Over_pt2_reco'][regions[region]['name']].Write()
    canvas[str(region)].cd()
    hist['pt1_Over_pt2_reco'][regions[region]['name']].Draw()
    hist['pt1_Over_pt2_reco'][regions[region]['name']].Draw()
    canvas[str(region)].SaveAs(str('~/scratch1/www/Pt1Pt2/pt1_pt2_plots/'+region+'_reco.png'))
    canvas[str(region)].Write()






