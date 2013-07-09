from nltk import ne_chunk,pos_tag,word_tokenize,sent_tokenize,sem
import re

class Doc():
    def __init__(self):
        self.headline = 'doc'
        self.text = ''

TO = re.compile (r'.*\bin\b(?!\b.+ing)')

class NE_Record:
    def __init__(self,text,heading):
        self.parties = []
        self.url = ''
        self.locations = []
        self.gpe = []
        self.organizations = []
        self.time = []
        self.date = []
        self.money = []
        self.people = []
        self.percents = []
        self.facility = []
        self.latlngs = []
        self.normalizedTime = 0
        self.text = text
        self.dateText = ''
        self.doc = Doc()
        self.heading = heading
        self.pastTO = False
        self.year = ''
        self.month = ''
        self.properDate = ''
        self.sender = ''
        self.recipient = ''
        if text:
            self.taggedText = self.labelText(text)
            self.sentences = sent_tokenize(text)
            self.words = word_tokenize(text)
            for sent in self.taggedText:
                self.setupNEs(sent)
        if heading:
            self.taggedHeading = self.labelText(heading)
            self.labelHeading(self.taggedHeading[0])



    def labelText(self,text):
        output = []
        sents = sent_tokenize(text)
        for sentence in sents:
            words = word_tokenize(sentence)
            taggedWords = pos_tag(words)
            treeWithNamedEntities = ne_chunk(taggedWords)
            output.append(treeWithNamedEntities)
        return output

    def labelHeading(self,heading):
        try:
            heading.node
        except AttributeError:
            pass
        else:
            if heading.node == 'PERSON' or heading.node == 'GPE' or heading.node == 'ORGANIZATION':
                leaves = heading.leaves()
                person = " ".join(str(x[0]) for x in leaves)
                self.parties.append(person)
                if self.pastTO:
                    self.recipient = person
                else:
                    self.sender = person
            else:
                for child in heading:
                    try:
                        if child[1] == 'TO':
                            self.pastTO = True
                    except Exception as e:
                        pass
                    self.labelHeading(child)



    def setupNEs(self,tree):
        try:
            tree.node
        except AttributeError:
            pass
        else:
            if tree.node == 'ORGANIZATION':
                leaves = tree.leaves()
                org = " ".join(str(x[0]) for x in leaves)
                self.organizations.append(org)
            elif tree.node == 'PERSON':
                leaves = tree.leaves()
                person = " ".join(str(x[0]) for x in leaves)
                self.people.append(person)
            elif tree.node == 'LOCATION':
                leaves = tree.leaves()
                location = " ".join(str(x[0]) for x in leaves)
                self.locations.append(location)
            if tree.node == 'DATE':
                leaves = tree.leaves()
                date = " ".join(str(x[0]) for x in leaves)
                self.date.append(date)
            elif tree.node == 'TIME':
                leaves = tree.leaves()
                time = " ".join(str(x[0]) for x in leaves)
                self.time.append(time)
            elif tree.node == 'MONEY':
                leaves = tree.leaves()
                money = " ".join(str(x[0]) for x in leaves)
                self.money.append(money)
            elif tree.node == 'PERCENT':
                leaves = tree.leaves()
                percent = " ".join(str(x[0]) for x in leaves)
                self.percents.append(percent)
            elif tree.node == 'FACILITY':
                leaves = tree.leaves()
                facility = " ".join(str(x[0]) for x in leaves)
                self.facility.append(facility)
            elif tree.node == 'GPE':
                leaves = tree.leaves()
                gpe = " ".join(str(x[0]) for x in leaves)
                self.gpe.append(gpe)
            else:
                for child in tree:
                    self.setupNEs(child)





    def traverse(self,t,phrase):
        try:
            t.node
        except AttributeError:
            ' '.join(phrase,t[0])
            pass
        else:
            for child in t:
                self.setupNEs(child,phrase)
