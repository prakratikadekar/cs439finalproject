# from sentence_transformers import SentenceTransformer
import gzip
import time
import re
import os.path
import json
import csv

gz_path = "ol_dump_editions_2025-11-06.txt.gz"

# removed "General"
# maybe to remove: History, Economics
politics_subject_list = ["POLITICAL SCIENCE", "History", "Politics and government", "Philosophy", "Public Policy", "SOCIAL SCIENCE", "Political Science", "Government", "BUSINESS & ECONOMICS", "Democracy", "Politics/International Relations", "Foreign relations", "Economics", "The State", "Anthropology", "International relations", "Cultural", "Cultural Policy", "Political aspects"]

# removed "General", "Algebra", "Development", "Education", "Social sciences", "Congresses", "Congrès", "Kongress", "Physics", "Informatique"
computer_science_subject_list = ["Artificial intelligence", "Software engineering", "Computer software", "Mathematics", "Computer networks", "Information storage and retrieval systems", "Artificial Intelligence (incl. Robotics)", "Information systems", "Computer Communication Networks", "Computer vision", "Data processing", "Information Systems Applications (incl. Internet)", "Database management","Data mining", "Algorithm Analysis and Problem Complexity", "Logic design", "Electronic data processing", "Information retrieval", "Information organization", "Computer simulation", "Optical pattern recognition", "Computational complexity", "Engineering", "Computer graphics", "User Interfaces and Human Computer Interaction", "Computers", "Information Systems", "Information technology", "Data structures (Computer science)", "Data protection", "Data encryption (Computer science)", "Multimedia systems", "Data Mining and Knowledge Discovery", "Computer security", "Management information systems", "Management of Computing and Information Systems", "Computational Mathematics and Numerical Analysis", "Mathematical Logic and Formal Languages", "Pattern perception", "Image Processing and Computer Vision", "Information theory", "Computer network architectures", "Logics and Meanings of Programs", "Computation by Abstract Devices", "Computers and Society", "Operating systems (Computers)", "Systems and Data Security", "Programming Languages, Compilers, Interpreters", "Algorithms", "Computer Science, general", "Data Encryption", "Simulation and Modeling", "Human-computer interaction", "Information Systems Applications (incl.Internet)", "Programming Techniques", "Computer programming", "Discrete Mathematics in Computer Science", "Telecommunication","Computer science, mathematics", "COMPUTERS", "Computer engineering", "Bioinformatics", "Computational Science and Engineering", "Symbolic and mathematical Logic", "Computer Imaging, Vision, Pattern Recognition and Graphics", "Internet", "Computational intelligence", "Engineering mathematics", "Computer system performance", "Computer algorithms", "Mathematical optimization", "Security measures", "Computer networks, security measures", "Numerical analysis", "Coding theory", "Statistics", "Information Systems and Communication Service", "Computer-aided design", "Combinatorial analysis", "Mathematical models", "Computer Science", "Systems engineering", "Computer software, development", "Mathematics of Computing", "Business Information Systems", "Image processing", "Economics", "Translators (Computer programs)", "Application software"]

works_pattern = re.compile(r'/works/[^"]+')

def get_subject_list(line: str):
    subject_start = line.find('"subjects": [')
    if subject_start == -1:
        return []

    count_of_bracket = 0
    subject_end = subject_start

    for i in range(subject_start, len(line)):
        if line[i] == '[':
            count_of_bracket += 1
        
        elif line[i] == ']':
            count_of_bracket -= 1

            if count_of_bracket == 0:
                subject_end = i
                break
    subject_list = line[subject_start:subject_end+1]
    all_subject_in_book_list = re.findall(r'"([^"]*)"', subject_list)

    return all_subject_in_book_list


def get_all_necessary_books():
    with gzip.open(gz_path, 'rt', encoding='utf-8', errors='ignore') as zip:
        with open('languagelist.txt', "w", encoding = 'utf-8') as language:
                workslist = set()

                start = time.time()

                
                for i, line in enumerate(zip):
                    if i % 100000 == 0:
                        print(f"Line Number in Zip: {i}")

                    if "/languages/eng" in line and "/works/" in line and "isbn_" in line:

                        if_added = 0

                        match2 = works_pattern.search(line)
                        
                        if match2:
                            work_number = match2.group(0)
                            if work_number in workslist:
                                continue

                            all_subject_in_book_list = get_subject_list(line)

                            for subject in politics_subject_list:
                                if subject in all_subject_in_book_list:
                                    if_added = 1
                                    break

                            if (if_added == 0):
                                for subject in computer_science_subject_list:
                                    if subject in all_subject_in_book_list:
                                        if_added = 1
                                        break
                            if (if_added == 1):
                                language.write(line)
                                workslist.add(work_number)

                end = time.time()
    return end - start

# title, isbn, description, subjects
def clean_data_to_necessities():
    with open("languagelist.txt", 'r', encoding = 'utf-8') as data:
        with open("book_data.csv", "w", newline = '', encoding = 'utf-8') as file:
            csv_writer = csv.writer(file, delimiter = '\t')
            csv_writer.writerow(['Title', 'ISBN-10', 'ISBN-13', 'Subjects', 'Description'])

            start = time.time()

            for i, line in enumerate(data):
                if i % 100000 == 0:
                    print(f"Line Number in Book txt file: {i}")

                split_line_by_tab = line.strip().split('\t')
                all_data = split_line_by_tab[4].strip()
                try:
                    correct_json_format_data = json.loads(all_data)
                except Exception as e:
                    print(f"Parse Error: {all_data[:200]}")
                    print("Bad line: {a}")
                title_data = correct_json_format_data.get('title', "")
                isbn_10_data = ",".join(correct_json_format_data.get('isbn_10', []))
                isbn_13_data = ",".join(correct_json_format_data.get('isbn_13', []))
                subjects_data = ",".join(correct_json_format_data.get('subjects', []))
                description_dict = correct_json_format_data.get('description', {})
                if isinstance(description_dict, dict):
                    description = description_dict.get('value', "")
                elif isinstance(description_dict, str):
                    description = description_dict
                else:
                    description = ""

                description = description.replace('\n', ' ').replace('\r', ' ')

                csv_writer.writerow([title_data, isbn_10_data, isbn_13_data, subjects_data, description])
            
            end = time.time()
    return end - start


def main():
    time = 0
    if not os.path.exists("languagelist.txt"):
        time = get_all_necessary_books()
    
    clean_time = clean_data_to_necessities()

    if time != 0:
        print(f"Total Time To Get All Books: {time}")

    print(f"Time to turn data into CSV: {clean_time}")

main()