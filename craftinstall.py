import os
import stat
import fileinput
import os.path
import shutil

class CraftInstaller:
    
    def __init__(self):
        self._source = ""
        self._dest_root = ""
        self._dest_craft = ""
    
    @property
    def source(self):
        return self._source
    
    @source.setter
    def source(self, value):
        self._source = value
        
    @property
    def dest_root(self):
        return self._dest_root
    
    @dest_root.setter
    def dest_root(self, value):
        self._dest_root = value
    
    @property
    def dest_craft(self):
        return self._dest_craft
    
    @dest_craft.setter
    def dest_craft(self, value):
        self._dest_craft = value

    @property
    def db_name(self):
        return self._db_name
    
    @db_name.setter
    def db_name(self, value):
        self._db_name = value

    @property
    def db_password(self):
        return self._db_password
    
    @db_password.setter
    def db_password(self, value):
        self._db_password = value

    @property
    def db_user(self):
        return self._db_user
    
    @db_user.setter
    def db_user(self, value):
        self._db_user = value
    
    def run(self):
        
        #-----------------------------------------------------------
        # Migrate Craft files
        #-----------------------------------------------------------

        # Set source directory
        while os.path.exists(self.source) != True:
            self.source = input(">>>Craft Source: ")
            if os.path.exists(self.source) != True:
                print("Path not found.")
        self.source = os.path.normpath(self.source)

        # Set project root directory
        self.dest_root = input(">>>Project root: ")
        if os.path.exists(self.dest_root) != True:
            print("Creating new directory: " + self.dest_root)
            os.mkdir(self.dest_root)
        self.dest_root = os.path.normpath(self.dest_root)
        
        # Set project craft directory
        self.dest_craft = os.path.normpath(self.dest_root) + "/craft"
        if (os.path.exists(self.dest_craft)):
            print("Error: " + self.dest_craft + "cannot already exist.")
            return False
        
        # Copy the root files
        shutil.copytree(self.source + "/public", self.dest_root + "/public_html")

        # Copy the craft files
        shutil.copytree(self.source + "/craft", self.dest_craft)

        #-----------------------------------------------------------
        # Set Permissions
        #-----------------------------------------------------------
        os.chmod(self.dest_craft + "/app", stat.S_IRWXU)
        os.chmod(self.dest_craft + "/config", stat.S_IRWXU)
        os.chmod(self.dest_craft + "/storage", stat.S_IRWXU)


        #-----------------------------------------------------------
        # Create Database
        #-----------------------------------------------------------
        self.db_name = input(">>>Database name: ")
        self.db_password = input(">>>Database password: ")
        self.db_user = input(">>>Database user name: ")

        ## TODO: create database, choose between new or existing, table names, multi-environment configs        
        
        #-----------------------------------------------------------
        # Set config file
        #-----------------------------------------------------------
                
        for line in fileinput.input(self.dest_craft + "/config/db.php", inplace=True):
            if "'user' => 'root'" in line:
                print(line.replace("'user' => 'root'", "'user' => '" + self.db_user + "'"))
            elif "'password' => ''" in line:
                print(line.replace("'password' => ''", "'password' => '" + self.db_password + "'"))
            elif "'database' => ''" in line:
                print(line.replace("'database' => ''", "'database' => '"+ self.db_name + "'"))
            else:
                print(line)
            

if __name__ == '__main__':
    installer = CraftInstaller()
    installer.run()