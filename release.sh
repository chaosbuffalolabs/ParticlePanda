currentdir=`pwd`
rm ParticlePanda-1.0-release-*
pushd ~/libraries/python-for-android/dist/default/
rm -rf ./bin/*
./build.py --package org.cbl.particlepanda --name "Particle Panda" --version 1.0 --dir "$currentdir" release
popd
cp ~/libraries/python-for-android/dist/default/bin/ParticlePanda-1.0-release-unsigned.apk ./

jarsigner -verbose -sigalg MD5withRSA -digestalg SHA1 -keystore ../keys/cbl-release-key.keystore -signedjar ParticlePanda-1.0-release-signed.apk ParticlePanda-1.0-release-unsigned.apk cbl_release

jarsigner -verify -verbose -certs ParticlePanda-1.0-release-signed.apk

zipalign -v 4 ParticlePanda-1.0-release-signed.apk ParticlePanda-1.0-release-signed-aligned.apk