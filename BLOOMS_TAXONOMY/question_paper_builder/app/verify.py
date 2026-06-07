import re

####################################    User Authentication Function   #####################################

def name_valid(name):
    if name.isalpha() and len(name) > 2:
        return True
    else:
        return False

def password_valid(pass1):
    reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
	
	# compiling regex
    pat = re.compile(reg)
	
	# searching regex				
    mat = re.search(pat, pass1)
	
	# validating conditions
    if mat:
        return True
    else:
        return False

def password_check(password1, password2):
    if password1 == password2:
        return True
    else : 
        return False

def contact_valid(number):
    Pattern = re.fullmatch("[6-9][0-9]{9}",number)
    if Pattern != None:
        return True
    else:
        return False

def authentication(first_name, last_name, pass1, pass2):
    if name_valid(first_name) == False:
        return "Invalid First Name"           
    elif name_valid(last_name) == False:
            return "Invalid Last Name"
    elif password_valid(pass1) == False:
        return "Password Should be in Proper Format. (eg. Password@1234)"
    elif password_check(pass1, pass2) == False:
        return "Password Not Matched"
    else:
        return "success"

##################################    Faculty Name Authentication Function   ##################################
def full_name_valid(name):
    allowed = set(' .-,()/')
    return len(name.strip()) > 0 and all(c.isalpha() or c.isspace() or c in allowed for c in name)

def form_varification(name):
    if not full_name_valid(name):
        return "Invalid Faculty Name. Use only letters, spaces, dots or hyphens."
    return "Success"
