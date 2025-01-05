import filewriter
import directoryHandler
from requests_html import HTMLSession

branch = ''
directoryUrl = ''
s = HTMLSession()
filewriter = filewriter.filewriter()
directoryHandler = directoryHandler.directoryHandler(filewriter)

with open('links.txt', 'r') as linksFile:
    numRepos = 100
    urls = [next(linksFile).replace('\n', '') for _ in range(numRepos)]  # Getting the first numRepos repos from list in links.txt

for url in urls:
    response = s.get(url)
    response.html.render()
    webPage = response
    try:
        branchButton = webPage.html.find('[id="branch-picker-repos-header-ref-selector"]')[0]  # Finding the default branch button of the current repo
    except:
        print("Empty repo: ", url)  # Current repo has no branch and is therefore empty
        continue    
    branch = branchButton.attrs["aria-label"].rsplit(" ", 1)[0]  # Getting branch name of default branch
    directoryUrl = url + "/tree/" + branch + "/"
    print("Parsing: ", url)
    filetable = webPage.html.find('[aria-labelledby="folders-and-files"]')[0]  # Getting initial list of directories and files in repo

    if filetable:
        for row in filetable.find('tr,[id]'):
            if "react-directory-row" in row.attrs["class"]:
                elem = row.find('a')  # Getting each element in the row on the default github repo page
                if len(elem) > 0:
                    elem = elem[0]
                    if "(File)" in elem.attrs["aria-label"]:
                        filewriter.addFile(elem.attrs["href"])  # Adding the file to the shared list of files between all the filewriter threads
                    elif "(Directory)" in elem.attrs["aria-label"]:
                        # Adding the directory and branch name to the shared list of directories between all the directory handler threads
                        directoryHandler.addDir([directoryUrl + elem.attrs["aria-label"].split(',')[0] + "?noancestors=1", branch])
    else:
        print("no filetable")
        print(webPage.html.find("title"))

