currentdir=`pwd`
rm ParticlePanda-0.6-debug.apk
pushd ~/libraries/python-for-android/dist/default/
rm -rf ./bin/*
./build.py --package org.test.particlepanda --name ParticlePanda --version 0.6 --dir "$currentdir" debug
popd
cp ~/libraries/python-for-android/dist/default/bin/ParticlePanda-0.6-debug.apk ./