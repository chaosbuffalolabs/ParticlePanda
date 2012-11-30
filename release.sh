currentdir=`pwd`
rm ParticlePanda-1.0-release-unsigned.apk
pushd ~/libraries/python-for-android/dist/default/
rm -rf ./bin/*
./build.py --package org.cbl.particlepanda --name "Particle Panda" --version 1.0 --dir "$currentdir" release
popd
cp ~/libraries/python-for-android/dist/default/bin/ParticlePanda-1.0-release-unsigned.apk ./