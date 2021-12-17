pyconcrete-admin.py compile --source *.py --pye
sudo rm -r bin_encrypted 
mkdir bin_encrypted
mkdir ./bin_encrypted/working_space
cp *.pye ./bin_encrypted/
cp eHealthDevice ./bin_encrypted/
cp ./working_space/*.jsn  ./bin_encrypted/working_space
cp ./working_space/AmazonRootCA1.* ./bin_encrypted/working_space
echo "sudo chmod 777 eHealthDevice" >> ./bin_encrypted/start_gui.sh
echo "pyconcrete main.pye" >> ./bin_encrypted/start_gui.sh
git log -1 --format="%H" >> ./bin_encrypted/commit_info
sudo chmod 777 ./bin_encrypted/start_gui.sh
rm *.pye
