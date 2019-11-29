from bs4 import BeautifulSoup as bs
import io,re,os.path
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def opening():
    opening = ''
    breakLine = """_______________________________________________________________________"""
    printInCenter = lambda text : ' '*int((len(breakLine)-len(text))/2) + text
    opening+=breakLine+'\n'
    opening+=printInCenter("Facebook Messenger Extractor") + "\n"
    opening+=printInCenter("Created by David Han ~ 2019") + "\n"
    opening+=breakLine
    return opening

def getMembers():
    allMembers = []
    print( "Input all members in conversation (with proper capitalization) --> ")
    member1 = input('Member 1 Facebook name: ')
    member2 = input("Member 2 Facebook name: ")
    allMembers.append(member1)
    allMembers.append(member2)
    return allMembers

def getThreads(content,members):
    userThread = []
    soup = bs(content,'html.parser')
    text = soup.get_text()
    userThread1 = [m.start() for m in re.finditer(members[0],text)]
    userThread2 = [m.start() for m in re.finditer(members[1],text)]
    userThread = userThread1+userThread2
    userThread.sort()
    allThread = []
    for i in range(len(userThread)-1):
        allThread.append(text[userThread[i]:userThread[i+1]])
    return allThread

def writeFile(allThread,file,members):
    f = open(file,"w")
    singleMessages = []
    for s in allThread:
        name = ""
        date = ""
        message = ""
        if s.find(members[0]) != -1:
            name = s[s.find(members[0]):len(members[0])]
            for month in months:
                if s.find(month)!=-1:
                    date = s[s.find(month):]
                    message = s[s.find(members[0])+len(members[0]):s.find(month)]
                    break
        if s.find(members[1]) != -1:
            name = s[s.find(members[1]):len(members[1])]
            for month in months:
                if s.find(month)!=-1:
                    date = s[s.find(month):]
                    message = s[s.find(members[1])+len(members[1]):s.find(month)]
                    break
        singleMessages.append((name,date,message))
    singleMessages = singleMessages[::-1]
    curName = singleMessages[0][0]
    f.write(curName+'------------------------------\n')
    for tup in singleMessages:
        name,date,message = tup #include date if needed
        if name ==curName:
            try:
                f.write(message+'\n')
            except: f.write("") #deleted message
        else:
            f.write(name+'------------------------------\n')
            try:
                f.write(message+'\n')
            except: f.write("") #deleted message
            curName = name
    f.close()

if __name__ == "__main__":
    print(opening() + "\n")
    sourceFileName = input("Input the location of your messages.html file:\n")
    try:
        with io.open(sourceFileName, 'r',encoding='utf-8') as content_file:
            content = content_file.read()
        print( "Reading file done!")
    except:
        exit("Error: file not found!")
    members = getMembers()

    allThread = getThreads(content,members)
    if len(allThread) == 0:
        print( "Error! Can not find any conversation of above members!")
        exit()
    else:
        outputFile = input("Enter name of output file (with .txt extension): ")
        print("!!SOME CHARACTERS MAY NOT BE ABLE TO BE ENCODED!!")
        writeFile(allThread,outputFile,members)
        print(outputFile, "has been created.")
