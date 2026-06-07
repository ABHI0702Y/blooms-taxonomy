"""
Generates a comprehensive multi-subject question dataset and saves it.
Run from: BLOOMS_TAXONOMY/question_paper_builder/
"""
import pandas as pd
from pathlib import Path

TESTING_DIR = Path(__file__).resolve().parent.parent / "testing"

questions = []  # (question_text, marks)

# ── DATA STRUCTURES & ALGORITHMS ───────────────────────────────────────────
dsa = [
    # 4 marks
    ("Define binary search tree and list its properties.", 4),
    ("State the time complexity of bubble sort, merge sort and quick sort.", 4),
    ("List various types of linked lists with one example each.", 4),
    ("Explain the concept of stack with PUSH and POP operations.", 4),
    ("Define hashing. What are different collision resolution techniques?", 4),
    ("What is a priority queue? How is it different from a regular queue?", 4),
    ("State the difference between depth-first search and breadth-first search.", 4),
    ("Define spanning tree. What is the minimum spanning tree?", 4),
    ("List the applications of stack data structure.", 4),
    ("Explain the concept of recursion with a suitable example.", 4),
    # 5 marks
    ("Explain the insertion and deletion operations in a singly linked list with diagrams.", 5),
    ("Describe the binary search algorithm with its time and space complexity.", 5),
    ("Explain heap sort algorithm with example. Write its time complexity.", 5),
    ("Describe the concept of graph representation using adjacency matrix and adjacency list.", 5),
    ("Explain the working of queue using circular array with suitable example.", 5),
    ("Describe the concept of AVL tree and explain the rotation operations.", 5),
    ("Explain Dijkstra's shortest path algorithm with a suitable example.", 5),
    ("Describe the process of building a max-heap from an unsorted array.", 5),
    ("Explain the tower of Hanoi problem and write its recursive solution.", 5),
    ("Describe how infix expression is converted to postfix using stack.", 5),
    # 6 marks
    ("Compare and contrast BFS and DFS traversal with time complexity and applications.", 6),
    ("Differentiate between singly linked list and doubly linked list. Give operations on doubly linked list.", 6),
    ("Analyze the merge sort algorithm and write its recurrence relation. Solve using master theorem.", 6),
    ("Compare linear search and binary search with respect to time complexity and suitability.", 6),
    ("Differentiate between array and linked list. Write algorithms for insertion in both.", 6),
    ("Explain B-tree and B+ tree with their differences and applications.", 6),
    ("Analyze the performance of hash tables with different collision resolution techniques.", 6),
    ("Explain Kruskal's and Prim's algorithm for minimum spanning tree with examples.", 6),
    ("Differentiate between tree and graph. Explain tree traversals with examples.", 6),
    ("Compare and contrast stack and queue with their implementations and applications.", 6),
    # 7 marks
    ("Write short notes on: a) Red-Black Trees b) Splay Trees c) Tries.", 7),
    ("Write short notes on: a) Dynamic Programming b) Greedy Algorithm c) Divide and Conquer.", 7),
    ("Write short notes on: a) Floyd-Warshall Algorithm b) Bellman-Ford Algorithm c) Topological Sorting.", 7),
    # 8 marks
    ("Design an efficient algorithm to find the shortest path between all pairs of vertices in a weighted graph. Explain with a complete example.", 8),
    ("Evaluate the performance of different sorting algorithms and justify which algorithm is most suitable for nearly sorted data, large data sets, and data with many duplicates.", 8),
    ("Design a data structure to implement an LRU (Least Recently Used) cache. Explain the algorithm and analyze its time complexity.", 8),
    ("Construct a B+ tree of order 5 for the keys: 10,20,30,40,50,60,70,80. Explain the insertion and splitting process in detail.", 8),
    ("Design and explain a graph algorithm to detect a cycle in a directed graph. Write the algorithm and trace it on an example.", 8),
]
questions.extend(dsa)

