import pyttsx3
import PyPDF2

book = open('C:\\Users\\arpan\\Documents\\11th physics second booklet asgnment only.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(book)
pages = pdfReader.numPages
print(pages)
print('Analyising the book....')
speaker = pyttsx3.init()
for num in range(5, pages):
    print('Reading : ',num)
    page = pdfReader.getPage(num)
    text = page.extractText()
    speaker.say(text)
    speaker.runAndWait()
