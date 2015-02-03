#!/bin/bash

#check="--createOnly"
#check="--submitOnly"
check="--check"

./scripts/prodNtuples.sh `parseDatasetFile.sh alcareco_datasets.dat | grep DYJetsToLL| grep madgraph |head '-1' |tail -1` --type=ALCARECOSIM --develRelease --scheduler=lsf $check

exit 0

./scripts/prodNtuples.sh `parseDatasetFile.sh alcareco_datasets.dat | grep DYJetsToLL| grep madgraph |head '-2' |tail -1` --type=ALCARECOSIM --develRelease --scheduler=lsf $check
./scripts/prodNtuples.sh `parseDatasetFile.sh alcareco_datasets.dat | grep DYJetsToLL| grep madgraph |head '-3' |tail -1` --type=ALCARECOSIM --develRelease --scheduler=lsf $check



#./scripts/prodNtuples.sh `parseDatasetFile.sh alcareco_datasets.dat | grep DYToEE| grep powheg |head '-1' |tail -1` --type=ALCARECOSIM
#./scripts/prodNtuples.sh `parseDatasetFile.sh alcareco_datasets.dat | grep DYToEE| grep powheg |head '-2' |tail -1` --type=ALCARECOSIM
#./scripts/prodNtuples.sh `parseDatasetFile.sh alcareco_datasets.dat | grep DYToEE| grep powheg |head '-3' |tail -1` --type=ALCARECOSIM

#./scripts/prodNtuples.sh `parseDatasetFile.sh alcareco_datasets.dat | grep DYJets| grep sherpa |head '-1' |tail -1` --type=ALCARECOSIM
#./scripts/prodNtuples.sh `parseDatasetFile.sh alcareco_datasets.dat | grep DYJets| grep sherpa |head '-2' |tail -1` --type=ALCARECOSIM
#./scripts/prodNtuples.sh `parseDatasetFile.sh alcareco_datasets.dat | grep DYJets| grep sherpa |head '-3' |tail -1` --type=ALCARECOSIM
