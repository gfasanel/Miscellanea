#!/bin/bash
#check="--createOnly"
#check="--submitOnly"
check="--check"

#This initializes the environment
#source /afs/cern.ch/work/g/gfasanel/ECALELF_new/CMSSW_5_3_14_patch2/src/Calibration/initCmsEnv.sh

#./scripts/prodAlcareco.sh `parseDatasetFile.sh alcareco_datasets.dat | grep DYJetsToLL| grep madgraph |head '-1' |tail -1`  --isMC -s ZSkim --scheduler=remoteGlidein $check
#./scripts/prodAlcareco.sh `parseDatasetFile.sh alcareco_datasets.dat | grep DYJetsToLL| grep madgraph |head '-2' |tail -1`  --isMC -s ZSkim --scheduler=remoteGlidein $check
#./scripts/prodAlcareco.sh `parseDatasetFile.sh alcareco_datasets.dat | grep DYJetsToLL| grep madgraph |head '-3' |tail -1`  --isMC -s ZSkim --scheduler=remoteGlidein $check

#./scripts/prodAlcareco.sh `parseDatasetFile.sh alcareco_datasets.dat | grep DYToEE| grep powheg |head '-1' |tail -1`  --isMC -s ZSkim --scheduler=remoteGlidein $check
#./scripts/prodAlcareco.sh `parseDatasetFile.sh alcareco_datasets.dat | grep DYToEE| grep powheg |head '-2' |tail -1`  --isMC -s ZSkim --scheduler=remoteGlidein $check
#./scripts/prodAlcareco.sh `parseDatasetFile.sh alcareco_datasets.dat | grep DYToEE| grep powheg |head '-3' |tail -1`  --isMC -s ZSkim --scheduler=remoteGlidein $check

#./scripts/prodAlcareco.sh `parseDatasetFile.sh alcareco_datasets.dat | grep DYJets| grep sherpa |head '-1' |tail -1`  --isMC -s ZSkim --scheduler=remoteGlidein $check
#./scripts/prodAlcareco.sh `parseDatasetFile.sh alcareco_datasets.dat | grep DYJets| grep sherpa |head '-2' |tail -1`  --isMC -s ZSkim --scheduler=remoteGlidein $check
#./scripts/prodAlcareco.sh `parseDatasetFile.sh alcareco_datasets.dat | grep DYJets| grep sherpa |head '-3' |tail -1`  --isMC -s ZSkim --scheduler=remoteGlidein $check

#########################Single Electron Data################################
#./scripts/prodAlcareco.sh `parseDatasetFile.sh alcareco_datasets.dat | grep SingleElectron| grep WSkimPath |head '-1' |tail -1` -s WSkim --scheduler=remoteGlidein $check
#./scripts/prodAlcareco.sh `parseDatasetFile.sh alcareco_datasets.dat | grep SingleElectron| grep WSkimPath |head '-2' |tail -1` -s WSkim --scheduler=remoteGlidein $check
#./scripts/prodAlcareco.sh `parseDatasetFile.sh alcareco_datasets.dat | grep SingleElectron| grep WSkimPath |head '-3' |tail -1` -s WSkim --scheduler=remoteGlidein $check
#./scripts/prodAlcareco.sh `parseDatasetFile.sh alcareco_datasets.dat | grep SingleElectron| grep WSkimPath |head '-4' |tail -1` -s WSkim --scheduler=remoteGlidein $check


#######################Single Electron MC####################################
./scripts/prodAlcareco.sh `parseDatasetFile.sh alcareco_datasets.dat | grep WToENu |head '-1' |tail -1` -s WSkim --scheduler=remoteGlidein $check
#./scripts/prodAlcareco.sh `parseDatasetFile.sh alcareco_datasets.dat | grep WToENu |head '-2' |tail -1` -s WSkim --scheduler=remoteGlidein $check