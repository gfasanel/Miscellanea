import math, os
import ROOT

ROOT.gROOT.SetBatch()        # don't pop up canvases
ROOT.gROOT.SetStyle('Plain') # white background
ROOT.gStyle.SetOptStat(0)

ROOT.gStyle.SetFrameBorderMode(ROOT.kWhite)
ROOT.gStyle.SetFrameFillColor(ROOT.kWhite)
ROOT.gStyle.SetCanvasBorderMode(ROOT.kWhite)
ROOT.gStyle.SetCanvasColor(ROOT.kWhite)
ROOT.gStyle.SetPadBorderMode(ROOT.kWhite)
ROOT.gStyle.SetPadColor(ROOT.kWhite)
ROOT.gStyle.SetStatColor(ROOT.kWhite)

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

print "Regions are: "
for region in pt_regions:
    print region, regions[region]['name']


hist={}# Ho bisogno di tutta una serie di istogramma che dipendono dalla variabile e dalla regione
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


histofile=ROOT.TFile('histograms.root','READ')
print 'File is ', histofile.GetName()
#histofile.ls()

for region in pt_regions:
    for det in detector_regions:
        #print regions[region]['name']
        #print str('pt1_reco_'+det+'_'+regions[region]['name'])
 
        hist['pt1_reco'][det][regions[region]['name']]          =histofile.Get(str('pt1_reco_'+det+'_'+regions[region]['name']))
        hist['pt2_reco'][det][regions[region]['name']]          =histofile.Get(str('pt2_reco_'+det+'_'+regions[region]['name']))
        hist['pt1_Over_pt2_reco'][det][regions[region]['name']] =histofile.Get(str('pt1_Over_pt2_reco_'+det+'_'+regions[region]['name']))
                                                                
        hist['pt1_gen'][det][regions[region]['name']]           =histofile.Get(str('pt1_gen_'+det+'_'+regions[region]['name']))
        hist['pt2_gen'][det][regions[region]['name']]           =histofile.Get(str('pt2_gen_'+det+'_'+regions[region]['name']))
        hist['pt1_Over_pt2_gen'][det][regions[region]['name']]  =histofile.Get(str('pt1_Over_pt2_gen_'+det+'_'+regions[region]['name']))

        hist['pt1_reco'][det][regions[region]['name']]          .GetEntries()
        hist['pt2_reco'][det][regions[region]['name']]          .GetEntries()
        hist['pt1_Over_pt2_reco'][det][regions[region]['name']] .GetEntries()
                                                      
        hist['pt1_gen'][det][regions[region]['name']]           .GetEntries()
        hist['pt2_gen'][det][regions[region]['name']]           .GetEntries()
        hist['pt1_Over_pt2_gen'][det][regions[region]['name']]  .GetEntries()


canvas={}# a comparison plot for each region
for det in detector_regions:
    canvas[det]={}

for region in pt_regions:
    for det in detector_regions:
        canvas[det][str(region)]=ROOT.TCanvas(str(det+'_'+region),str(det+'_'+region))

# draw everything and save the histos

#print hist['pt1_Over_pt2_reco'][regions[region]['name']].GetEntries()


if not os.path.exists('~/scratch1/www/Pt1Pt2/pt1_pt2_plots'):
    os.makedirs('~/scratch1/www/Pt1Pt2/pt1_pt2_plots')

#file = ROOT.TFile('histograms.root','RECREATE')

for region in pt_regions:
    for det in detector_regions:
        canvas[det][str(region)].cd()
        print "plotting"
    #print regions[region]['name']
        hist['pt1_Over_pt2_gen'][det][regions[region]['name']].SetLineColor(ROOT.kRed)

        if(hist['pt1_Over_pt2_gen'][det][regions[region]['name']].Integral()!=0):
            hist['pt1_Over_pt2_gen'][det][regions[region]['name']].Scale(1./hist['pt1_Over_pt2_gen'][det][regions[region]['name']].Integral())
        if(hist['pt1_Over_pt2_reco'][det][regions[region]['name']].Integral()!=0):
            hist['pt1_Over_pt2_reco'][det][regions[region]['name']].Scale(1./hist['pt1_Over_pt2_reco'][det][regions[region]['name']].Integral())

        hist['pt1_Over_pt2_gen'][det][regions[region]['name']].SetMaximum(max([hist['pt1_Over_pt2_gen'][det][regions[region]['name']].GetMaximum(),hist['pt1_Over_pt2_reco'][det][regions[region]['name']].GetMaximum()]))

        hist['pt1_Over_pt2_gen'][det][regions[region]['name']].Draw()
        hist['pt1_Over_pt2_reco'][det][regions[region]['name']].Draw("same")

        label=ROOT.TLatex(0.6,0.85,'Gen entries %i'%hist['pt1_Over_pt2_gen'][det][regions[region]['name']].GetEntries())
        label.SetNDC()

        label2=ROOT.TLatex(0.6,0.75,'Reco entries %i'%hist['pt1_Over_pt2_reco'][det][regions[region]['name']].GetEntries())
        label2.SetNDC()
        label.Draw()
        label2.Draw()

        leg=ROOT.TLegend(0.6,0.6,0.9,0.7)
        leg.SetBorderSize(0)
        leg.SetFillColor(ROOT.kWhite)
        leg.AddEntry(hist['pt1_Over_pt2_gen'][det][regions[region]['name']],"Generated","l")
        leg.AddEntry(hist['pt1_Over_pt2_reco'][det][regions[region]['name']],"Reconstruced","l")

        leg.Draw('same')
        canvas[det][str(region)].SaveAs(str('~/scratch1/www/Pt1Pt2/pt1_pt2_plots/'+det+'_'+region+'.png'))

    #canvas[str(region)].Write()

canvas_ptZ=ROOT.TCanvas("ptZ","ptZ")
ptZ_gen=histofile.Get("ptZ_gen")
ptZ_gen.Draw()
canvas_ptZ.SaveAs('~/scratch1/www/Pt1Pt2/pt1_pt2_plots/ptZ_gen.png')



