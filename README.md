# Document Search
This project provides a simple document search engine using Python, Redis, and a corpus of Wikipedia abstracts. Users can search documents using either the "AND" or "OR" search types and receive ranked results based on term frequency-inverse document frequency (TF-IDF). This is a fork of the original project, Simple search engine implementation in Python, created for illustrative purposes to go with this blog post. This fork contains various modifications and enhancements to the original implementation.

## Acknowledgements
We would like to acknowledge the original author, Bart de Goede, for creating the foundation of this project. The blog post and initial code were instrumental in building this enhanced document search engine.

### Installation
Prerequisites
Ensure you have Python 3.6 or higher installed on your system. You also need the apt-get package manager for Linux or brew package manager for macOS to install Redis.

### Installing dependencies and Redis
Clone the repository:
bash
Copy code
git clone https://github.com/ckdvs99/python-searchengine.git
cd document_search
Run the setup.py script to install the required Python packages and Redis:
bash
Copy code
python setup.py install
  ### Note: If you're using an operating system other than Linux or macOS, please manually install Redis on your system.

### Usage
After installing the required packages and Redis, you can use the document search engine by running the following command in the terminal:

bash
Copy code
python run.py
Follow the prompts to input your search query, search type (AND or OR), and the search engine will return ranked results based on relevance. The results will be saved in an Excel file named search_results.xlsx.

### Contributing
Feel free to submit issues or pull requests to help improve this project. All contributions are welcome!

### License
This project is licensed under the MIT License.