# ── OPERATING SYSTEMS ──────────────────────────────────────────────────────
os_qs = [
    # 4 marks
    ("Define process and thread. List the differences between them.", 4),
    ("State the conditions necessary for a deadlock to occur.", 4),
    ("Define page fault. What happens when a page fault occurs?", 4),
    ("List the various CPU scheduling algorithms with one example each.", 4),
    ("Define semaphore. How is it used for process synchronization?", 4),
    ("What is thrashing? How can it be prevented?", 4),
    ("Define virtual memory and explain its advantages.", 4),
    ("List the file allocation methods used in operating systems.", 4),
    ("State the difference between preemptive and non-preemptive scheduling.", 4),
    ("Define critical section problem and list its requirements.", 4),
    # 5 marks
    ("Explain the producer-consumer problem and its solution using semaphores.", 5),
    ("Describe the working of Round Robin scheduling with an example. Calculate average waiting time.", 5),
    ("Explain the concept of paging in memory management with a diagram.", 5),
    ("Describe different states of a process and draw the process state diagram.", 5),
    ("Explain Banker's algorithm for deadlock avoidance with a suitable example.", 5),
    ("Describe the FCFS disk scheduling algorithm with example. Calculate total head movement.", 5),
    ("Explain segmentation in memory management with advantages and disadvantages.", 5),
    ("Describe the concept of demand paging and page replacement.", 5),
    ("Explain inter-process communication mechanisms with examples.", 5),
    ("Describe the working of a file system with its data structures.", 5),
    # 6 marks
    ("Compare FCFS, SJF, Round Robin, and Priority scheduling algorithms with examples.", 6),
    ("Analyze the dining philosophers problem and propose a solution to avoid deadlock.", 6),
    ("Compare and contrast paging and segmentation memory management techniques.", 6),
    ("Differentiate between internal and external fragmentation. Explain compaction and paging solutions.", 6),
    ("Compare LRU, FIFO, and Optimal page replacement algorithms with an example.", 6),
    ("Differentiate between multiprogramming and multiprocessing. Explain context switching.", 6),
    ("Analyze the readers-writers problem and provide a solution using semaphores.", 6),
    ("Compare contiguous, linked, and indexed file allocation methods with advantages.", 6),
    # 8 marks
    ("Evaluate different CPU scheduling algorithms (FCFS, SJF, SRTF, RR, Priority) for a given set of processes with arrival time and burst time. Calculate average waiting time and turnaround time for each.", 8),
    ("Design a solution for the deadlock problem in an operating system. Explain deadlock detection, prevention, and recovery mechanisms with suitable examples.", 8),
    ("Evaluate the performance of different page replacement algorithms (FIFO, LRU, Optimal) for a given reference string. Calculate page fault rate and justify the best algorithm.", 8),
    ("Design a disk scheduling algorithm that minimizes seek time. Compare SCAN, C-SCAN, and LOOK algorithms with a given request queue.", 8),
]
questions.extend(os_qs)

# ── DATABASE MANAGEMENT SYSTEMS ────────────────────────────────────────────
dbms_qs = [
    # 4 marks
    ("Define normalization. State the objectives of normalization.", 4),
    ("List the different types of SQL joins with syntax.", 4),
    ("Define primary key, foreign key, and candidate key with examples.", 4),
    ("State the ACID properties of a transaction.", 4),
    ("Define ER diagram. List its components.", 4),
    ("What is a view in SQL? What are its advantages?", 4),
    ("List the different types of functional dependencies.", 4),
    ("Define indexing. State different types of indexes.", 4),
    ("State the difference between DDL, DML, and DCL commands.", 4),
    ("What is a stored procedure? State its advantages.", 4),
    # 5 marks
    ("Explain the concept of ER-to-Relational mapping with a suitable example.", 5),
    ("Describe the concept of normalization up to 3NF with examples.", 5),
    ("Explain different types of SQL joins with examples.", 5),
    ("Describe the concept of transaction management and explain commit and rollback.", 5),
    ("Explain the concept of indexing in databases with B-tree and hash indexing.", 5),
    ("Describe the Two-Phase Locking protocol for concurrency control.", 5),
    ("Explain the different integrity constraints in SQL with examples.", 5),
    ("Describe the concept of database security and authorization.", 5),
    ("Explain the concept of relational algebra with five basic operations.", 5),
    ("Describe query optimization techniques used in DBMS.", 5),
    # 6 marks
    ("Compare and contrast 1NF, 2NF, 3NF, and BCNF with examples showing decomposition.", 6),
    ("Differentiate between SQL and NoSQL databases. When would you choose one over the other?", 6),
    ("Analyze the different concurrency control problems (lost update, dirty read, unrepeatable read) and their solutions.", 6),
    ("Compare different database recovery techniques: checkpoint, log-based, and shadow paging.", 6),
    ("Differentiate between centralized, distributed, and client-server database architectures.", 6),
    ("Analyze and construct an ER diagram for a university database management system.", 6),
    # 8 marks
    ("Design a complete relational database schema for an e-commerce application. Define all entities, relationships, and constraints. Normalize the schema to 3NF.", 8),
    ("Evaluate different concurrency control mechanisms (locking, timestamp ordering, MVCC). Analyze their performance trade-offs and justify the best approach for a banking application.", 8),
    ("Design and explain a comprehensive query optimization strategy. Discuss cost estimation, join ordering, and index selection with suitable examples.", 8),
]
questions.extend(dbms_qs)

