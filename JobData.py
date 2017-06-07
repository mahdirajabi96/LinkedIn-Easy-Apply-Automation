class JobData:
    def __init__(self, jobTitle, company, link, city, htmlel):
        self.jobTitle = jobTitle
        self.company = company
        self.link = link
        self.city = city
        self.htmlel = htmlel
    #enddef
    def __str__(self):
        return self.jobTitle+','+self.company+','+self.link+','+self.city
