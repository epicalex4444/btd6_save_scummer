# BTD6_SAVE_SCUMMER
## Warnings
Due to how btd6 makes saves, you have to exit your game in btd6 before making a save otherwise the save may not be what you expect.  
Loading saves from different versions of btd6 can have undesired effects such as removing all trophy store items.  
You can get hacker pooled loading saves from different btd6 accounts.
## Installation
1. Go to the releases section in github and download btd6_save_scummer.zip from the latest release
2. Extract the downloaded file and move it to a desired location
3. If you don't have python installed already you are go to https://www.python.org/downloads/ and download python, make sure to add python to path when installing
4. Open up powershell and navigate to the directory of save_scummer.py using cd and ls commands. navigating in powershell guide: https://forsenergy.com/en-us/windowspowershellhelp/html/a0fab50f-77d4-42b6-b6ae-8f9d46daaa7a.htm
5. You will most likely need to install the python modules psutil and pynput but you may need to install others as well, installing python modules can be done with the command "py -3 -m pip install moduleName", when you try to run save_scummer.py(next step) it will tell you which modules you need to install if any
6. To run the file then enter py -3 save_scummer.py
7. You can also run save_scummer.py in any other way you want, running it through powershell is just an easy an accessible way to do it
## How To Use
Once you have ran the save_scummer.py file you will get the main window and a warning saying you need to add the btd6 save directory and btd6 exe directory to use the program. The BTD6 Exe Directory is the location of the BloonsTD6.exe, it is generelly C:\\Program Files (x86)\\Steam\\steamapps\\common\\BloonsTD6\\. You can get to this address through steam by browsing local files. The BTD6 Save Directory is the location that BTD6 puts save data there will be a file called Profile.Save in the directory. Generelly you should go to C:\\Program Files (x86)\\Steam\\userdata\\, from there the number after userdata indicates which steam account, you can find your steam id at https://steamidfinder.com/. The number after that indicates the game, btd6 is 960090, after that the folders should be linear leading to Profile.Save. Once you have found these folder you can right click the address at the top of file explorer and copy as text and paste in into the input boxes.

Once you have inputted these addresses into the corresponing text box and clicked the set button, assuming these addresses are correct you can start creating and loading saves. If for whatever reason the location of the btd6 exe or save moves you will have to set the new addresses in the settings.

To make a save you write the saves name into the text box in the main window then you click the save button. To load or delete a save you find the save you want in the main window then click the load or delete button directly to the right of it.

You can also set hotkeys in settings to quickly perform save/load these hotkeys will bring up a small menu just for these task. You can also set quicksave and quickload hotkeys which store one save at a time, this save will get overwriten by the next quicksave and is only accessible by the quickload hotkey.
## How It Works
When you make a save it creates a folder with that name in the saves folder, in the folder it copies Profile.Save and Profile.bak from btd6.

When you load a save it closes btd6, copies the Profile.Save and Profile.bak from it's save folder back to btd6 overwritting the current ones there, then opens btd6 again.

When you delete a save it removes the folder and contents from the save folder.
## Future Development
Nothing is set in stone but these are ideas I have to improve the program.    
Either intergrate this into btd6 as a mod or turn it into an exe and so it can be ran just by clicking it.  
improve the gui.
