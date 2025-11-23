from sentence_transformers import SentenceTransformer
from googleapiclient.discovery import build
import gzip
import time
import re

# gz_path = "ol_dump_works_2025-11-06.txt.gz"
# subject_pattern = re.compile(r'"subjects":\s*(\[[^\]]*\])')
# # extra pattern: # r'"subjects"\s*:\s*\[(.*?)\]'

# count = 0
# with gzip.open(gz_path, 'rt', encoding='utf-8', errors='ignore') as zip:
    
#     # work list the full json lines for each book
#     with open('worklist.txt', "w") as work:
#         with open('subjectlist.txt', "w") as subject:

#             start = time.time()
#             for i, line in enumerate(zip):
#                 if i % 1000000 == 0:
#                     print(f"Line Number: {i}")
                    
#                 if "\"subjects\"" in line:
#                     work.write(line)
                    
#                     match = subject_pattern.search(line)
#                     if match:
#                         subject.write(match.group(1) + "\n")

#             end = time.time()

model = SentenceTransformer("all-MiniLM-L6-v2")

# youtube api key - AIzaSyAA9eTbY21j9nlw_mDfCEOSTIiXk7iuNFk