# ── COMPUTER NETWORKS ──────────────────────────────────────────────────────
cn_qs = [
    # 4 marks
    ("Define OSI model and list its seven layers.", 4),
    ("State the difference between TCP and UDP protocols.", 4),
    ("Define IP addressing. What is subnetting?", 4),
    ("List the different types of network topologies.", 4),
    ("Define DNS and explain its purpose.", 4),
    ("What is DHCP? State its working principle.", 4),
    ("Define routing and switching. State their differences.", 4),
    ("List the functions of the data link layer.", 4),
    ("Define firewall. List different types of firewalls.", 4),
    ("State the difference between IPv4 and IPv6.", 4),
    # 5 marks
    ("Explain the TCP three-way handshake with a diagram.", 5),
    ("Describe the concept of subnetting with an example for a Class C network.", 5),
    ("Explain the working of ARP and RARP protocols.", 5),
    ("Describe the sliding window protocol with its working.", 5),
    ("Explain the concept of CSMA/CD and CSMA/CA with their applications.", 5),
    ("Describe the working of SMTP, POP3, and IMAP protocols.", 5),
    ("Explain the concept of VLANs and their advantages.", 5),
    ("Describe different routing algorithms: distance vector and link state.", 5),
    ("Explain the concept of congestion control in TCP.", 5),
    ("Describe the working of HTTP and HTTPS protocols.", 5),
    # 6 marks
    ("Compare and contrast TCP and UDP. Explain when each is preferred with examples.", 6),
    ("Differentiate between circuit switching and packet switching with their advantages.", 6),
    ("Compare different routing protocols: RIP, OSPF, and BGP with their use cases.", 6),
    ("Analyze the concept of network security. Explain SSL/TLS handshake protocol.", 6),
    ("Compare and contrast IPv4 and IPv6 addressing. Explain the need for IPv6.", 6),
    ("Differentiate between guided and unguided transmission media with examples.", 6),
    # 8 marks
    ("Design a complete network architecture for a university campus with multiple buildings. Specify the topology, devices, protocols, and addressing scheme.", 8),
    ("Evaluate different error detection and correction techniques (parity, CRC, Hamming code). Analyze their effectiveness with suitable examples.", 8),
    ("Design and explain a secure network communication system. Discuss cryptography, digital signatures, certificates, and VPN.", 8),
]
questions.extend(cn_qs)

