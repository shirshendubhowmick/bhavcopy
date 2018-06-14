from datetime import date, timedelta
import urllib.request
import zipfile
import csv


class ExtractBhavCopy:
    baseUrl = "https://www.bseindia.com/download/BhavCopy/Equity/"
    finalUrl = None
    csvData = []
    yesterdayDate = None

    def __init__(self):
        self.yesterdayDate = (date.today() - timedelta(1)).strftime("%d%m%y")
        zipFileName = "EQ" +  self.yesterdayDate + "_CSV.ZIP"
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
            self.parseCSV()
        except:
            print("Error extracting ZIP file")
    
    def parseCSV(self):
        csvFileName = "EQ" + self.yesterdayDate + ".CSV"
        with open("csvExtract/" + csvFileName, 'r') as csvFile:
            csvData = csv.DictReader(csvFile)
            for row in csvData:
                self.csvData.append(row)
        print(self.csvData)


data = ExtractBhavCopy()
