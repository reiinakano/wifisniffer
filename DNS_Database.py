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

            sql = """CREATE TABLE IF NOT EXISTS description_queries (
             description_queryID  INT UNSIGNED  NOT NULL AUTO_INCREMENT,
             description_query  VARCHAR(255) NOT NULL,
             querydescribed INT UNSIGNED NOT NULL,
             PRIMARY KEY (description_queryID)
             );"""
            self.cursor.execute(sql)

            sql = """ALTER TABLE description_queries ADD FOREIGN KEY (querydescribed) REFERENCES DNS_QRY (queryID);"""
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

    def get_siteID(self, site):
        sql = "SELECT siteID FROM SITES WHERE name='%s'" % site
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        print data
        if data:
            print "%s already exists in database" % site
            return data[0][0]
        else:
            print "%s does not exist in database" % site
            return -1

    def rename_site(self, old, new):
        if self.check_site(new):
            return 2
        sql = """UPDATE SITES set name='%s' where name='%s'""" % (new, old)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print "Successfully committed"
            return 0 # Successful addition
        except:
            print "Error!"
            self.db.rollback()
            return 1 # Weird Error

    def get_queryID(self, query):
        sql = "SELECT queryID FROM DNS_QRY WHERE name='%s'" % query
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        print data
        if data:
            print "%s already exists in database" % query
            return data[0][0]
        else:
            print "%s does not exist in database" % query
            return -1

    def check_DNS_query(self, query):
        sql = "SELECT queryID FROM DNS_QRY WHERE name='%s'" % query
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        print data
        if data:
            print "%s already exists in database" % query
            return True
        else:
            print "%s does not exist in database" % query
            return False

    def add_DNS_query(self, query): # This method adds the DNS query to the DNS_QRY table and assigns it by default as "Unclassified"
        if self.check_DNS_query(query):
            return 2
        sql = """INSERT INTO DNS_QRY(queryID, name, site) VALUES (NULL, '%s', 1001)""" % query
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print "Successfully committed"
            return 0 # Successful addition
        except:
            print "Error!"
            self.db.rollback()
            return 1 # Weird Error

    def get_site_of_DNS_query(self, query):
        sql = """SELECT SITES.name FROM SITES
         JOIN DNS_QRY ON SITES.siteID = DNS_QRY.site
         WHERE DNS_QRY.name='%s'""" % query
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        print data[0][0]
        return data[0][0]

    def reclassify_DNS_query(self, query, site): # Reclassifies existing query 'query' under 'site'
        siteID = self.get_siteID(site)
        if siteID == -1:
            return 2 # Error
        sql = """UPDATE DNS_QRY SET site=%d WHERE name='%s'""" % (siteID, query)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print "Successfully committed"
            return 0 # Successful addition
        except:
            print "Error!"
            self.db.rollback()
            return 1 # Weird Error

    def site_has_description(self, site): # Checks if site has an existing description in the database
        siteID = self.get_siteID(site)
        if siteID == -1:
            print "cannot check if non-existing site has description"
            raise Exception # Error
        sql = "SELECT descriptionID FROM descriptions WHERE sitedescribed=%d" % siteID
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        print data
        if data:
            print "%s already has a description" % site
            return True
        else:
            print "%s does not yet have a description" % site
            return False

    def add_site_description(self, site, description):
        if self.site_has_description(site):
            return 1 # Already has a description
        siteID = self.get_siteID(site)
        sql = """INSERT INTO descriptions(descriptionID, description, sitedescribed) VALUES (NULL, '%s', %d)""" %(description, siteID)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print "Successfully committed"
            return 0 # Successful addition
        except:
            print "Error!"
            self.db.rollback()
            return 1 # Weird Error

    def change_site_description(self, site, description):
        siteID = self.get_siteID(site)
        sql = """UPDATE descriptions SET description='%s' WHERE sitedescribed=%d""" %(description, siteID)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print "Successfully committed"
            return 0 # Successful addition
        except:
            print "Error!"
            self.db.rollback()
            return 1 # Weird Error

    def query_has_description(self, query): # Checks if site has an existing description in the database
        queryID = self.get_queryID(query)
        if queryID == -1:
            print "cannot check if non-existing query has description"
            raise Exception # Error
        sql = "SELECT description_queryID FROM description_queries WHERE querydescribed=%d" % queryID
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        print data
        if data:
            print "%s already has a description" % query
            return True
        else:
            print "%s does not yet have a description" % query
            return False

    def add_query_description(self, query, description):
        if self.query_has_description(query):
            return 1 # Already has a description
        queryID = self.get_queryID(query)
        sql = """INSERT INTO description_queries(description_queryID, description_query, querydescribed) VALUES (NULL, '%s', %d)""" %(description, queryID)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print "Successfully committed"
            return 0 # Successful addition
        except:
            print "Error!"
            self.db.rollback()
            return 1 # Weird Error

    def change_query_description(self, query, description):
        queryID = self.get_queryID(query)
        sql = """UPDATE description_queries SET description_query='%s' WHERE querydescribed=%d""" %(description, queryID)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            print "Successfully committed"
            return 0 # Successful addition
        except:
            print "Error!"
            self.db.rollback()
            return 1 # Weird Error

    def close_database(self):
        self.db.close()
        print "Database closed"

if __name__ == "__main__":
    db = DNS_Database()
    db.add_site("Facebook")
    db.rename_site("Reddit", "Gizmodo")
    db.add_DNS_query("www.reddit.com")
    db.reclassify_DNS_query("www.reddit.com", "Reddit")
    db.reclassify_DNS_query("www.dsfasfdasfa.com", "Reddit")
    db.add_site_description("Facebook", "Social media site")
    db.change_site_description("Github", "Social media site.")
    db.add_query_description("www.reddit.com", "Main site of Redit")
    db.change_query_description("www.reddit.com", "Main site of Reddit")
    db.get_site_of_DNS_query("www.reddit.com")
    db.close_database()