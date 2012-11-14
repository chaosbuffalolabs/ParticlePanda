pushd ~/libraries/python-for-android/dist/default/
rm -rf ./bin/*
./build.py --package org.test.particlepanda --name ParticlePanda --version 0.5 --dir '/media/hd/Documents/Chaos Buffalo/CBLParticleSystem/' debug
popd
cp ~/libraries/python-for-android/dist/default/bin/ParticlePanda-0.5-debug.apk ./