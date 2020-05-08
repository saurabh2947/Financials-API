import xbrl, re
import pandas as pd

class financials:
    def __init__(self,sc=50096):
        self.scripcode=sc

    def bse_xmlparser(self):
    
        #initializaing dataframe
        df=pd.DataFrame()

        #parsing the XML file
        print('Initializing...')
        extension='.xml'
        filename=str(self.scripcode)+extension
        doc=str(xbrl.XBRLParser.parse(open(filename)))

        #cleaning the doc
        a=re.search(r'(.*?)<in-bse-fin:scripcode',doc).end()-21
        cleandoc=doc[a:]
        cleandoc=cleandoc.replace("\n", "")
        print('Doc cleaned')

        #getting contextref

        cntxt=re.compile(r'contextref=\"(.*?)\"')
        j=cntxt.findall(cleandoc)
        df['Context']=j

        #getting the XML tag
        arg=re.compile(r'</in-bse-fin:(.*?)>')
        k=arg.findall(cleandoc)
        df['keys']=k

        #getting the value
        value=re.compile(r'\">(.*?)</in-bse-fin:',re.DOTALL)
        n=value.findall(str(cleandoc))
        df['values']=n

        #sending the dataframe to csv
        df.set_index('keys',inplace=True)
        df.to_csv(str(self.scripcode)+'.csv')
        print('Done')

sc=input('Enter Scrip code:')
company=financials(sc)
company.bse_xmlparser()