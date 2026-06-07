from django.core.management.base import BaseCommand
from app.models import College, Branch, Subject

BRANCH_TEMPLATES = {
    "CSE": {
        "name": "Computer Science and Engineering",
        "semesters": {
            "SEM I":    ["Engineering Mathematics I", "Engineering Physics", "Programming in C", "Engineering Drawing", "Basic Electrical Engineering"],
            "SEM II":   ["Engineering Mathematics II", "Data Structures", "Digital Electronics", "Environmental Studies", "Communication Skills"],
            "SEM III":  ["Object Oriented Programming", "Discrete Mathematics", "Computer Organization", "Database Management Systems", "Operating Systems"],
            "SEM IV":   ["Analysis of Algorithms", "Computer Networks", "Software Engineering", "Theory of Computation", "Microprocessors"],
            "SEM V":    ["Machine Learning", "Web Technologies", "Information Security", "Compiler Design", "Cloud Computing"],
            "SEM VI":   ["Artificial Intelligence", "Distributed Systems", "Mobile Application Development", "Big Data Analytics", "Elective I"],
            "SEM VII":  ["Deep Learning", "IoT Systems", "Data Science", "Blockchain Technology", "Project I"],
            "SEM VIII": ["Major Project", "Professional Ethics", "Open Elective"],
        }
    },
    "IT": {
        "name": "Information Technology",
        "semesters": {
            "SEM I":    ["Engineering Mathematics I", "Engineering Physics", "C Programming", "Engineering Drawing"],
            "SEM II":   ["Engineering Mathematics II", "Data Structures", "Digital Electronics", "Environmental Studies"],
            "SEM III":  ["Object Oriented Programming", "Database Management Systems", "Computer Networks", "Discrete Mathematics"],
            "SEM IV":   ["Operating Systems", "Software Engineering", "Web Programming", "Theory of Computation"],
            "SEM V":    ["Cyber Security", "Python Programming", "Artificial Intelligence", "Cloud Computing"],
            "SEM VI":   ["Mobile Computing", "Software Testing", "Blockchain", "Natural Language Processing"],
            "SEM VII":  ["Data Analytics", "DevOps", "Information Systems Management", "Project I"],
            "SEM VIII": ["Major Project", "Professional Ethics", "Open Elective"],
        }
    },
    "ECE": {
        "name": "Electronics and Communication Engineering",
        "semesters": {
            "SEM I":    ["Engineering Mathematics I", "Engineering Physics", "C Programming", "Engineering Drawing", "Basic Electrical Circuits"],
            "SEM II":   ["Engineering Mathematics II", "Electronic Devices and Circuits", "Digital Electronics", "Environmental Studies"],
            "SEM III":  ["Signals and Systems", "Analog Circuits", "Engineering Mathematics III", "Network Theory", "Electronic Measurements"],
            "SEM IV":   ["Analog Communication", "Digital Communication", "Microcontrollers", "Electromagnetic Theory", "Linear Integrated Circuits"],
            "SEM V":    ["Wireless Communication", "VLSI Design", "Embedded Systems", "Antenna and Wave Propagation", "Digital Signal Processing"],
            "SEM VI":   ["Optical Fiber Communication", "Mobile Communication", "Control Systems", "Satellite Communication", "Elective I"],
            "SEM VII":  ["5G Networks", "IoT and Applications", "Signal Processing Applications", "Project I", "Elective II"],
            "SEM VIII": ["Major Project", "Professional Ethics", "Open Elective"],
        }
    },
    "EE": {
        "name": "Electrical Engineering",
        "semesters": {
            "SEM I":    ["Engineering Mathematics I", "Engineering Physics", "C Programming", "Engineering Drawing", "Basic Electrical Engineering"],
            "SEM II":   ["Engineering Mathematics II", "Network Analysis", "Electronic Devices", "Environmental Studies"],
            "SEM III":  ["Electrical Machines I", "Signals and Systems", "Power Systems I", "Control Systems", "Engineering Mathematics III"],
            "SEM IV":   ["Electrical Machines II", "Power Electronics", "Measurement and Instrumentation", "Power Systems II"],
            "SEM V":    ["Microprocessors and Applications", "Electric Drives", "High Voltage Engineering", "Switch Gear and Protection"],
            "SEM VI":   ["Power System Operation and Control", "Utilization of Electrical Power", "Renewable Energy Systems", "Industrial Automation"],
            "SEM VII":  ["Smart Grid Technology", "HVDC Transmission", "Project I", "Elective I"],
            "SEM VIII": ["Major Project", "Professional Ethics", "Open Elective"],
        }
    },
    "ME": {
        "name": "Mechanical Engineering",
        "semesters": {
            "SEM I":    ["Engineering Mathematics I", "Engineering Physics", "Engineering Drawing", "Basic Electrical Engineering", "Manufacturing Processes"],
            "SEM II":   ["Engineering Mathematics II", "Engineering Mechanics", "Material Science", "Environmental Studies"],
            "SEM III":  ["Thermodynamics", "Strength of Materials", "Fluid Mechanics", "Engineering Mathematics III", "Theory of Machines"],
            "SEM IV":   ["Heat Transfer", "Machine Design", "Manufacturing Technology", "Metrology and Quality Control"],
            "SEM V":    ["Internal Combustion Engines", "CAD/CAM", "Industrial Engineering", "Refrigeration and Air Conditioning"],
            "SEM VI":   ["Finite Element Analysis", "Robotics and Automation", "Power Plant Engineering", "Operations Research"],
            "SEM VII":  ["Mechatronics", "Automobile Engineering", "Project I", "Elective I"],
            "SEM VIII": ["Major Project", "Professional Ethics", "Open Elective"],
        }
    },
    "CE": {
        "name": "Civil Engineering",
        "semesters": {
            "SEM I":    ["Engineering Mathematics I", "Engineering Physics", "Engineering Drawing", "Basic Electrical Engineering", "Building Materials"],
            "SEM II":   ["Engineering Mathematics II", "Engineering Mechanics", "Surveying I", "Environmental Studies"],
            "SEM III":  ["Structural Analysis I", "Fluid Mechanics", "Soil Mechanics", "Engineering Geology", "Engineering Mathematics III"],
            "SEM IV":   ["Structural Analysis II", "Concrete Technology", "Hydraulics", "Transportation Engineering", "Geotechnical Engineering"],
            "SEM V":    ["Design of Reinforced Concrete Structures", "Water Supply Engineering", "Environmental Engineering", "Foundation Engineering"],
            "SEM VI":   ["Design of Steel Structures", "Project Management", "Quantity Surveying", "Remote Sensing and GIS"],
            "SEM VII":  ["Construction Management", "Bridge Engineering", "Project I", "Elective I"],
            "SEM VIII": ["Major Project", "Professional Ethics", "Open Elective"],
        }
    },
    "AIML": {
        "name": "Artificial Intelligence and Machine Learning",
        "semesters": {
            "SEM I":    ["Engineering Mathematics I", "Programming in Python", "Introduction to AI", "Engineering Physics"],
            "SEM II":   ["Engineering Mathematics II", "Data Structures", "Probability and Statistics", "Digital Electronics"],
            "SEM III":  ["Machine Learning", "Database Systems", "Computer Vision Fundamentals", "Linear Algebra for AI"],
            "SEM IV":   ["Deep Learning", "Natural Language Processing", "Big Data Technologies", "Reinforcement Learning"],
            "SEM V":    ["Computer Vision", "AI Ethics", "Cloud for AI", "Time Series Analysis"],
            "SEM VI":   ["Generative AI", "MLOps", "AI for Healthcare", "Elective I"],
            "SEM VII":  ["Applied AI Projects", "AI in Industry 4.0", "Project I", "Elective II"],
            "SEM VIII": ["Major Project", "Professional Ethics", "Startup Essentials"],
        }
    },
    "DS": {
        "name": "Data Science",
        "semesters": {
            "SEM I":    ["Engineering Mathematics I", "Programming in Python", "Statistics I", "Introduction to Data Science"],
            "SEM II":   ["Engineering Mathematics II", "Data Structures", "Statistics II", "Database Management Systems"],
            "SEM III":  ["Machine Learning", "Data Visualization", "Big Data Analytics", "Probability and Random Processes"],
            "SEM IV":   ["Deep Learning", "Natural Language Processing", "Data Engineering", "Business Intelligence"],
            "SEM V":    ["Computer Vision", "Time Series Analysis", "Cloud Data Platforms", "AI Ethics"],
            "SEM VI":   ["Generative Models", "MLOps", "Recommendation Systems", "Elective I"],
            "SEM VII":  ["Applied Data Science", "Real-time Analytics", "Project I", "Elective II"],
            "SEM VIII": ["Major Project", "Data Science Capstone", "Open Elective"],
        }
    },
    "CHEM": {
        "name": "Chemical Engineering",
        "semesters": {
            "SEM I":    ["Engineering Mathematics I", "Engineering Chemistry", "Engineering Drawing", "Basic Electrical Engineering"],
            "SEM II":   ["Engineering Mathematics II", "Organic Chemistry", "Environmental Studies", "Material Science"],
            "SEM III":  ["Fluid Mechanics", "Chemical Thermodynamics", "Mass Transfer I", "Engineering Mathematics III"],
            "SEM IV":   ["Heat Transfer", "Chemical Reaction Engineering I", "Mass Transfer II", "Instrumental Analysis"],
            "SEM V":    ["Process Control", "Chemical Reaction Engineering II", "Plant Design", "Petroleum Refining"],
            "SEM VI":   ["Transport Phenomena", "Biochemical Engineering", "Safety Engineering", "Elective I"],
            "SEM VII":  ["Process Simulation", "Polymer Technology", "Project I", "Elective II"],
            "SEM VIII": ["Major Project", "Professional Ethics", "Open Elective"],
        }
    },
}

