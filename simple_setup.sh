DST=/data/x/tools/cmd-mind
PKG=/data/x/tools/pkgs/cmd-mind-simple
rm -rf $DST
mkdir -p /data/x/tools/pkgs
cp -r ./ $PKG
ln -s $PKG/src  $DST
