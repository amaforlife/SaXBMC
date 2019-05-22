# SaXBMC Repository

This script generates content for my owned saXBMC repository but you can use it for your own needs of course after some modifications.
  
Prerequisites:
You need a repository on your Github account where you can upload your files, folders and addons later. For this you can simply clone this repository. Please delete the contents of the zip folder afterwards.

In the next step you have to create your repository addon (e.g. repository.myrepo) locally in the addon folder of your Kodi installation. You can find informations about the structure and the structure of the required files in the Kodi Wiki or here in the repository.saxbmc within the ZIP folder. Don't forget to add your repo addon to the list of your addons (MY_ADDONS) in the script.

**Before you first run the addon generator, modify the parameters described within the user section of the addon_generator.py to your needs.**

This script is designed for direct upload to your github repository. To do that, simply run addon_generator.py and push the created content to your github. You can use your favorite editor for that. I recommend PyCharm from Jetbrains because it contains modules for a VCS - among others for Github - which make updating, committing and pushing content very easy. You can learn more about the integrated version control in the PyCharm help.

Running the addon_generator.py within PyCharm ist very easy. Just set a starting point on the main routine of the script (penultimate line of the script) and start the script. Then you can push the newly generated content directly from PyCharm into your repository.

Happy repositoring!
