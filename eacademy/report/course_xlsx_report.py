from odoo import models
import xlsxwriter

class CourseXlsx(models.AbstractModel):
    _name = 'report.eacademy.report_course_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Course Report in XLSX'

    def generate_xlsx_report(self, workbook, data, courses):
        for course in courses:
            sheet = workbook.add_worksheet(course.name)

            bold = workbook.add_format({'bold': True})

            # Headers
            sheet.write(0, 0, 'Course Name', bold)
            sheet.write(0, 1, 'Start Date', bold)
            sheet.write(0, 2, 'End Date', bold)
            sheet.write(0, 3, 'Description', bold)

            # Content
            sheet.write(1, 0, course.name)
            sheet.write(1, 1, str(course.start_date))
            sheet.write(1, 2, str(course.end_date))
            sheet.write(1, 3, course.description or '')
