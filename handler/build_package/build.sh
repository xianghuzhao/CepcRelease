#!/bin/sh

make_jobs=$1

mkdir -p build
cd build

echo ' >>>> Run cmake'
cmake ..

echo ''
echo ' >>>> Run make'
make -j$make_jobs

echo ''
echo ' >>>> Run make install'
make install
