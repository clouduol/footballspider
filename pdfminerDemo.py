#! /usr/bin/python3

from urllib.request import urlopen
from io import StringIO
from io import open
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

import warnings
warnings.filterwarnings("ignore")

# pdfFile is a fp, urlopen or open return value both ok
def readPDF(pdfFile):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    process_pdf(rsrcmgr, device, pdfFile)
    device.close()

    content = retstr.getvalue()
    retstr.close()
    return content

# local, open
print("## local, open ##")
pdfFile_local = open("/home/guoyunlong/Downloads/pdf-sample.pdf","rb")
outputString_local = readPDF(pdfFile_local)
print(outputString_local)
pdfFile_local.close()

# remote, urlopen
print("## remote , urlopen ##")
pdfFile = \
urlopen("http://unec.edu.az/application/uploads/2014/12/pdf-sample.pdf")
outputStirng = readPDF(pdfFile)
print(outputStirng)
pdfFile.close()
