#for entry in `ls $search_dir`; do
    #echo $entry
    ##img2py -a transmission.p test.py
#done
rm ../images.py
echo "from wx.lib.embeddedimage import PyEmbeddedImage" >> ../images.py
for entry in `ls *.png`; do
    echo $entry
    img2py -a $entry ../images.py
    
done
