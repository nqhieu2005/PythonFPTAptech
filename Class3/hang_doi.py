from collections import deque

hang_doi = deque(["Minh", "Hoa", "Hai", "Huong"])

hang_doi.append("Hieu")
hang_doi.popleft()
print(hang_doi)