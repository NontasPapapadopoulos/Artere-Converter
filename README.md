# Artere-Converter 


The aim of this project is to create a converter between two power flow solvers ARTERE and Pandapower. 
Pandapower is a modern OSS program for power system simulation while ARTERE is an older one with no access to the source code. 

Here you can find information for both: 
1) Pandapower: http://www.pandapower.org/ 
2) ARTERE: https://people.montefiore.uliege.be/vct/software.html

This project contains two files. 
1) from_artere file converts an ARTERE network in another form that could be consumable from Pandapower. 
2) The file to_artere, converts a network from Pandapower to ARTERE 


 ##  How it Works: 
If you want to convert a network from ARTERE to Pandapower, you must insert the program to the same folder with your project and all you have to type is:

  `import from_artere` 
  
   `from_artere.from_artere("name_of_the_file.dat") `

Similarly, If you want to convert a network from Pandapower to ARTERE, you must type: 

   `import to_artere` 
   
   `to_artere.to_artere("name_of_the_file.py")`


##  Explain the code: 
* In order to convert an ARTERE network to a Pandapower network first, we have to open and read the dat file. 
Secondly we are checking for comments and getting rid of them. After getting riding the comments we split the text whenever there is a semicolon. 
Then we iterate with a for loop through each line. 
While we are iterating, we  check what is the type of the record. According to the type of record, we parse the data. After parsing the data we create Strings in a proper form and we store them in lists. After we finish with parsing, we create a new file with ".py" and we move the strings from the lists to the new file. 

* Converting a Pandapower network to ARTERE network is a pretty similar process. Iterating through  net elements, we parse the data and store them in dictionaries. After finishing with this proccess, we create a file with ".dat" extension and we create Strings in proper form and store them in the new file. 


## Results 
You can find two networks, database and 6bus in both forms in this repository. You can try and check the results if you run power flow analysis with ARTERE and Pandapower


## Required software

   1) ARTERE: https://people.montefiore.uliege.be/vct/software.html Check for downloads
   2)  Pandapower: http://www.pandapower.org/
   3) Python installed in your computer
    
   Ι strongly recomend PyCharm as IDE. Else you can use Jupiter Notebook

   * Download PyCharm: https://www.jetbrains.com/pycharm/
   * Download Anaconda: https://www.anaconda.com/
   * Down load Python: https://www.python.org/downloads/
   * Install pandapower: Open a cmd and type pip install pandapower
   * Then Open pycharm and press Ctrl + alt + S, go to project -> python interpeter, select python interpeter and pres + to add Pandapower in your project


