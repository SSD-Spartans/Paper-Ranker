# this script fetches 9900 paper details from semantic scholar api in a list of dictionaries
# I am getting these details regarding paper using this script =>title,authors,url,venue,year,fieldsOfStudy.
import re

import requests
from bs4 import BeautifulSoup


def to_lower(text):
    for f in re.findall("([A-Z]+)", text):
        text = text.replace(f, f.lower())
    return text


def paper_details(keyword):
    papers = []
    response = requests.get("https://dblp.org/search/publ/api?q=" + keyword + "&h=1000&format=json")
    response = response.json()
    temp = response['result']['hits']['hit']
    for item in temp:
        info = item['info']
        if info['type'] == "Conference and Workshop Papers":
            papers.append(info)

    return papers


def get_conference_ranks():
    url = "http://cic.tju.edu.cn/faculty/zhileiliu/doc/COREComputerScienceConferenceRankings.html"
    r = requests.get(url)
    html_content = r.content
    soup = BeautifulSoup(html_content, 'html.parser')

    conferences = []

    table = soup.find('table')

    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        conferences.append([ele for ele in cols if ele])
    return conferences




# def get_paper_details():
#     paper_details = []
#     for i in range(0, 9800, 100):
#         response = requests.get(
#             "https://api.semanticscholar.org/graph/v1/paper/search?query=machine+learning&offset=" + str(
#                 i) + "&limit=100&fields=title,authors,url,venue,year,fieldsOfStudy")
#         if (response.status_code == 200):
#             paper_detail = response.json()
#             paper_details.append(paper_detail)
#     return paper_details


''' format of data in listofpaperdetails holding all papers
its a list of dictionaries
[{'total': 5380911, 'offset': 0, 'next': 2, 'data': [{'paperId': '46200b99c40e8586c8a0f588488ab6414119fb28', 'url': 'https://www.semanticscholar.org/paper/46200b99c40e8586c8a0f588488ab6414119fb28', 'title': 'TensorFlow: A system for large-scale machine learning', 'venue': 'OSDI', 'year': 2016, 'fieldsOfStudy': ['Computer Science'], 'authors': [{'authorId': '2057642721', 'name': 'Martín Abadi'}, {'authorId': '144758007', 'name': 'P. Barham'}, {'authorId': '2108406634', 'name': 'Jianmin Chen'}, {'authorId': '2545358', 'name': 'Z. Chen'}, {'authorId': '36347083', 'name': 'Andy Davis'}, {'authorId': '49959210', 'name': 'J. Dean'}, {'authorId': '145139947', 'name': 'M. Devin'}, {'authorId': '1780892', 'name': 'S. Ghemawat'}, {'authorId': '2060655766', 'name': 'Geoffrey Irving'}, {'authorId': '2090818', 'name': 'M. Isard'}, {'authorId': '1942300', 'name': 'M. Kudlur'}, {'authorId': '3369421', 'name': 'Josh Levenberg'}, {'authorId': '3089272', 'name': 'Rajat Monga'}, {'authorId': '144375552', 'name': 'Sherry Moore'}, {'authorId': '20154699', 'name': 'D. Murray'}, {'authorId': '32163737', 'name': 'Benoit Steiner'}, {'authorId': '2080690', 'name': 'P. Tucker'}, {'authorId': '2053781980', 'name': 'Vijay Vasudevan'}, {'authorId': '47941411', 'name': 'Pete Warden'}, {'authorId': '35078078', 'name': 'Martin Wicke'}, {'authorId': '2117163698', 'name': 'Yuan Yu'}, {'authorId': '2108113522', 'name': 'Xiaoqian Zhang'}]}, {'paperId': '9c9d7247f8c51ec5a02b0d911d1d7b9e8160495d', 'url': 'https://www.semanticscholar.org/paper/9c9d7247f8c51ec5a02b0d911d1d7b9e8160495d', 'title': 'TensorFlow: Large-Scale Machine Learning on Heterogeneous Distributed Systems', 'venue': 'ArXiv', 'year': 2016, 'fieldsOfStudy': ['Computer Science'], 'authors': [{'authorId': '2057642721', 'name': 'Martín Abadi'}, {'authorId': '2078528337', 'name': 'Ashish Agarwal'}, {'authorId': '144758007', 'name': 'P. Barham'}, {'authorId': '2445241', 'name': 'E. Brevdo'}, {'authorId': '2545358', 'name': 'Z. Chen'}, {'authorId': '48738717', 'name': 'C. Citro'}, {'authorId': '32131713', 'name': 'G. Corrado'}, {'authorId': '36347083', 'name': 'Andy Davis'}, {'authorId': '49959210', 'name': 'J. Dean'}, {'authorId': '145139947', 'name': 'M. Devin'}, {'authorId': '1780892', 'name': 'S. Ghemawat'}, {'authorId': '153440022', 'name': 'I. Goodfellow'}, {'authorId': '2064102917', 'name': 'Andrew Harp'}, {'authorId': '2060655766', 'name': 'Geoffrey Irving'}, {'authorId': '2090818', 'name': 'M. Isard'}, {'authorId': '39978391', 'name': 'Y. Jia'}, {'authorId': '1944541', 'name': 'R. Józefowicz'}, {'authorId': '2059819603', 'name': 'Lukasz Kaiser'}, {'authorId': '1942300', 'name': 'M. Kudlur'}, {'authorId': '3369421', 'name': 'Josh Levenberg'}, {'authorId': '30415265', 'name': 'Dandelion Mané'}, {'authorId': '3089272', 'name': 'Rajat Monga'}, {'authorId': '144375552', 'name': 'Sherry Moore'}, {'authorId': '20154699', 'name': 'D. Murray'}, {'authorId': '37232298', 'name': 'Christopher Olah'}, {'authorId': '144927151', 'name': 'M. Schuster'}, {'authorId': '1789737', 'name': 'Jonathon Shlens'}, {'authorId': '32163737', 'name': 'Benoit Steiner'}, {'authorId': '1701686', 'name': 'Ilya Sutskever'}, {'authorId': '35210462', 'name': 'Kunal Talwar'}, {'authorId': '2080690', 'name': 'P. Tucker'}, {'authorId': '2657155', 'name': 'Vincent Vanhoucke'}, {'authorId': '2053781980', 'name': 'Vijay Vasudevan'}, {'authorId': '1765169', 'name': 'F. Viégas'}, {'authorId': '1689108', 'name': 'Oriol Vinyals'}, {'authorId': '47941411', 'name': 'Pete Warden'}, {'authorId': '145233583', 'name': 'M. Wattenberg'}, {'authorId': '35078078', 'name': 'Martin Wicke'}, {'authorId': '2117163698', 'name': 'Yuan Yu'}, {'authorId': '2777763', 'name': 'X. Zheng'}]}]}]

'''