# ── MACHINE LEARNING & AI ──────────────────────────────────────────────────
ml_qs = [
    # 4 marks
    ("Define supervised, unsupervised, and reinforcement learning with examples.", 4),
    ("List different activation functions used in neural networks.", 4),
    ("State the bias-variance tradeoff in machine learning.", 4),
    ("Define overfitting and underfitting. How can they be detected?", 4),
    ("List various feature selection techniques used in machine learning.", 4),
    ("What is cross-validation? State its types.", 4),
    ("Define precision, recall, and F1 score.", 4),
    ("List the steps in the machine learning pipeline.", 4),
    ("What is gradient descent? State its types.", 4),
    ("Define confusion matrix and its components.", 4),
    # 5 marks
    ("Explain the working of K-means clustering algorithm with example.", 5),
    ("Describe the backpropagation algorithm in neural networks.", 5),
    ("Explain the concept of decision tree with information gain and Gini index.", 5),
    ("Describe Support Vector Machine with the concept of hyperplane and margin.", 5),
    ("Explain the concept of Random Forest and how it reduces overfitting.", 5),
    ("Describe Principal Component Analysis (PCA) and its applications.", 5),
    ("Explain the Naive Bayes classifier with its assumptions and applications.", 5),
    ("Describe the working of the K-Nearest Neighbors (KNN) algorithm.", 5),
    ("Explain the concept of regularization (L1 and L2) in machine learning.", 5),
    ("Describe the concept of ensemble learning with bagging and boosting.", 5),
    # 6 marks
    ("Compare and contrast supervised, unsupervised, and semi-supervised learning with examples.", 6),
    ("Analyze the working of convolutional neural networks (CNN) for image classification.", 6),
    ("Compare K-means and hierarchical clustering algorithms with their advantages.", 6),
    ("Differentiate between classification and regression. Explain logistic regression with sigmoid function.", 6),
    ("Analyze the performance metrics for classification problems and explain ROC curve.", 6),
    ("Compare Ridge regression (L2) and Lasso regression (L1) with their use cases.", 6),
    # 8 marks
    ("Design a complete machine learning pipeline for predicting student academic performance. Include data preprocessing, feature selection, model selection, training, and evaluation.", 8),
    ("Evaluate different machine learning algorithms (Decision Tree, SVM, Neural Network, Random Forest) for a given classification problem. Compare their performance and justify the best choice.", 8),
    ("Design and explain a deep learning architecture for natural language processing. Explain word embeddings, LSTM, and attention mechanisms.", 8),
    ("Evaluate the application of machine learning in healthcare for disease prediction. Design a complete system and discuss ethical considerations.", 8),
]
questions.extend(ml_qs)

# ── WEB TECHNOLOGIES ───────────────────────────────────────────────────────
wt_qs = [
    # 4 marks
    ("Define HTML5 and list its new features.", 4),
    ("State the difference between GET and POST methods in HTTP.", 4),
    ("List the different types of CSS selectors.", 4),
    ("Define JavaScript and state its features.", 4),
    ("What is responsive web design? List its techniques.", 4),
    ("Define REST API and list its principles.", 4),
    ("List the differences between cookies and session storage.", 4),
    ("What is AJAX? State its advantages.", 4),
    ("Define JSON and XML. State their differences.", 4),
    ("List the security vulnerabilities in web applications (OWASP Top 5).", 4),
    # 5 marks
    ("Explain the concept of DOM manipulation using JavaScript with examples.", 5),
    ("Describe the Bootstrap grid system and explain how to create responsive layouts.", 5),
    ("Explain the concept of React.js components, props, and state.", 5),
    ("Describe the working of Django MVT architecture with an example.", 5),
    ("Explain the concept of RESTful web services with HTTP methods and status codes.", 5),
    ("Describe the concept of web security: SQL injection and XSS with prevention.", 5),
    ("Explain CSS Flexbox and Grid layout with suitable examples.", 5),
    ("Describe the concept of Node.js and its event-driven architecture.", 5),
    # 6 marks
    ("Compare and contrast different JavaScript frameworks (React, Angular, Vue) and their use cases.", 6),
    ("Analyze the MVC and MVT design patterns. Compare Django and Flask frameworks.", 6),
    ("Differentiate between server-side rendering and client-side rendering with their advantages.", 6),
    ("Compare SQL databases (MySQL) and NoSQL databases (MongoDB) for web applications.", 6),
    # 8 marks
    ("Design a complete full-stack web application for an online examination system. Specify the architecture, technologies, database schema, and security measures.", 8),
    ("Evaluate different authentication mechanisms (session-based, JWT, OAuth) for a web application. Design a secure authentication system.", 8),
    ("Design and explain a microservices architecture for a large-scale e-commerce application. Discuss API Gateway, service discovery, and load balancing.", 8),
]
questions.extend(wt_qs)

