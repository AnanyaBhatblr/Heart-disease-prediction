import fitz  # PyMuPDF
import pytesseract
import pandas as pd
import joblib

# Update this path to where your Tesseract executable is located
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def extract_data_from_text(text):
    data = {
        'age': None,
        'sex': None,
        'cp': None,
        'trestbps': None,
        'chol': None,
        'fbs': None,
        'restecg': None,
        'thalach': None,
        'exang': None,
        'oldpeak': None,
        'slope': None,
        'ca': None,
        'thal': None
    }

    for line in text.split('\n'):
        if 'age' in line.lower():
            data['age'] = int(line.split()[-1])
        if 'sex' in line.lower():
            data['sex'] = 'Male' if 'male' in line.lower() else 'Female'
        if 'cp' in line.lower():
            data['cp'] = line.split()[-1]
        if 'trestbps' in line.lower():
            data['trestbps'] = int(line.split()[-1])
        if 'chol' in line.lower():
            data['chol'] = int(line.split()[-1])
        if 'fbs' in line.lower():
            data['fbs'] = '> 120 mg/dl' if '>' in line else '< 120 mg/dl'
        if 'restecg' in line.lower():
            data['restecg'] = line.split()[-1]
        if 'thalach' in line.lower():
            data['thalach'] = int(line.split()[-1])
        if 'exang' in line.lower():
            data['exang'] = 'Yes' if 'yes' in line.lower() else 'No'
        if 'oldpeak' in line.lower():
            data['oldpeak'] = float(line.split()[-1])
        if 'slope' in line.lower():
            data['slope'] = line.split()[-1]
        if 'ca' in line.lower():
            data['ca'] = line.split()[-1]
        if 'thal' in line.lower():
            data['thal'] = line.split()[-1]

    return data

def get_true_values(df):
    df['sex'] = df.sex.map({'Male': 1, 'Female': 0})
    df['cp'] = df.cp.map({'Typical angina': 1,
                          'Atypical angina': 2,
                          'Non-anginal pain': 3,
                          'Asymptomatic': 4})
    df['fbs'] = df.fbs.map({'< 120 mg/dl': 0, '> 120 mg/dl': 1})
    df['restecg'] = df.restecg.map({'Normal': 0,
                                    'ST-T wave abnormality': 1,
                                    'Left Ventrical Hypertrophy': 2})
    df['exang'] = df.exang.map({'No': 0, 'Yes': 1})
    df['slope'] = df.slope.map({'Upsloping': 1,
                                'Flat': 2,
                                'Downsloping': 3})
    df['thal'] = df.thal.map({'Normal': 3,
                              'Fixed Defect': 6,
                              'Reversable Defect': 7})
    df['ca'] = df.ca.map({'Zero': 0, 'One': 1, 'Two': 2, 'Three': 3})
    return df

def load_and_test(test_params):
    # Load the saved model, scaler, and columns
    knn_model = joblib.load('knn_model.pkl')
    scaler = joblib.load('scaler.pkl')
    columns = joblib.load('columns.pkl')

    test_df = pd.DataFrame(test_params, columns=['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal'])
    test_df = get_true_values(test_df)
    test_df = pd.get_dummies(test_df)

    # Add missing columns to the test data
    for col in columns:
        if col not in test_df.columns:
            test_df[col] = 0
    test_df = test_df[columns]  # Ensure the order of columns is the same

    test_data = scaler.transform(test_df)

    prediction = knn_model.predict(test_data)
    return prediction

if __name__ == '__main__':
    pdf_path = 'heart_disease_report.pdf'
    text = extract_text_from_pdf(pdf_path)
    extracted_data = extract_data_from_text(text)
    test_params = [list(extracted_data.values())]
    prediction = load_and_test(test_params)
    print('Prediction for extracted parameters:', prediction)
