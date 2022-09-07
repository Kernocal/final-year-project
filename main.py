from session import createTorSession
from whiteHouse import startAuthentication
from crawler import generateDatabaseSkeleton

def startCrawling():
    s = createTorSession()
    if not s:
        return False
    generateDatabaseSkeleton()
    startAuthentication(s)
    return s

if __name__ == '__main__':
    print("Welcome to the White House Market data extraction tool.")
    startCrawling()
    print("Exiting.")