# ── SOFTWARE ENGINEERING ───────────────────────────────────────────────────
se_qs = [
    # 4 marks
    ("Define software engineering and list its principles.", 4),
    ("State the different phases of the software development life cycle (SDLC).", 4),
    ("Define functional and non-functional requirements with examples.", 4),
    ("List the different types of software testing.", 4),
    ("What is a use case diagram? List its components.", 4),
    ("Define cohesion and coupling in software design.", 4),
    ("List the characteristics of good software requirements.", 4),
    ("What is version control? State the advantages of Git.", 4),
    # 5 marks
    ("Explain the Waterfall model with its phases, advantages, and disadvantages.", 5),
    ("Describe Agile methodology and explain the Scrum framework.", 5),
    ("Explain the concept of object-oriented design using UML diagrams.", 5),
    ("Describe the different levels of software testing: unit, integration, system.", 5),
    ("Explain the concept of software metrics and quality assurance.", 5),
    ("Describe the concept of design patterns with examples (Singleton, Factory, Observer).", 5),
    ("Explain the difference between black-box and white-box testing with examples.", 5),
    # 6 marks
    ("Compare Waterfall, Agile, Spiral, and RAD models. Justify which model suits large-scale projects.", 6),
    ("Analyze the concept of software architecture patterns (MVC, Microservices, Layered). Compare their suitability.", 6),
    ("Differentiate between verification and validation. Compare different testing strategies.", 6),
    ("Compare coupling and cohesion types. Analyze their effect on software quality.", 6),
    # 8 marks
    ("Design a complete software project plan for a hospital management system. Include requirements, architecture, design, testing strategy, and project schedule.", 8),
    ("Evaluate different software development methodologies for a startup developing a mobile app. Justify your recommendation with analysis of team size, timeline, and requirements.", 8),
    ("Design and explain a complete test plan for an e-commerce application. Include unit testing, integration testing, performance testing, and security testing strategies.", 8),
]
questions.extend(se_qs)

# ── OBJECT ORIENTED PROGRAMMING (Java/C++) ─────────────────────────────────
oop_qs = [
    # 4 marks
    ("Define the four pillars of object-oriented programming.", 4),
    ("State the difference between class and object with examples.", 4),
    ("Define constructor and destructor. State their types.", 4),
    ("List the access specifiers in Java/C++ with their scope.", 4),
    ("What is method overloading? State the rules for overloading.", 4),
    ("Define interface and abstract class. State their differences.", 4),
    ("What is inheritance? List different types of inheritance.", 4),
    ("Define exception handling. List the keywords used in Java.", 4),
    # 5 marks
    ("Explain polymorphism with method overloading and method overriding examples.", 5),
    ("Describe the concept of inheritance with a multilevel example. Explain method overriding.", 5),
    ("Explain the concept of packages and interfaces in Java with examples.", 5),
    ("Describe the concept of generics (templates) in Java/C++ with examples.", 5),
    ("Explain multithreading in Java. Describe the thread life cycle.", 5),
    ("Describe the concept of design patterns: Singleton, Factory, and Strategy.", 5),
    ("Explain exception handling in Java with try, catch, finally, and throw.", 5),
    # 6 marks
    ("Compare abstract class and interface in Java with their usage scenarios and examples.", 6),
    ("Differentiate between compile-time polymorphism and runtime polymorphism with examples.", 6),
    ("Analyze the SOLID principles of object-oriented design with examples.", 6),
    ("Compare Java and C++ in terms of OOP features, memory management, and portability.", 6),
    # 8 marks
    ("Design an object-oriented model for a library management system. Include all classes, relationships, inheritance hierarchy, and interfaces.", 8),
    ("Evaluate the application of design patterns in building a scalable notification system. Design using Observer, Strategy, and Singleton patterns.", 8),
    ("Design and implement an object-oriented framework for a banking application with proper exception handling, inheritance, and polymorphism.", 8),
]
questions.extend(oop_qs)

