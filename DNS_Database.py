import MySQLdb

class DNS_Database():
    def __init__(self):
        self.db = MySQLdb.connect("localhost")
        if self.db is None:
            raise Exception
        print "Connected to database server"
        self.cursor = self.db.cursor()
        print "Started cursor"
        self.cursor.execute("SELECT VERSION()")
        data = self.cursor.fetchone()
        print "Database version : %s " % data

        self.cursor.execute("CREATE DATABASE IF NOT EXISTS DNS_Records;")
        data = self.cursor.fetchall()
        for row in data:
            print row

        self.cursor.execute("USE DNS_Records")
        data = self.cursor.fetchall()
        for row in data:
            print row

        sql = """CREATE TABLE IF NOT EXISTS SITES (
         siteID  INT UNSIGNED  NOT NULL AUTO_INCREMENT,
         name  VARCHAR(30),
         PRIMARY KEY (siteID)
         );"""
        self.cursor.execute(sql)

        sql = "SELECT * FROM SITES WHERE siteID=1001"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        print data
        if data:
            print "First row is already in the table"
            pass
        else:
            sql = """INSERT INTO SITES(siteID, name)
             VALUES (1001, 'Unclassified')"""
            try:
                self.cursor.execute(sql)
                self.db.commit()
                print "Successfully committed"
            except:
                print "Error!"
                self.db.rollback()

            sql = """CREATE TABLE IF NOT EXISTS DNS_QRY (
             queryID  INT UNSIGNED  NOT NULL AUTO_INCREMENT,
             name  VARCHAR(255) NOT NULL,
             site INT UNSIGNED NOT NULL,
             PRIMARY KEY (queryID)
             );"""
            self.cursor.execute(sql)

            sql = """ALTER TABLE DNS_QRY ADD FOREIGN KEY (site) REFERENCES SITES (siteID);"""
            self.cursor.execute(sql)

            sql = """CREATE TABLE IF NOT EXISTS descriptions (
             descriptionID  INT UNSIGNED  NOT NULL AUTO_INCREMENT,
             description  VARCHAR(255) NOT NULL,
             sitedescribed INT UNSIGNED NOT NULL,
             PRIMARY KEY (descriptionID)
             );"""
            self.cursor.execute(sql)

            sql = """ALTER TABLE descriptions ADD FOREIGN KEY (sitedescribed) REFERENCES SITES (siteID);"""
            self.cursor.execute(sql)

    def add_site(self, site): # This method adds site name to the database (eg Facebook, Twitter, Reddit), not the specific DNS queries
        if not site:
            print "Site cannot be none"
            return 3 # Site is none
        if self.check_site(site):
            return 2 # returns if the site already exists
        sql = """INSERT INTO SITES(siteID, name)
         VALUES (NULL, '%s')""" % site
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print "Successfully committed"
            return 0 # Successful addition
        except:
            print "Error!"
            self.db.rollback()
            return 1 # Weird Error

    def check_site(self, site): # This methods checks to see if site name is already in database (used in conjunction ith add_site)
        sql = "SELECT siteID FROM SITES WHERE name='%s'" % site
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        print data
        if data:
            print "%s already exists in database" % site
            return True
        else:
            print "%s does not exist in database" % site
            return False


    def close_database(self):
        self.db.close()
        print "Database closed"

if __name__ == "__main__":
    db = DNS_Database()
    db.add_site("Facebook")
    db.add_site("Reddit")
    db.close_database()