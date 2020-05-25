# DocumentSearch
The goal of this exercise is to create a working program to search a set of documents for the given search term or phrase, and return results in order of relevance. Relevancy is defined as number of times the exact term or phrase appears in the document. Create three methods for searching the documents: • Simple string matching • Text search using regular expressions • Preprocess the content and then search the index Prompt the user to enter a search term and search method, execute the search, and return results.

Three files have been provided for you to read and use as sample search content. Run a performance test that does 2M searches with random search terms, and measures execution time. Which approach is fastest? Why? Provide some thoughts on what you would do on the software or hardware side to make this program scale to handle massive content and/or very large request volume (5000 requests/second or more).  

# Technology Stack
Python 3.7.3

# Git Repository
Download the project from the following git repository https://github.com/asessofia/DocumentSearch

# To test/run 
1. Clone the repository above
2. cd to DocumentSearch
3. run the command python3 main.py
4. Make a selection on the user prompt and proceed
############################################################
How to handle really large files?

	Answer: There is a method named search_really_large_files  in main.py
	
The idea is:
	
seek to a start position in file
read from file to buffer (the search string has to be smaller than the buffer size) but if not at the beginning, drop back the - 1 bytes, to catch the string if started at the end of the last read buffer and continued on the next one.
Increase the counter if found else break loop
	You can always adjust the “bsize”and increase it as much as it is suitable for the hardware you are using and optimize it for the best performance. Large bsize will always increase speed but only if the hardware has the capacity to handle it.

How to handle too many requests per second?
	Answer: This can be achieved by making use of multiprocessing. Let’s say if we have a CPU with 4 cores we will be able to handle 4 requests at a time. And if these requests are heavy then only we should use multiprocessing. Otherwise another solution would be to host heavy code somewhere else with scalability and better hardware to do extensive task while we manage the number of requests with simple threading and call this function which is hosted somewhere else on better hardware. I.e. Separating the searching and request handling tasks.

The results of 1 million random search


Above picture shows the time counted and printed in the script itself.




Above picture shows method_name, execution count, time in millisecond and own time as measured by the profiler.

As you can see here pre-processing takes most of the time as in the current script it is happening every time the object of class is created, but in the real system that would be done only once hence saving us a lot of time. 

Based on testing,the method with preprocessing is the faster as it does not have to search the text files every time but rather it deals with a predefined data structure and it is the just the matter of accessing right values from the dictionary.
We have one time cost of preprocessing the text files but it can be neglected against the better results we get every time after that any word is searched from the text files.

The best approach to take will be to preprocess all the files and add them to a data structure, then whenever the user makes a search, we search the data from this predefined, preprocessed data structure and get results in the blink of an eye.

The docstring is added in each of the methods in “main.py” to clarify what they do. Please follow that for further clarification.
