class PlayListItemFilter:

    def __init__(self):
        self.filterFunctions = []
        self.addFilter(PlayListItemFilter.defaultFilter)

    def addFilter(self, filterFunction):
        self.filterFunctions.append(filterFunction)

    def addFiltersFromArguments(self, arguments):
        # search parameter
        if not arguments.search is None:
            self.addFilter(PlayListItemFilter.getSearchFilter(arguments.search))
        # index parameter

    def checkItem(self, item):
        for filter in self.filterFunctions:
            if filter(item) == False:
                return False
        return True
    
    @staticmethod
    def defaultFilter(item):
        if item is None:
            return False
        if item['title'] is None:
            return False
        return True
    
    @staticmethod
    def getSearchFilter(keywords):
        if isinstance(keywords, list):
            keywords = keywords[0].split()
        def searchFilter(item):
                for keyword in keywords:
                    if keyword.lower() in item['title'].lower():
                        return True
                return False
        return searchFilter

