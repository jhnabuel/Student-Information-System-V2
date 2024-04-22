import mysql.connector
class ConnectDatabase:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 3306
        self.user = "root"
        self.password = ""
        self.database = "informationsystem"
        self.cursor = None

    def connect_database(self):
        self.connect = mysql.connector.connect(
            host=self.host,
            user=self.user,
            port=self.port,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connect.cursor(dictionary=True)

    def add_student(self, student_id, student_name, student_year, student_gender, student_course):
        try:
            self.connect_database()
            # Prepare the SQL query with placeholders
            query = """INSERT INTO studentinfo (idnumber, name, yearLevel, gender, courseCode) 
                       VALUES (%s, %s, %s, %s, %s);"""
            # Execute the SQL query with the provided parameters
            self.cursor.execute(query, (student_id, student_name, student_year, student_gender, student_course))
            # Commit the transaction to save the changes
            self.connect.commit()
            return None  # Return None to indicate success
        except Exception as e:
            # Rollback the transaction and return the error message
            self.connect.rollback()
            return str(e)
        finally:
            # Close the database connection
            self.connect.close()

    def delete_student(self, student_id):
        self.connect_database()
        # Construct SQL query for deleting student info
        sql = "DELETE FROM studentinfo WHERE idnumber = %s;"
        try:
            # Execute the SQL query for deleting student info
            self.cursor.execute(sql, (student_id,))
            self.connect.commit()
        except Exception as E:
            # Rollback the operation in a case of an error
            self.connect.rollback()
            return E
        finally:
            # Close the database connection
            self.connect.close()

    def edit_student(self, student_id, student_name, student_year, student_gender, student_course):
        try:
            self.connect_database()
            # Prepare the SQL query with placeholders
            query = f"""UPDATE studentinfo
                        SET name = %s, yearLevel = %s, gender = %s, courseCode = %s 
                       WHERE idnumber = %s;"""
            # Execute the SQL query with the provided parameters
            self.cursor.execute(query, (student_name, student_year, student_gender, student_course, student_id))
            # Commit the transaction to save the changes
            self.connect.commit()
            return None  # Return None to indicate success
        except Exception as e:
            # Rollback the transaction and return the error message
            self.connect.rollback()
            return str(e)
        finally:
            # Close the database connection
            self.connect.close()

    def search_student(self, search_field=None, search_value=None):
        self.connect_database()
        condition = ""
        if search_field and search_value:
            if search_field == "ID Number":
                condition = "idnumber LIKE %s"
            elif search_field == "Name":
                condition = "name LIKE %s"
            elif search_field == "Year Level":
                condition = "yearLevel LIKE %s"
            elif search_field == "Course Code":
                condition = "courseCode LIKE %s"

        order_by = "idnumber ASC"
        if condition:
            sql = f"""
                SELECT * FROM studentinfo WHERE {condition};    
            """
            self.cursor.execute(sql, (f"%{search_value}%",))  # Correct parameter passing
        else:
            sql = f"""
                SELECT * FROM studentinfo ORDER BY {order_by};
            """
            self.cursor.execute(sql)
        try:
            result = self.cursor.fetchall()
            return result
        except Exception as E:
            return E

    def add_course(self, course_code, course_name):
        try:
            self.connect_database()
            # Prepare the SQL query with placeholders
            query = """INSERT INTO courseinfo (course_code, course_name) 
                       VALUES (%s, %s);"""
            # Execute the SQL query with the provided parameters
            self.cursor.execute(query, (course_code, course_name))
            # Commit the transaction to save the changes
            self.connect.commit()
            return None  # Return None to indicate success
        except Exception as e:
            # Rollback the transaction and return the error message
            self.connect.rollback()
            return str(e)
        finally:
            # Close the database connection
            self.connect.close()

    def delete_course(self, course_code):
        self.connect_database()
        # Construct SQL query for deleting student info
        sql = "DELETE FROM courseinfo WHERE course_code = %s;"
        try:
            # Execute the SQL query for deleting student info
            self.cursor.execute(sql, (course_code,))
            self.connect.commit()
        except Exception as E:
            # Rollback the operation in a case of an error
            self.connect.rollback()
            return E
        finally:
            # Close the database connection
            self.connect.close()

    def edit_course(self, course_code, course_name, original_course):
        try:
            self.connect_database()
            # Prepare the SQL query with placeholders
            query = f"""UPDATE courseinfo
                        SET course_code = %s, course_name = %s
                       WHERE course_code = %s;"""
            # Execute the SQL query with the provided parameters
            self.cursor.execute(query, (course_code, course_name, original_course))
            # Commit the transaction to save the changes
            self.connect.commit()
            return None  # Return None to indicate success
        except Exception as e:
            # Rollback the transaction and return the error message
            self.connect.rollback()
            return str(e)
        finally:
            # Close the database connection
            self.connect.close()

    def search_course(self, search_value=None):
        self.connect_database()

        if search_value:
            condition = "course_code LIKE %s OR course_name LIKE %s"
        else:
            condition = None

        order_by = "course_code ASC"
        if condition:
            sql = f"""
                SELECT * FROM courseinfo WHERE {condition};    
            """
            self.cursor.execute(sql, (f"%{search_value}%", f"%{search_value}%"))  # Correct parameter passing
        else:
            sql = f"""
                SELECT * FROM courseinfo ORDER BY {order_by};
            """
            self.cursor.execute(sql)
        try:
            result = self.cursor.fetchall()
            return result
        except Exception as E:
            return E
