\pdfPath="/Users/rsachdeva/Documents/pythonProjs/W2/0064O00000k6gEFQAY-00P4O00001KByHTUA1-check stubs _ w2.pdf"



import textract
text = textract.process(pdfPath)
print(text)