# ── THEORY OF COMPUTATION ──────────────────────────────────────────────────
toc_qs = [
    # 4 marks
    ("Define finite automata and list its components.", 4),
    ("State the difference between DFA and NFA.", 4),
    ("Define regular expression and list its operators.", 4),
    ("What is a context-free grammar? Give an example.", 4),
    ("Define Turing machine and list its components.", 4),
    ("State the pumping lemma for regular languages.", 4),
    ("List the closure properties of regular languages.", 4),
    # 5 marks
    ("Explain the conversion of NFA to DFA with a suitable example.", 5),
    ("Describe the construction of a DFA for the language accepting strings ending with '01'.", 5),
    ("Explain the concept of pushdown automaton with an example.", 5),
    ("Describe the Chomsky Normal Form (CNF) conversion for a context-free grammar.", 5),
    ("Explain the concept of decidability and undecidability with the halting problem.", 5),
    ("Describe the minimization of DFA using the table-filling algorithm.", 5),
    # 6 marks
    ("Compare DFA, NFA, and epsilon-NFA with examples showing their equivalence.", 6),
    ("Analyze the relationship between regular languages, context-free languages, and recursively enumerable languages.", 6),
    ("Differentiate between decidable and undecidable problems. Explain Rice's theorem.", 6),
    # 8 marks
    ("Design a Turing machine for recognizing the language {a^n b^n c^n | n >= 1}. Explain the working in detail.", 8),
    ("Evaluate the complexity classes P, NP, NP-Complete, and NP-Hard. Explain the P vs NP problem with the importance of NP-Complete problems.", 8),
]
questions.extend(toc_qs)

# ── CLOUD COMPUTING ────────────────────────────────────────────────────────
cloud_qs = [
    # 4 marks
    ("Define cloud computing and list its essential characteristics.", 4),
    ("List the three service models of cloud computing with examples.", 4),
    ("Define virtualization and its role in cloud computing.", 4),
    ("State the difference between public, private, and hybrid cloud.", 4),
    ("List the advantages and disadvantages of cloud computing.", 4),
    # 5 marks
    ("Explain the concept of Infrastructure as a Service (IaaS) with examples.", 5),
    ("Describe the concept of containerization using Docker with its advantages.", 5),
    ("Explain Kubernetes and its role in container orchestration.", 5),
    ("Describe the concept of serverless computing with examples.", 5),
    ("Explain cloud security challenges and best practices.", 5),
    # 6 marks
    ("Compare IaaS, PaaS, and SaaS service models with real-world examples and use cases.", 6),
    ("Analyze the concept of auto-scaling in cloud computing. Compare horizontal and vertical scaling.", 6),
    ("Differentiate between cloud storage solutions: object storage, block storage, and file storage.", 6),
    # 8 marks
    ("Design a cloud architecture for a global e-learning platform. Specify the cloud services, regions, load balancing, CDN, and disaster recovery.", 8),
    ("Evaluate different cloud providers (AWS, Azure, GCP) for hosting a machine learning application. Compare compute, storage, ML services, and pricing.", 8),
]
questions.extend(cloud_qs)

# ── BLOCKCHAIN TECHNOLOGY ──────────────────────────────────────────────────
blockchain_qs = [
    # 4 marks
    ("Define blockchain and list its key characteristics.", 4),
    ("State the difference between public and private blockchain.", 4),
    ("Define smart contract and state its applications.", 4),
    ("List the consensus mechanisms used in blockchain.", 4),
    ("What is cryptocurrency? How does Bitcoin work?", 4),
    # 5 marks
    ("Explain the concept of distributed ledger technology with blockchain architecture.", 5),
    ("Describe the working of Proof of Work (PoW) consensus mechanism.", 5),
    ("Explain the concept of Ethereum and smart contracts with Solidity.", 5),
    ("Describe the concept of decentralized applications (DApps).", 5),
    ("Explain the blockchain transaction lifecycle with cryptographic hashing.", 5),
    # 6 marks
    ("Compare Proof of Work and Proof of Stake consensus mechanisms with energy efficiency.", 6),
    ("Analyze blockchain applications in supply chain management with a use case.", 6),
    ("Differentiate between blockchain and traditional database systems.", 6),
    # 8 marks
    ("Design a blockchain-based system for academic credential verification. Specify the architecture, smart contracts, and privacy mechanisms.", 8),
    ("Evaluate the security features of blockchain technology. Analyze 51% attacks, double spending, and Sybil attacks with countermeasures.", 8),
]
questions.extend(blockchain_qs)