UNIVERSITIES = [
    ("Indian Institute of Technology Bombay",            "Mumbai, Maharashtra",             ["CSE", "IT", "EE", "ME", "CE", "CHEM", "AIML"]),
    ("Indian Institute of Technology Delhi",             "New Delhi",                       ["CSE", "IT", "EE", "ME", "CE", "CHEM", "AIML", "DS"]),
    ("Indian Institute of Technology Madras",            "Chennai, Tamil Nadu",             ["CSE", "EE", "ME", "CE", "CHEM", "AIML"]),
    ("Indian Institute of Technology Kanpur",            "Kanpur, Uttar Pradesh",           ["CSE", "EE", "ME", "CE", "CHEM"]),
    ("Indian Institute of Technology Kharagpur",         "Kharagpur, West Bengal",          ["CSE", "IT", "EE", "ME", "CE", "CHEM"]),
    ("Indian Institute of Technology Roorkee",           "Roorkee, Uttarakhand",            ["CSE", "IT", "EE", "ME", "CE", "CHEM"]),
    ("Indian Institute of Technology Guwahati",          "Guwahati, Assam",                 ["CSE", "EE", "ME", "CE", "CHEM"]),
    ("Indian Institute of Technology Hyderabad",         "Hyderabad, Telangana",            ["CSE", "EE", "ME", "CE", "AIML"]),
    ("Indian Institute of Technology Gandhinagar",       "Gandhinagar, Gujarat",            ["CSE", "ME", "CE"]),
    ("Indian Institute of Technology Jodhpur",           "Jodhpur, Rajasthan",              ["CSE", "EE", "ME"]),
    ("Indian Institute of Technology Patna",             "Patna, Bihar",                    ["CSE", "EE", "ME", "CE"]),
    ("Indian Institute of Technology Ropar",             "Rupnagar, Punjab",                ["CSE", "EE", "ME", "CE"]),
    ("Indian Institute of Technology Bhubaneswar",       "Bhubaneswar, Odisha",             ["CSE", "EE", "ME", "CE"]),
    ("Indian Institute of Technology Indore",            "Indore, Madhya Pradesh",          ["CSE", "EE", "ME"]),
    ("Indian Institute of Technology Mandi",             "Mandi, Himachal Pradesh",         ["CSE", "EE", "ME", "CE"]),
    ("Indian Institute of Technology (BHU) Varanasi",   "Varanasi, Uttar Pradesh",         ["CSE", "EE", "ME", "CE", "CHEM"]),
    ("Indian Institute of Technology Palakkad",          "Palakkad, Kerala",                ["CSE", "EE", "ME"]),
    ("Indian Institute of Technology Tirupati",          "Tirupati, Andhra Pradesh",        ["CSE", "EE", "ME", "CE"]),
    ("Indian Institute of Technology (ISM) Dhanbad",    "Dhanbad, Jharkhand",              ["CSE", "EE", "ME", "CE", "CHEM"]),
    ("Indian Institute of Technology Bhilai",            "Bhilai, Chhattisgarh",            ["CSE", "EE", "ME"]),
    ("Indian Institute of Technology Goa",               "Goa",                             ["CSE", "ME"]),
    ("Indian Institute of Technology Jammu",             "Jammu, J&K",                      ["CSE", "EE", "ME"]),
    ("Indian Institute of Technology Dharwad",           "Dharwad, Karnataka",              ["CSE", "EE", "ME"]),
    ("National Institute of Technology Tiruchirappalli",          "Tiruchirappalli, Tamil Nadu",          ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("National Institute of Technology Warangal",                 "Warangal, Telangana",                  ["CSE", "IT", "ECE", "EE", "ME", "CE", "CHEM"]),
    ("National Institute of Technology Karnataka Surathkal",      "Mangaluru, Karnataka",                 ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("National Institute of Technology Calicut",                  "Calicut, Kerala",                      ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Motilal Nehru National Institute of Technology Allahabad",  "Allahabad, Uttar Pradesh",             ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Visvesvaraya National Institute of Technology Nagpur",      "Nagpur, Maharashtra",                  ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Malaviya National Institute of Technology Jaipur",          "Jaipur, Rajasthan",                    ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Maulana Azad National Institute of Technology Bhopal",      "Bhopal, Madhya Pradesh",               ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("National Institute of Technology Rourkela",                 "Rourkela, Odisha",                     ["CSE", "IT", "ECE", "EE", "ME", "CE", "CHEM"]),
    ("National Institute of Technology Durgapur",                 "Durgapur, West Bengal",                ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Sardar Vallabhbhai National Institute of Technology Surat", "Surat, Gujarat",                       ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Dr. B.R. Ambedkar National Institute of Technology Jalandhar", "Jalandhar, Punjab",                ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("National Institute of Technology Kurukshetra",              "Kurukshetra, Haryana",                 ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("National Institute of Technology Silchar",                  "Silchar, Assam",                       ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("National Institute of Technology Hamirpur",                 "Hamirpur, Himachal Pradesh",           ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("National Institute of Technology Srinagar",                 "Srinagar, J&K",                        ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("National Institute of Technology Uttarakhand",              "Srinagar Garhwal, Uttarakhand",        ["CSE", "ECE", "ME", "CE"]),
    ("National Institute of Technology Puducherry",               "Karaikal, Puducherry",                 ["CSE", "ECE", "EE", "ME"]),
    ("National Institute of Technology Arunachal Pradesh",        "Yupia, Arunachal Pradesh",             ["CSE", "ECE", "EE", "ME", "CE"]),
    ("National Institute of Technology Goa",                      "Farmagudi, Goa",                       ["CSE", "ECE", "EE", "ME", "CE"]),
    ("National Institute of Technology Manipur",                  "Imphal, Manipur",                      ["CSE", "ECE", "EE", "ME", "CE"]),
    ("National Institute of Technology Meghalaya",                "Shillong, Meghalaya",                  ["CSE", "ECE", "EE", "ME", "CE"]),
    ("National Institute of Technology Mizoram",                  "Aizawl, Mizoram",                      ["CSE", "ECE", "EE", "ME"]),
    ("National Institute of Technology Nagaland",                 "Dimapur, Nagaland",                    ["CSE", "ECE", "EE", "ME"]),
    ("National Institute of Technology Delhi",                    "Delhi",                                 ["CSE", "IT", "ECE", "EE", "ME"]),
    ("National Institute of Technology Sikkim",                   "Ravangla, Sikkim",                     ["CSE", "ECE", "EE", "ME", "CE"]),
    ("National Institute of Technology Andhra Pradesh",           "Tadepalligudem, Andhra Pradesh",       ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("National Institute of Technology Agartala",                 "Agartala, Tripura",                    ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("National Institute of Technology Patna",                    "Patna, Bihar",                         ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("National Institute of Technology Raipur",                   "Raipur, Chhattisgarh",                 ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("National Institute of Technology Jamshedpur",               "Jamshedpur, Jharkhand",                ["CSE", "IT", "ME", "CE", "CHEM"]),
    ("Indian Institute of Information Technology Allahabad",        "Allahabad, Uttar Pradesh",    ["CSE", "IT", "AIML", "DS"]),
    ("International Institute of Information Technology Hyderabad", "Hyderabad, Telangana",        ["CSE", "ECE", "AIML", "DS"]),
    ("International Institute of Information Technology Bangalore", "Bangalore, Karnataka",         ["CSE", "IT", "AIML"]),
    ("Indraprastha Institute of Information Technology Delhi",      "Delhi",                        ["CSE", "IT", "ECE", "AIML", "DS"]),
    ("IIIT Gwalior (ABV-IIITM)",                                    "Gwalior, Madhya Pradesh",     ["CSE", "IT", "AIML"]),
    ("Indian Institute of Information Technology Kancheepuram",    "Chennai, Tamil Nadu",          ["CSE", "IT"]),
    ("Indian Institute of Information Technology Kottayam",         "Kottayam, Kerala",            ["CSE", "ECE"]),
    ("Indian Institute of Information Technology Sri City",         "Chittoor, Andhra Pradesh",    ["CSE", "ECE"]),
    ("Indian Institute of Information Technology Vadodara",         "Vadodara, Gujarat",           ["CSE", "IT"]),
    ("Indian Institute of Information Technology Pune",             "Pune, Maharashtra",           ["CSE", "IT", "AIML"]),
    ("Indian Institute of Information Technology Ranchi",           "Ranchi, Jharkhand",           ["CSE", "ECE"]),
    ("Indian Institute of Information Technology Nagpur",           "Nagpur, Maharashtra",         ["CSE", "IT"]),
    ("Indian Institute of Information Technology Naya Raipur",      "Raipur, Chhattisgarh",       ["CSE", "IT", "AIML"]),
    ("Indian Institute of Information Technology Una",              "Una, Himachal Pradesh",       ["CSE", "ECE"]),
    ("Indian Institute of Information Technology Kalyani",          "Kalyani, West Bengal",        ["CSE", "ECE"]),
    ("Indian Institute of Information Technology Bhagalpur",        "Bhagalpur, Bihar",            ["CSE", "ECE"]),
    ("Indian Institute of Information Technology Manipur",          "Imphal, Manipur",             ["CSE", "ECE"]),
    ("Indian Institute of Information Technology Agartala",         "Agartala, Tripura",           ["CSE", "IT"]),
    ("Indian Institute of Information Technology Surat",            "Surat, Gujarat",              ["CSE", "ECE"]),
    ("Indian Institute of Information Technology Dharwad",          "Dharwad, Karnataka",          ["CSE", "ECE"]),
    ("Indian Institute of Information Technology Kurnool",          "Kurnool, Andhra Pradesh",     ["CSE", "ECE"]),
    ("Indian Institute of Information Technology Lucknow",          "Lucknow, Uttar Pradesh",      ["CSE", "IT", "AIML"]),
    ("Indian Institute of Information Technology Raichur",          "Raichur, Karnataka",          ["CSE", "ECE"]),
    ("Indian Institute of Information Technology Sonepat",          "Sonepat, Haryana",            ["CSE", "IT"]),
    ("Indian Institute of Information Technology Bhopal",           "Bhopal, Madhya Pradesh",      ["CSE", "IT"]),
    ("Birla Institute of Technology and Science Pilani",            "Pilani, Rajasthan",           ["CSE", "IT", "ECE", "EE", "ME", "CHEM"]),
    ("BITS Pilani - Hyderabad Campus",                              "Hyderabad, Telangana",        ["CSE", "IT", "ECE", "EE", "ME", "CHEM"]),
    ("BITS Pilani - Goa Campus",                                    "Goa",                         ["CSE", "IT", "ECE", "EE", "ME"]),
    ("VIT University Vellore",                                      "Vellore, Tamil Nadu",         ["CSE", "IT", "ECE", "EE", "ME", "CE", "AIML", "DS"]),
    ("VIT Chennai",                                                 "Chennai, Tamil Nadu",         ["CSE", "IT", "ECE", "EE", "ME"]),
    ("VIT AP University",                                           "Amaravati, Andhra Pradesh",   ["CSE", "ECE", "EE", "ME", "AIML"]),
    ("VIT Bhopal",                                                  "Bhopal, Madhya Pradesh",      ["CSE", "IT", "ECE", "ME"]),
    ("Manipal Institute of Technology",                             "Manipal, Karnataka",          ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Manipal University Jaipur",                                   "Jaipur, Rajasthan",           ["CSE", "IT", "ECE", "ME"]),
    ("Amity University Noida",                                      "Noida, Uttar Pradesh",        ["CSE", "IT", "ECE", "EE", "ME", "AIML", "DS"]),
    ("Amity University Mumbai",                                     "Mumbai, Maharashtra",         ["CSE", "IT", "ECE", "ME"]),
    ("SRM Institute of Science and Technology",                     "Chennai, Tamil Nadu",         ["CSE", "IT", "ECE", "EE", "ME", "CE", "AIML"]),
    ("SRM University AP",                                           "Amaravati, Andhra Pradesh",   ["CSE", "IT", "ECE", "EE", "ME"]),
    ("SRM University Delhi-NCR",                                    "Sonepat, Haryana",            ["CSE", "IT", "ECE", "ME"]),
    ("Thapar Institute of Engineering and Technology",              "Patiala, Punjab",             ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Symbiosis Institute of Technology Pune",                      "Pune, Maharashtra",           ["CSE", "IT", "ECE", "ME", "AIML"]),
    ("Lovely Professional University",                              "Phagwara, Punjab",            ["CSE", "IT", "ECE", "EE", "ME", "CE", "AIML"]),
    ("Chandigarh University",                                       "Mohali, Punjab",              ["CSE", "IT", "ECE", "EE", "ME", "CE", "AIML"]),
    ("Shiv Nadar University",                                       "Greater Noida, Uttar Pradesh", ["CSE", "ECE", "EE", "AIML"]),
    ("Kalinga Institute of Industrial Technology",                  "Bhubaneswar, Odisha",         ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("SASTRA Deemed University",                                    "Thanjavur, Tamil Nadu",       ["CSE", "IT", "ECE", "ME", "CE"]),
    ("PSG College of Technology",                                   "Coimbatore, Tamil Nadu",      ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("RV College of Engineering",                                   "Bangalore, Karnataka",        ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("PES University",                                              "Bangalore, Karnataka",        ["CSE", "IT", "ECE", "EE", "ME"]),
    ("Dhirubhai Ambani Institute of ICT",                           "Gandhinagar, Gujarat",        ["CSE", "IT", "ECE"]),
    ("Nirma University",                                            "Ahmedabad, Gujarat",          ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Graphic Era University",                                      "Dehradun, Uttarakhand",       ["CSE", "IT", "ECE", "ME"]),
    ("Bennett University",                                          "Greater Noida, Uttar Pradesh", ["CSE", "IT", "ECE", "AIML"]),
    ("MIT Pune (Maharashtra Institute of Technology)",              "Pune, Maharashtra",           ["CSE", "IT", "ME", "CE"]),
    ("D.Y. Patil University Pune",                                  "Pune, Maharashtra",           ["CSE", "IT", "ME", "CE"]),
    ("GITAM University",                                            "Visakhapatnam, Andhra Pradesh", ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Koneru Lakshmaiah Education Foundation",                      "Vijayawada, Andhra Pradesh",  ["CSE", "IT", "ECE", "ME"]),
    ("Chitkara University",                                         "Rajpura, Punjab",             ["CSE", "IT", "ECE", "ME"]),
    ("BML Munjal University",                                       "Gurgaon, Haryana",            ["CSE", "IT", "ECE", "ME"]),
    ("Vel Tech University",                                         "Chennai, Tamil Nadu",         ["CSE", "IT", "ECE", "ME"]),
    ("Jain University",                                             "Bangalore, Karnataka",        ["CSE", "IT", "ECE", "ME"]),
    ("Presidency University Bangalore",                             "Bangalore, Karnataka",        ["CSE", "IT", "ECE", "ME"]),
    ("Alliance University",                                         "Bangalore, Karnataka",        ["CSE", "IT", "ME"]),
    ("Woxsen University",                                           "Hyderabad, Telangana",        ["CSE", "AIML", "DS"]),
    ("Annamalai University",                                        "Chidambaram, Tamil Nadu",     ["CSE", "IT", "ECE", "ME", "CE"]),
    ("Cochin University of Science and Technology",                 "Kochi, Kerala",               ["CSE", "IT", "ECE", "EE", "ME"]),
    ("Jadavpur University",                                         "Kolkata, West Bengal",        ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Anna University",                                     "Chennai, Tamil Nadu",             ["CSE", "IT", "ECE", "EE", "ME", "CE", "CHEM"]),
    ("Visvesvaraya Technological University",               "Belagavi, Karnataka",             ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Dr. A.P.J. Abdul Kalam Technical University",        "Lucknow, Uttar Pradesh",          ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Gujarat Technological University",                   "Ahmedabad, Gujarat",              ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Rajasthan Technical University",                     "Kota, Rajasthan",                 ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("APJ Abdul Kalam Technological University",           "Thiruvananthapuram, Kerala",      ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Biju Patnaik University of Technology",              "Rourkela, Odisha",                ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Jawaharlal Nehru Technological University Hyderabad","Hyderabad, Telangana",            ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("JNTU Kakinada",                                      "Kakinada, Andhra Pradesh",        ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("JNTU Anantapur",                                     "Anantapur, Andhra Pradesh",       ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Maulana Abul Kalam Azad University of Technology",   "Kolkata, West Bengal",            ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Punjab Technical University",                        "Jalandhar, Punjab",               ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("RTM Nagpur University",                              "Nagpur, Maharashtra",             ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Dr. Babasaheb Ambedkar Technological University",    "Lonere, Maharashtra",             ["CSE", "ME", "CE", "CHEM"]),
    ("Chhattisgarh Swami Vivekanand Technical University","Bhilai, Chhattisgarh",            ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Jharkhand University of Technology",                 "Ranchi, Jharkhand",               ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Madhya Pradesh Technical University",                "Bhopal, Madhya Pradesh",          ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Uttarakhand Technical University",                   "Dehradun, Uttarakhand",           ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Himachal Pradesh Technical University",              "Hamirpur, Himachal Pradesh",      ["CSE", "IT", "ECE", "EE", "ME"]),
    ("Aryabhatta Knowledge University",                    "Patna, Bihar",                    ["CSE", "IT", "ECE", "EE", "ME"]),
    ("Delhi Technological University",                     "Delhi",                           ["CSE", "IT", "ECE", "EE", "ME", "CE", "AIML"]),
    ("Netaji Subhas University of Technology",             "Delhi",                           ["CSE", "IT", "ECE", "EE", "ME"]),
    ("Indira Gandhi Delhi Technical University for Women", "Delhi",                           ["CSE", "IT", "ECE", "EE", "ME"]),
    ("Guru Gobind Singh Indraprastha University",          "Delhi",                           ["CSE", "IT", "ECE", "EE", "ME"]),
    ("Indian Institute of Engineering Science and Technology Shibpur", "Howrah, West Bengal", ["CSE", "IT", "EE", "ME", "CE"]),
    ("Bikaner Technical University",                       "Bikaner, Rajasthan",              ["CSE", "IT", "ECE", "ME"]),
    ("University of Mumbai",                     "Mumbai, Maharashtra",    ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Savitribai Phule Pune University",         "Pune, Maharashtra",      ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Amravati University",                      "Amravati, Maharashtra",  ["CSE", "IT", "ME", "CE"]),
    ("Shivaji University Kolhapur",              "Kolhapur, Maharashtra",  ["CSE", "IT", "ME", "CE"]),
    ("Solapur University",                       "Solapur, Maharashtra",   ["CSE", "ME", "CE"]),
    ("North Maharashtra University",             "Jalgaon, Maharashtra",   ["CSE", "ME"]),
    ("Dr. Babasaheb Ambedkar Marathwada University", "Aurangabad, Maharashtra", ["CSE", "IT", "ME"]),
    ("Swami Ramanand Teerth Marathwada University",  "Nanded, Maharashtra",    ["CSE", "ME", "CE"]),
    ("Bangalore University",                     "Bangalore, Karnataka",   ["CSE", "IT", "ECE"]),
    ("Kuvempu University",                       "Shivamogga, Karnataka",  ["CSE", "IT"]),
    ("Mysore University",                        "Mysuru, Karnataka",      ["CSE", "IT"]),
    ("Gulbarga University",                      "Kalaburagi, Karnataka",  ["CSE", "IT"]),
    ("Mangalore University",                     "Mangaluru, Karnataka",   ["CSE", "IT", "ECE"]),
    ("Davangere University",                     "Davangere, Karnataka",   ["CSE"]),
    ("Rani Channamma University",                "Belagavi, Karnataka",    ["CSE", "IT"]),
    ("Tumkur University",                        "Tumakuru, Karnataka",    ["CSE"]),
    ("Periyar University",                       "Salem, Tamil Nadu",      ["CSE", "IT"]),
    ("Alagappa University",                      "Karaikudi, Tamil Nadu",  ["CSE", "IT"]),
    ("Bharathidasan University",                 "Tiruchirappalli, Tamil Nadu", ["CSE", "IT"]),
    ("Bharathiar University",                    "Coimbatore, Tamil Nadu", ["CSE", "IT"]),
    ("Madurai Kamaraj University",               "Madurai, Tamil Nadu",    ["CSE", "IT"]),
    ("Andhra University",                        "Visakhapatnam, Andhra Pradesh", ["CSE", "ECE", "EE", "ME", "CE"]),
    ("Sri Venkateswara University",              "Tirupati, Andhra Pradesh",      ["CSE", "ECE", "ME", "CE"]),
    ("Osmania University",                       "Hyderabad, Telangana",          ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Kakatiya University",                      "Warangal, Telangana",           ["CSE", "IT"]),
    ("University of Hyderabad",                  "Hyderabad, Telangana",          ["CSE", "AIML"]),
    ("University of Kerala",                     "Thiruvananthapuram, Kerala",    ["CSE", "IT", "ECE"]),
    ("Kannur University",                        "Kannur, Kerala",                ["CSE", "IT"]),
    ("Calicut University",                       "Malappuram, Kerala",            ["CSE", "IT", "ECE"]),
    ("Mahatma Gandhi University",                "Kottayam, Kerala",              ["CSE", "ECE"]),
    ("Gujarat University",                       "Ahmedabad, Gujarat",    ["CSE", "IT"]),
    ("M.S. University of Baroda",               "Vadodara, Gujarat",     ["CSE", "IT", "ME"]),
    ("Saurashtra University",                    "Rajkot, Gujarat",       ["CSE", "IT"]),
    ("South Gujarat University (Veer Narmad)",  "Surat, Gujarat",        ["CSE", "IT"]),
    ("Sardar Patel University",                  "Anand, Gujarat",        ["CSE", "IT"]),
    ("University of Rajasthan",                  "Jaipur, Rajasthan",     ["CSE", "IT"]),
    ("MDS University Ajmer",                     "Ajmer, Rajasthan",      ["CSE", "IT"]),
    ("University of Kota",                       "Kota, Rajasthan",       ["CSE", "IT"]),
    ("Aligarh Muslim University",                "Aligarh, Uttar Pradesh",       ["CSE", "IT", "ECE", "EE", "ME", "CE"]),
    ("Banaras Hindu University",                 "Varanasi, Uttar Pradesh",      ["CSE", "ECE", "ME", "CE"]),
    ("University of Allahabad",                  "Allahabad, Uttar Pradesh",     ["CSE", "IT"]),
    ("Lucknow University",                       "Lucknow, Uttar Pradesh",       ["CSE", "IT"]),
    ("Bundelkhand University",                   "Jhansi, Uttar Pradesh",        ["CSE", "IT"]),
    ("Mahatma Jyotiba Phule Rohilkhand University", "Bareilly, Uttar Pradesh",  ["CSE", "IT"]),
    ("Jamia Millia Islamia",                     "Delhi",                  ["CSE", "IT", "ECE", "ME"]),
    ("Guru Gobind Singh College Of Engineering And Research Centre", "Nashik, Maharashtra", ["CSE", "IT", "ME", "ECE"]),
    ("Punjab University Chandigarh",             "Chandigarh",            ["CSE", "IT", "ECE", "ME"]),
    ("Kurukshetra University",                   "Kurukshetra, Haryana",  ["CSE", "IT", "ECE", "ME"]),
    ("Maharshi Dayanand University",             "Rohtak, Haryana",       ["CSE", "IT", "ECE", "ME"]),
    ("Guru Jambheshwar University",              "Hisar, Haryana",        ["CSE", "IT"]),
    ("Chaudhary Devi Lal University",            "Sirsa, Haryana",        ["CSE"]),
    ("Himachal Pradesh University",              "Shimla, Himachal Pradesh", ["CSE", "IT"]),
    ("Jammu University",                         "Jammu, J&K",            ["CSE", "IT"]),
    ("Kashmir University",                       "Srinagar, J&K",         ["CSE", "IT"]),
    ("Devi Ahilya Vishwavidyalaya",              "Indore, Madhya Pradesh",  ["CSE", "IT", "ECE"]),
    ("Barkatullah University",                   "Bhopal, Madhya Pradesh",  ["CSE", "IT"]),
    ("Jiwaji University",                        "Gwalior, Madhya Pradesh", ["CSE", "IT"]),
    ("Rani Durgavati University",                "Jabalpur, Madhya Pradesh", ["CSE"]),
    ("Vikram University",                        "Ujjain, Madhya Pradesh",  ["CSE"]),
    ("Jodhpur National University",              "Jodhpur, Rajasthan",     ["CSE", "IT"]),
    ("Magadh University",                        "Bodh Gaya, Bihar",       ["CSE"]),
    ("Lalit Narayan Mithila University",         "Darbhanga, Bihar",       ["CSE"]),
    ("Veer Kunwar Singh University",             "Ara, Bihar",             ["CSE", "IT"]),
    ("Ranchi University",                        "Ranchi, Jharkhand",      ["CSE", "IT"]),
    ("Vinoba Bhave University",                  "Hazaribagh, Jharkhand",  ["CSE", "IT"]),
    ("Kolhan University",                        "Chaibasa, Jharkhand",    ["CSE"]),
    ("Guru Ghasidas Vishwavidyalaya",            "Bilaspur, Chhattisgarh", ["CSE", "IT"]),
    ("Sambalpur University",                     "Sambalpur, Odisha",      ["CSE", "IT"]),
    ("Berhampur University",                     "Brahmapur, Odisha",      ["CSE"]),
    ("North Orissa University",                  "Baripada, Odisha",       ["CSE"]),
    ("Utkal University",                         "Bhubaneswar, Odisha",    ["CSE", "IT"]),
    ("Fakir Mohan University",                   "Balasore, Odisha",       ["CSE"]),
    ("Calcutta University",                      "Kolkata, West Bengal",   ["CSE", "IT", "ECE"]),
    ("Tezpur University",                        "Tezpur, Assam",          ["CSE", "ECE", "EE", "ME"]),
    ("Gauhati University",                       "Guwahati, Assam",        ["CSE", "IT", "ECE"]),
    ("Dibrugarh University",                     "Dibrugarh, Assam",       ["CSE", "IT"]),
    ("Cotton University",                        "Guwahati, Assam",        ["CSE"]),
    ("Assam University",                         "Silchar, Assam",         ["CSE", "ECE"]),
    ("Bodoland University",                      "Kokrajhar, Assam",       ["CSE"]),
    ("Nagaland University",                      "Kohima, Nagaland",       ["CSE"]),
    ("Manipur University",                       "Imphal, Manipur",        ["CSE", "IT"]),
    ("Mizoram University",                       "Aizawl, Mizoram",        ["CSE"]),
    ("Tripura University",                       "Agartala, Tripura",      ["CSE", "IT"]),
    ("North-Eastern Hill University",            "Shillong, Meghalaya",    ["CSE"]),
    ("Rajiv Gandhi University",                  "Itanagar, Arunachal Pradesh", ["CSE"]),
    ("Sikkim University",                        "Gangtok, Sikkim",        ["CSE"]),
    ("Hemvati Nandan Bahuguna Garhwal University","Srinagar Garhwal, Uttarakhand", ["CSE", "IT"]),
    ("Kumaun University",                        "Nainital, Uttarakhand",  ["CSE"]),
    ("Gurukul Kangri University",                "Haridwar, Uttarakhand",  ["CSE", "IT"]),
    ("Pondicherry University",                   "Puducherry",             ["CSE", "IT", "ECE", "EE", "ME"]),
]


class Command(BaseCommand):
    help = 'Populate database with Indian universities, branches and subjects using bulk operations'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing data before seeding')

    def handle(self, *args, **options):
        if not options.get('clear') and College.objects.exists():
            self.stdout.write(self.style.SUCCESS(
                f'Already seeded: {College.objects.count()} colleges | '
                f'{Branch.objects.count()} branches | {Subject.objects.count()} subjects'
            ))
            return

        if options.get('clear'):
            Subject.objects.all().delete()
            Branch.objects.all().delete()
            College.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared existing data.'))

        # ── Step 1: bulk create colleges ──────────────────────────────────────
        college_data = {name: loc for name, loc, _ in UNIVERSITIES}
        College.objects.bulk_create(
            [College(name=name, location=loc) for name, loc in college_data.items()],
            ignore_conflicts=True,
        )
        college_map = {c.name: c for c in College.objects.filter(name__in=college_data.keys())}
        self.stdout.write(f'Colleges: {len(college_map)}')

        # ── Step 2: bulk create branches ──────────────────────────────────────
        branches_to_create = []
        for college_name, _loc, branch_codes in UNIVERSITIES:
            college = college_map.get(college_name)
            if not college:
                continue
            if isinstance(branch_codes, str):
                branch_codes = [branch_codes]
            for code in branch_codes:
                template = BRANCH_TEMPLATES.get(code)
                if template:
                    branches_to_create.append(Branch(college=college, name=template['name']))

        Branch.objects.bulk_create(branches_to_create, ignore_conflicts=True)
        branch_map = {}
        for b in Branch.objects.filter(college__in=college_map.values()):
            branch_map[(b.college_id, b.name)] = b
        self.stdout.write(f'Branches: {len(branch_map)}')

        # ── Step 3: bulk create subjects in batches of 500 ───────────────────
        subjects_to_create = []
        for college_name, _loc, branch_codes in UNIVERSITIES:
            college = college_map.get(college_name)
            if not college:
                continue
            if isinstance(branch_codes, str):
                branch_codes = [branch_codes]
            for code in branch_codes:
                template = BRANCH_TEMPLATES.get(code)
                if not template:
                    continue
                branch = branch_map.get((college.id, template['name']))
                if not branch:
                    continue
                for semester, subject_list in template['semesters'].items():
                    for subject_name in subject_list:
                        subjects_to_create.append(Subject(
                            branch=branch, name=subject_name, semester=semester,
                        ))

        batch_size = 500
        for i in range(0, len(subjects_to_create), batch_size):
            Subject.objects.bulk_create(subjects_to_create[i:i + batch_size], ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS(
            f'\nDone!  {College.objects.count()} universities  |  '
            f'{Branch.objects.count()} branches  |  '
            f'{Subject.objects.count()} subjects'
        ))
