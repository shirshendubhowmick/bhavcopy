from datetime import date, timedelta
import urllib.request
import zipfile


class ExtractBhavCopy:
    baseUrl = "https://www.bseindia.com/download/BhavCopy/Equity/"
    finalUrl = None

    def __init__(self):
        yesterdayDate = (date.today() - timedelta(1)).strftime("%d%m%y")
        zipFileName = "EQ" +  yesterdayDate + "_CSV.ZIP"
        self.finalUrl = self.baseUrl + zipFileName
        print(self.finalUrl)
        try:
            urllib.request.urlretrieve(self.finalUrl, "zipFiles/" + zipFileName)
        except:
            print("Error downloading extract")
        try:
            zipRef = zipfile.ZipFile("zipFiles/" + zipFileName, 'r')
            zipRef.extractall("csvExtract")
            zipRef.close()
        except:
            print("Error extracting ZIP file")



data = ExtractBhavCopy()
