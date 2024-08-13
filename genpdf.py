from fpdf import FPDF
import pandas as pd

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Heart Disease Report', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

def create_pdf_report(data, filename='heart_disease_report.pdf'):
    pdf = PDF()
    pdf.add_page()

    pdf.chapter_title('Patient Details:')
    details = (
        f"Age: {data['age']}\n"
        f"Sex: {data['sex']}\n"
        f"Chest Pain Type (cp): {data['cp']}\n"
        f"Resting Blood Pressure (trestbps): {data['trestbps']}\n"
        f"Serum Cholestoral (chol): {data['chol']}\n"
        f"Fasting Blood Sugar (fbs): {data['fbs']}\n"
        f"Resting Electrocardiographic Results (restecg): {data['restecg']}\n"
        f"Maximum Heart Rate Achieved (thalach): {data['thalach']}\n"
        f"Exercise Induced Angina (exang): {data['exang']}\n"
        f"Oldpeak: {data['oldpeak']}\n"
        f"Slope: {data['slope']}\n"
        f"Number of Major Vessels (ca): {data['ca']}\n"
        f"Thalassemia (thal): {data['thal']}"
    )
    pdf.chapter_body(details)

    pdf.output(filename)
    print(f"PDF report saved as {filename}")

if __name__ == '__main__':
    # Example data
    data = {
        'age': 55,
        'sex': 'Male',
        'cp': 'Typical angina',
        'trestbps': 140,
        'chol': 233,
        'fbs': '> 120 mg/dl',
        'restecg': 'Normal',
        'thalach': 150,
        'exang': 'No',
        'oldpeak': 2.3,
        'slope': 'Flat',
        'ca': 'Zero',
        'thal': 'Normal'
    }

    create_pdf_report(data)