# ── ARTIFICIAL INTELLIGENCE ────────────────────────────────────────────────
ai_qs = [
    # 4 marks
    ("Define artificial intelligence and list its applications.", 4),
    ("State the difference between informed and uninformed search strategies.", 4),
    ("Define knowledge representation and reasoning.", 4),
    ("List the components of an intelligent agent.", 4),
    ("What is natural language processing? State its tasks.", 4),
    # 5 marks
    ("Explain the A* search algorithm with a suitable example.", 5),
    ("Describe the minimax algorithm for game playing.", 5),
    ("Explain the concept of expert systems with their components.", 5),
    ("Describe the concept of fuzzy logic and its applications.", 5),
    ("Explain the working of a chatbot using NLP techniques.", 5),
    # 6 marks
    ("Compare BFS, DFS, and A* search algorithms for problem solving with time and space complexity.", 6),
    ("Analyze the concept of machine learning vs deep learning vs AI. Draw the relationship.", 6),
    ("Differentiate between rule-based and machine learning approaches in NLP.", 6),
    # 8 marks
    ("Design an AI-based system for autonomous vehicle navigation. Explain the perception, planning, and control components.", 8),
    ("Evaluate different AI techniques for medical image analysis. Design a complete diagnostic system using deep learning.", 8),
]
questions.extend(ai_qs)

# ── MATHEMATICS / ENGINEERING MATHEMATICS ──────────────────────────────────
math_qs = [
    # 4 marks
    ("Define eigen values and eigen vectors. State their properties.", 4),
    ("State the Cayley-Hamilton theorem.", 4),
    ("List the properties of a group in abstract algebra.", 4),
    ("Define probability and state its axioms.", 4),
    ("State Bayes' theorem with its formula.", 4),
    # 5 marks
    ("Explain the concept of Laplace transform with its linearity property.", 5),
    ("Describe numerical methods for solving differential equations: Euler's method.", 5),
    ("Explain the concept of Fourier series and its applications.", 5),
    ("Describe the concept of linear programming and the simplex method.", 5),
    # 6 marks
    ("Compare different numerical integration methods: Trapezoidal, Simpson's 1/3, and 3/8 rules.", 6),
    ("Analyze the application of linear algebra in computer graphics and machine learning.", 6),
    ("Differentiate between discrete and continuous probability distributions with examples.", 6),
    # 8 marks
    ("Design and explain a mathematical model for epidemiological spread of disease (SIR model). Solve using differential equations.", 8),
    ("Evaluate different optimization algorithms (Gradient Descent, Newton's Method, Genetic Algorithms) and justify their applications.", 8),
]
questions.extend(math_qs)

# ── Build DataFrame ─────────────────────────────────────────────────────────
new_df = pd.DataFrame(questions, columns=['question', 'marks'])
print(f"New questions generated: {len(new_df)}")
print(f"Marks distribution:\n{new_df['marks'].value_counts().sort_index()}")

# Load existing data
existing_df = pd.read_csv(TESTING_DIR / "ML_QUESTION_Sheet1_final.csv")
print(f"\nExisting questions: {len(existing_df)}")

# Keep only marks 4-8 from existing + merge new
existing_filtered = existing_df[existing_df['marks'].isin([4,5,6,7,8])]
combined_df = pd.concat([existing_filtered, new_df], ignore_index=True)
combined_df = combined_df.drop_duplicates(subset='question')
print(f"Combined total: {len(combined_df)}")
print(f"Combined marks distribution:\n{combined_df['marks'].value_counts().sort_index()}")

# Save
combined_df.to_csv(TESTING_DIR / "ML_QUESTION_Sheet1_final.csv", index=False)
print(f"\nSaved to {TESTING_DIR / 'ML_QUESTION_Sheet1_final.csv'}")
