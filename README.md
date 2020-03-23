# Mission_to_Mars  
Have the mongod running, excute app.py in apps directory.  
After kicking bottom "Scrap New Data", "Latest Mars News", "Featured Mars Image" and "Mars Facts" would all be fetched, saved to MongoDB. Now the index page should show the new data.
# Challenge  
This challenge is an augment of the class project "Mission to Mars".  
To launch [app.py](https://github.com/pqrt12/Mission_to_Mars/blob/master/apps/app.py), a mongod should be running.  
All necessary files are in the [apps](https://github.com/pqrt12/Mission_to_Mars/blob/master/apps) directory: [scraping.py](https://github.com/pqrt12/Mission_to_Mars/blob/master/apps/scraping.py), [hemisphere.html](https://github.com/pqrt12/Mission_to_Mars/blob/master/apps/templates/hemisphere.html), [index.html](https://github.com/pqrt12/Mission_to_Mars/blob/master/apps/templates/index.html).  
All four Mars Hemisphere full resolution images URLs were scrapped and saved in mongoDb. Each Hemisphere image may be viewed in a new route "/hemisphere/\<index\>".  
Minor changes were done in the DataFrame of Mars fact table, and it is now displaced using Bootstrap table.  
After new scraping is done, it is redirected back to the homepage automatically, with the scraping timestamp.  
There are two Jupyter Notebook files. [Mission_to_Mars.ipynb](https://github.com/pqrt12/Mission_to_Mars/blob/master/Practice/Mission_to_Mars.ipynb) is for the "Mission to Mars" class project. The challenge trial was done in [hemispheres.ipynb](https://github.com/pqrt12/Mission_to_Mars/blob/master/Practice/hemispheres.ipynb).
