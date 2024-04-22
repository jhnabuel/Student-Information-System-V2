import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QMainWindow, QPushButton, QFrame, QMessageBox,
                             QComboBox, QTableWidget, QTableWidgetItem, QAbstractItemView)

from mainsys import Ui_MainWindow
from connect_databasesql import ConnectDatabase

# Create a main window class
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)

        # Initialize the UI from a separate UI file
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Initialize input fields for student
        self.idInput = self.ui.idInput
        self.idInput2 = self.ui.idInput2
        self.nameInput = self.ui.nameInput
        self.courseCombo = self.ui.courseCombo
        self.yearCombo = self.ui.yearCombo
        self.genderCombo = self.ui.genderCombo

        # Initialize input fields for course
        self.courseCodeInput = self.ui.courseCodeInput
        self.courseNameInput = self.ui.courseNameInput

        # Initialize buttons for student
        self.addStudentBtn = self.ui.addStudent
        self.editStudentBtn = self.ui.editStudent
        self.deleteStudentBtn = self.ui.deleteStudent
        self.clearStudentBtn = self.ui.clearStudent

        # Initialize buttons for course
        self.addCourseBtn = self.ui.addCourse
        self.editCourseBtn = self.ui.editCourse
        self.deleteCourseBtn = self.ui.deleteCourse
        self.clearCourseBtn = self.ui.clearCourse

        self.button_list_student = self.ui.inputFrame1.findChildren(QPushButton)
        self.button_list_course = self.ui.inputFrame2.findChildren(QPushButton)


        # Initialize tables
        self.studentDisplaytable = self.ui.studentDisplay
        self.studentDisplaytable.setSortingEnabled(False)
        self.courseDisplaytable = self.ui.courseDisplay
        self.courseDisplaytable.setSortingEnabled(False)

        # Initialize search function
        self.searchFilter = self.ui.searchFilter
        self.searchStudentInput = self.ui.searchStudent
        self.searchCourseInput = self.ui.searchCourse

        gender = ["Male", "Female", "Nonbinary", "Decline to state"]
        self.genderCombo.addItems(gender)
        year = ["1", "2", "3", "4"]
        self.yearCombo.addItems(year)
        self.init_signal_slot()
        filter = ["ID Number", "Name", "Year Level", "Course Code"]
        self.searchFilter.addItems(filter)

        # Create a database connection object
        self.db = ConnectDatabase()
        self.populateCourseBox()
        # Displaying student data
        self.load_student_data()
        self.load_course_data()
        self.studentDisplaytable.itemClicked.connect(self.select_student_info)
        self.courseDisplaytable.itemClicked.connect(self.select_course_info)
        self.searchStudentInput.textChanged.connect(self.search_student_info)
        self.searchCourseInput.textChanged.connect(self.search_course_info)



    def enable_buttons_student(self):
        for button in self.button_list_student:
            button.setDisabled(False)

    def disable_buttons_student(self):
        for button in self.button_list_student:
            button.setDisabled(True)

    def init_signal_slot(self):
        self.addStudentBtn.clicked.connect(self.addstudentinfo)
        self.deleteStudentBtn.clicked.connect(self.delete_student_info)
        self.editStudentBtn.clicked.connect(self.edit_student_info)
        self.clearStudentBtn.clicked.connect(self.clear_student_input)
        self.addCourseBtn.clicked.connect(self.add_course_info)
        self.deleteCourseBtn.clicked.connect(self.delete_course_info)
        self.editCourseBtn.clicked.connect(self.edit_course_info)
        self.clearCourseBtn.clicked.connect(self.clear_course_input)

    def addstudentinfo(self):
        try:
            # Disable student buttons while processing
            self.disable_buttons_student()

            # Get student info from input fields
            student_info = self.get_student_info()

            # Check if student info is valid
            if not student_info:
                QMessageBox.information(self, "Warning", "Please input student ID and student name",
                                        QMessageBox.StandardButton.Ok)
            else:
                # Extract student attributes from the student_info dictionary
                student_id = student_info["student_id"]
                student_name = student_info["student_name"]
                year = student_info["year"]
                gender = student_info["gender"]
                student_course = student_info["student_course"]

                # Check if student ID and name are not empty
                if not student_id or not student_name:
                    QMessageBox.warning(self, "Warning", "Please input student ID and student name",
                                        QMessageBox.StandardButton.Ok)
                else:
                    # Check if student ID already exists
                    if self.check_student_id(student_id):
                        QMessageBox.warning(self, "Warning", "Student ID already exists.",
                                            QMessageBox.StandardButton.Ok)
                    else:
                        # Attempt to add student information to the database
                        self.db.add_student(student_id, student_name, year, gender, student_course)
                        QMessageBox.warning(self, "Information", "Student information added to table.",
                                            QMessageBox.StandardButton.Ok)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add student information: {str(e)}",
                                 QMessageBox.StandardButton.Ok)
        finally:
            # Enable student buttons after processing
            self.enable_buttons_student()
            self.load_student_data()

    def studentname_valid(self):
        name = self.nameInput.text().strip()
        if not name:
            QMessageBox.warning(self, "Warning", "Please enter a name.", QMessageBox.StandardButton.Ok)
            return None  # Return None directly if validation fails

        if not name.replace(" ", "").isalpha():
            QMessageBox.warning(self, "Warning", "Please enter letters only for the name.",
                                QMessageBox.StandardButton.Ok)
            return None  # Return None directly if validation fails

        return name

    def studentid_valid(self):
        id_num1 = self.idInput.text().strip()
        id_num2 = self.idInput2.text().strip()

        if not id_num1 or not id_num2:
            QMessageBox.warning(self, "Warning", "Please enter both parts of the ID.", QMessageBox.StandardButton.Ok)
            return None  # Return None directly if validation fails

        if not id_num1.isdigit() or not id_num2.isdigit():
            QMessageBox.warning(self, "Warning", "Please enter digits only.", QMessageBox.StandardButton.Ok)
            return None  # Return None directly if validation fails

        if len(id_num1) != 4 or len(id_num2) != 4:
            QMessageBox.warning(self, "Warning", "Please enter 4 digits for each part.", QMessageBox.StandardButton.Ok)
            return None  # Return None directly if validation fails
        id_number = id_num1 + "-" + id_num2
        return id_number

    def check_student_id(self, student_id):
        # Function to check if Student ID already exists
        self.db.connect_database()
        self.db.cursor.execute("SELECT * FROM studentinfo WHERE idnumber = %s", (student_id,))
        row = self.db.cursor.fetchone()
        self.db.cursor.close()

        self.db.connect.close()

        return row is not None

    def get_student_info(self):
        student_id = str(self.studentid_valid())
        student_name = str(self.studentname_valid())
        year = self.yearCombo.currentText()
        gender = self.genderCombo.currentText()
        student_course = self.courseCombo.currentText()

        student_info = {
            "student_id": student_id,
            "student_name": student_name,
            "year": year,
            "gender": gender,
            "student_course": student_course
        }
        return student_info

    def load_student_data(self):
        self.db.connect_database()
        try:
            # Fetch all student data from the database
            student_data = self.db.search_student()
            # Display student data in the table widget
            self.display_student_data(student_data)
        except Exception as E:
            print("Error:", E)
        finally:
            # Close the database connection
            self.db.connect.close()

    def display_student_data(self, student_data):
        # Clear exisiting table contents
        self.studentDisplaytable.clear()
        self.studentDisplaytable.verticalHeader().setVisible(False)
        if student_data:
            self.studentDisplaytable.setRowCount(len(student_data))
            self.studentDisplaytable.setColumnCount(len(student_data[0]))
            # Populate the tablewidget with data
            for row_num, row_data in enumerate(student_data):
                for col_num, col_data in enumerate(row_data):
                    value = row_data[col_data]
                    self.studentDisplaytable.setItem(row_num, col_num, QTableWidgetItem(str(value)))
            # Set column headers
            headers = ["ID Number", "Name", "Year Level", "Gender", "Course Code"]
            self.studentDisplaytable.setHorizontalHeaderLabels(headers)
            self.studentDisplaytable.setSelectionMode(QAbstractItemView.SingleSelection)


    def select_student_info(self):
        # Function to select student info from the table and populate the fields to delete/edit
        try:
            select_row = self.studentDisplaytable.currentRow()
            if select_row != -1:
                self.idInput.setEnabled(False)
                self.idInput2.setEnabled(False)
                student_id = self.studentDisplaytable.item(select_row, 0).text().strip()
                student_id1 = student_id[:4]
                student_id2 = student_id[5:]
                student_name = self.studentDisplaytable.item(select_row, 1).text().strip()
                student_year = self.studentDisplaytable.item(select_row, 2).text().strip()
                student_gender = self.studentDisplaytable.item(select_row, 3).text().strip()
                student_course = self.studentDisplaytable.item(select_row, 4).text().strip()

                self.idInput.setText(student_id1)
                self.idInput2.setText(student_id2)
                self.nameInput.setText(student_name)
                self.yearCombo.setCurrentText(student_year)
                self.genderCombo.setCurrentText(student_gender)
                self.courseCombo.setCurrentText(student_course)

        except Exception as E:
            print(str(E))
            return E
        return select_row

    def delete_student_info(self):
        try:
            selected_info = self.select_student_info()
            if selected_info != -1:
                print(selected_info)
                select_option = QMessageBox.warning(self, "Warning", "Are you sure you want to delete this student?",
                                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if select_option == QMessageBox.StandardButton.Yes:
                    student_to_delete = self.studentDisplaytable.item(selected_info, 0).text().strip()
                    self.db.delete_student(student_to_delete)
                    QMessageBox.warning(self, "Information", f"Student with ID Number: {student_to_delete}, "
                                                                 f"has been deleted.", QMessageBox.StandardButton.Ok)

        except Exception as E:
            print(str(E))
        self.load_student_data()

    def edit_student_info(self):
        # Edit/update student information
        try:
            new_info = self.get_student_info()
            student_id = new_info["student_id"]
            new_student_name = new_info["student_name"]
            new_student_year = new_info["year"]
            gender = new_info["gender"]
            new_student_course = new_info["student_course"]
            if new_info["student_id"]:
                select_option = QMessageBox.warning(self, "Warning", "Are you sure you want to edit student information?",
                                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if select_option == QMessageBox.StandardButton.Yes:
                    self.db.edit_student(student_id, new_student_name, new_student_year, gender, new_student_course)
                    QMessageBox.warning(self, "Information", f"Student information with ID Number: {student_id}, "
                                                             f"has been updated.", QMessageBox.StandardButton.Ok)
            self.load_student_data()
        except Exception as e:
            print(str(e))

    def clear_student_input(self):
        self.idInput.clear()
        self.idInput.setEnabled(True)
        self.idInput2.clear()
        self.idInput2.setEnabled(True)
        self.nameInput.clear()
        self.yearCombo.setCurrentText("")
        self.genderCombo.setCurrentText("")
        self.courseCombo.setCurrentText("")

    def search_student_info(self):
        try:
            search_parameter = self.searchStudentInput.text()
            search_filter = self.searchFilter.currentText()
            search_results = self.db.search_student(search_filter, search_parameter)
            self.display_student_data(search_results)
        except Exception as E:
            print(str(E))

    def populateCourseBox(self):
        self.courseCombo.clear()
        self.db.connect_database()
        self.db.cursor.execute("SELECT course_code FROM courseinfo")
        rows = self.db.cursor.fetchall()
        for row in rows:
            self.courseCombo.addItem(row["course_code"])
        self.db.cursor.close()

        self.db.connect.close()

    def get_course_info(self):
        course_code = self.courseCodeInput.text().strip()
        course_name = self.courseNameInput.text().strip()
        course_info = {
            "course_code": course_code,
            "course_name": course_name,
        }
        return course_info

    def check_course_code(self, course_code):
        # Function to check if Student ID already exists
        self.db.connect_database()
        self.db.cursor.execute("SELECT * FROM courseinfo WHERE course_code = %s", (course_code,))
        row = self.db.cursor.fetchone()
        self.db.cursor.close()
        self.db.connect.close()
        return row is not None

    def add_course_info(self):
        try:
            # Disable student buttons while processing
            self.disable_buttons_student()

            # Get student info from input fields
            course_info = self.get_course_info()
            course_code = course_info["course_code"]
            course_name = course_info["course_name"]
            # Check if student ID and name are not empty
            if not course_code or not course_name:
                QMessageBox.warning(self, "Warning", "Please input course code and course name",
                                        QMessageBox.StandardButton.Ok)
            else:
                # Check if student ID already exists
                if self.check_course_code(course_code):
                    QMessageBox.warning(self, "Warning", "Course code already exists.",
                                        QMessageBox.StandardButton.Ok)
                else:
                    # Attempt to add student information to the database
                    self.db.add_course(course_code, course_name)
                    QMessageBox.warning(self, "Information", "Course information added to table.",
                                        QMessageBox.StandardButton.Ok)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add course information: {str(e)}",
                                 QMessageBox.StandardButton.Ok)
        finally:
            self.load_course_data()
            self.populateCourseBox()

    def load_course_data(self):
        self.db.connect_database()
        try:
            # Fetch all student data from the database
            course_data = self.db.search_course()
            # Display student data in the table widget
            self.display_course_data(course_data)
        except Exception as E:
            print("Error:", E)
        finally:
            # Close the database connection
            self.db.connect.close()

    def display_course_data(self, course_data):
        # Clear exisiting table contents
        self.courseDisplaytable.clear()
        self.courseDisplaytable.verticalHeader().setVisible(False)
        if course_data:
            self.courseDisplaytable.setRowCount(len(course_data))
            self.courseDisplaytable.setColumnCount(len(course_data[0]))
            # Populate the tablewidget with data
            for row_num, row_data in enumerate(course_data):
                for col_num, col_data in enumerate(row_data):
                    value = row_data[col_data]
                    self.courseDisplaytable.setItem(row_num, col_num, QTableWidgetItem(str(value)))
            # Set column headers
            headers = ["Course Code", "Course Name"]
            self.courseDisplaytable.setHorizontalHeaderLabels(headers)
            self.courseDisplaytable.setSelectionMode(QAbstractItemView.SingleSelection)

    def select_course_info(self):
        # Function to select student info from the table and populate the fields to delete/edit
        try:
            select_row = self.courseDisplaytable.currentRow()
            if select_row != -1:
                course_code = self.courseDisplaytable.item(select_row, 0).text().strip()
                course_name = self.courseDisplaytable.item(select_row, 1).text().strip()

                self.courseCodeInput.setText(course_code)
                self.courseNameInput.setText(course_name)

        except Exception as E:
            print(str(E))
            return E
        return select_row

    def delete_course_info(self):
        try:
            selected_info = self.select_course_info()
            if selected_info != -1:
                select_option = QMessageBox.warning(self, "Warning", "Are you sure you want to delete this course?",
                                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if select_option == QMessageBox.StandardButton.Yes:
                    course_to_delete = self.courseDisplaytable.item(selected_info, 0).text().strip()
                    self.db.delete_course(course_to_delete)
                    QMessageBox.warning(self, "Information", f"Course with course code: {course_to_delete}, "
                                                             f"has been deleted.", QMessageBox.StandardButton.Ok)

        except Exception as E:
            print(str(E))
        self.load_course_data()
        self.load_student_data()
        self.populateCourseBox()

    def edit_course_info(self):
        try:
            # Get new course information from input fields
            new_info = self.get_course_info()
            new_course_code = new_info["course_code"]
            new_course_name = new_info["course_name"]

            # Get the original course code
            selected_info = self.select_course_info()
            if selected_info != -1:
                original_course_code = self.courseDisplaytable.item(selected_info, 0).text().strip()

            # Check if the new course code is different from the original course code
            if new_course_code != original_course_code:
                select_option = QMessageBox.warning(self, "Warning",
                                                    "Are you sure you want to edit course information?",
                                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                if select_option == QMessageBox.StandardButton.Yes:
                    # Call the edit_course method with the new and original course codes
                    self.db.edit_course(new_course_code, new_course_name, original_course_code)
                    QMessageBox.warning(self, "Information", "Course information has been updated.",
                                        QMessageBox.StandardButton.Ok)

            # Reload the course and student data
            self.load_course_data()
            self.load_student_data()
            self.populateCourseBox()
        except Exception as e:
            print(str(e))

    def search_course_info(self):
        try:
            search_value = self.searchCourseInput.text().strip()
            search_results = self.db.search_course(search_value)
            self.display_course_data(search_results)
        except Exception as E:
            print(str(E))
    def clear_course_input(self):
        self.courseCodeInput.clear()
        self.courseNameInput.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


