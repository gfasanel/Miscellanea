#more info at https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookFWLitePython
#more info at https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD#MC_Truth
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

Pt1overPt2Hist = ROOT.TH1F ("Pt1overPt2", "Pt1overPt2", 100, 0, 3)
Pt1overPt2GenHist = ROOT.TH1F ("Pt1overPt2Gen", "Pt1overPt2Gen", 100, 0, 3)
Pt1Hist = ROOT.TH1F ("Pt1", "Pt1", 100, 0, 300)
Pt1GenHist = ROOT.TH1F ("Pt1Gen", "Pt1Gen", 100, 0, 300)
Pt2Hist = ROOT.TH1F ("Pt2", "Pt2", 100, 0, 300)
Pt2GenHist = ROOT.TH1F ("Pt2Gen", "Pt2Gen", 100, 0, 300)

invMassHist = ROOT.TH1F ("invMass", "invMass", 100, 0, 300)
# loop over events

#loopo sugli eventi e a evento fissato mi prendo la collezione degli elettroni

for iev,event in enumerate(events):
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

    ismatched0=0
    ismatched1=0
    for iele,electron in enumerate(electrons):#elettroni ricostruiti
        if len(electrons)<2: continue # se meno di 2 el ricostruiti, skippa l'evento
        if electron.pt()<5: continue
        dr=999
        vector_reco = ROOT.TLorentzVector(electron.px(),electron.py(),electron.pz(),electron.energy())

        for igen, genParticle in enumerate(gen_particles):#loopo sulle particelle generate
            if (abs(genParticle.pdgId())==11 and genParticle.mother().pdgId()==23 ):# se si tratta di un elettrone di madre Z
                vector_gen = ROOT.TLorentzVector(genParticle.px(),genParticle.py(),genParticle.pz(),genParticle.energy())
                dr=vector_reco.DeltaR(vector_gen)
                if dr<0.3: # matching avvenuto
                    if (ismatched0==0):
                        ismatched0=1
                        vector_ele1 = ROOT.TLorentzVector(electron.px(),electron.py(),electron.pz(),electron.energy())
                        pt1=electron.pt()
                        pt1_gen=genParticle.pt()
                        Pt1Hist.Fill(pt1)
                        Pt1GenHist.Fill(pt1_gen)
                        print 'ele 0 matched',pt1,pt1_gen
                    elif (ismatched1==0):
                        ismatched1=1
                        vector_ele2 = ROOT.TLorentzVector(electron.px(),electron.py(),electron.pz(),electron.energy())
                        pt2=electron.pt()
                        pt2_gen=genParticle.pt()
                        Pt2Hist.Fill(pt2)
                        Pt2GenHist.Fill(pt2_gen)
                        print 'ele 1 matched',pt2,pt2_gen
                        break #hai trovato due elettroni che matchano: puoi chiudere il ciclo sulle generate

    #print 'pt1,pt2',pt1,pt2
    #print 'pt1_gen,pt2_gen',pt1_gen,pt2_gen
    if (ismatched0 and ismatched1):
        print 'filling pt1/pt2'
        Pt1overPt2Hist.Fill(pt1/pt2)
        Pt1overPt2GenHist.Fill(pt1_gen/pt2_gen)
        invMassHist.Fill((vector_ele1+vector_ele2).M())

# make a canvas, draw, and save it

c1 = ROOT.TCanvas()
Pt1overPt2Hist.Draw()
Pt1overPt2GenHist.SetLineColor(ROOT.kRed)
Pt1overPt2GenHist.Draw("same")
c1.SaveAs("Pt1overPt2.root")

c2 = ROOT.TCanvas()
invMassHist.Draw()
c2.SaveAs("invMass.root")

file = ROOT.TFile('histograms.root','RECREATE')
Pt1overPt2Hist.Write()
Pt1overPt2GenHist.Write()
Pt1Hist.Write()
Pt1GenHist.Write()
Pt2Hist.Write()
Pt2GenHist.Write()
invMassHist.Write()





