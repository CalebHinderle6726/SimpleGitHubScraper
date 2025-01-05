# SimpleGitHubScraper
Simple multithreaded GitHub scraper

# links.py
Running this will fill a text file with a number of github urls in n batches of 100 whre n is the batches variable inside links.py. Using a Bearer token as authorization will increase the limit on the number of batches that GitHub allows, it is 60 batches without auth. The last number in the initial url used can be adjusted as needed, it represents the starting id of the repos that will be listed off.

# scraper.py
Running this with urls in the **links.txt** file and file type extensions in the **whitelist** variable within the **filewriter** class file will retrieve the raw data from the given repos with urls in the **links.txt** file that are of the file types listed in the whitelist and save them within text files of increasing numbers in the name within a folder called **data**. **Files within data are appended to, so if the scraper is being reran with the same url, there will be duplicate data**. It may help to initialize files for data based on the whitelist as errors can occur when too many threads are used and the files are not premade.

The **directoryHandler** class used within **scraper.py** can be given a Bearer token as authorization to increase the limit on the number of requests that can be made to github. The number of threads within the **diectoryHandler** class can also be adjusted as needed.

The **filewriter** class used within scraper.py holds the whitelist which is a list of file extensions that the scraper will not ignore. The **filewriter** class also has a thread number that can be adjusted as needed.
