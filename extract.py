from datetime import date, timedelta
import urllib.request
import zipfile
import csv
import redis
import redisconfig


class ExtractBhavCopy:
    baseUrl = "https://www.bseindia.com/download/BhavCopy/Equity/"
    finalUrl = None
    csvData = []
    lastdayDate = None
    csvFileName = None

    def __init__(self):
        dayInterval = 1
        if(date.today().weekday() == 6):  # check for sunday
            dayInterval = 2
        elif ((date.today().weekday() == 0)):  # check for monday
            dayInterval = 3
        self.lastdayDate = (date.today() - timedelta(dayInterval))\
            .strftime("%d%m%y")
        zipFileName = "EQ" + self.lastdayDate + "_CSV.ZIP"
        self.finalUrl = self.baseUrl + zipFileName
        self.csvFileName = "EQ" + self.lastdayDate + ".CSV"
        # print(self.finalUrl)
        try:
            urllib.request.urlretrieve(self.finalUrl, "zipFiles/"
                                       + zipFileName)
        except:
            print("Error downloading extract")
        try:
            zipRef = zipfile.ZipFile("zipFiles/" + zipFileName, 'r')
            zipRef.extractall("csvExtract")
            zipRef.close()
            self.filterCsv()
        except:
            print("Error extracting ZIP file")

    def filterCsv(self):
        with open("csvExtract/" + self.csvFileName, "r") as originalCsv,\
                open("csvExtract/filtered" + self.csvFileName, "w",
                     newline="") as filteredCsv:
            reader = csv.reader(originalCsv)
            writer = csv.writer(filteredCsv)
            for row in reader:
                del row[2:4]
                del row[6:]
                writer.writerow(row)
        self.parseCsv()

    def parseCsv(self):
        with open("csvExtract/filtered" + self.csvFileName, 'r') as csvFile:
            csvData = csv.DictReader(csvFile)
            for row in csvData:
                # print(dict(row))
                self.csvData.append(dict(row))
        # print(self.csvData)


class LoadBhavCopy:
    r = None

    def __init__(self):
        try:
            pool = redis.ConnectionPool(host=redisconfig.host,
                                        port=redisconfig.port,
                                        db=redisconfig.db,
                                        decode_responses=redisconfig
                                        .decode_responses_value)
            self.r = redis.Redis(connection_pool=pool)
        except:
            print("Error Connecting to Redis")
        self.loadData()

    def loadData(self):
        self.r.flushall()
        for idx, item in enumerate(ExtractBhavCopy.csvData):
            if(idx < 10):
                self.r.rpush("BhavCopy", item)
            self.r.hmset(item["SC_NAME"], item)
        # print(self.r.lrange("BhavCopy", 0, -1))


ExtractBhavCopy()
LoadBhavCopy()
