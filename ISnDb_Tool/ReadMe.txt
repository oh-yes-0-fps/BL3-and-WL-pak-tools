
on the first run it will create the directories and reference files
On conseecutive runs it will make an encrypted .dat that will have that data you told it to have in it

It will creat a Mod folder with a "InventorySerialNumberDatabase.mod.dat" in it,
replace the Null entries with what you want to add, don't delete ones your not replacing

Once you made directories you can run the AssetGuidGen and it will make one thats not currently used in the InventorySerialNumberDatabase
it will add ones you gen to a ModGuid.txt that stores ones youv'e genned yourself, you can add entries from other mods to it to ensure no overlapping with them

This is an alpha tool so no config file or arguments 

to run these open powershell in the directorie
Make sure you have python 3.0+ and for these commands python has to be installed in default location
also replace {UserName} with the current users name
type in command below for Inv_Serial_Gen.py
& C:/Users/{UserName}/AppData/Local/Microsoft/WindowsApps/python3.10.exe Inv_Serial_Gen.py
type in command below for AsserGuidGen.py
& C:/Users/{UserName}/AppData/Local/Microsoft/WindowsApps/python3.10.exe AsserGuidGen.py
