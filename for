#!/bin/bash
hak=$PWD
cfile=$hak/dist/DEBIAN/conffiles
echo "/opt/pycectv/kanavat.conf" >$cfile
cd dist/opt/pycectv/data/
for  filename in *; do
    echo /opt/pycectv/data/$filename >>$cfile
done
cd $hak
