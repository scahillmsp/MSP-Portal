from flask import Flask, send_from_directory, jsonify, request
import pandas as pd

app = Flask(__name__)

# Load data from Excel file
excel_file = 'parts_data.xlsx'
parts_df = pd.read_excel(excel_file, sheet_name='Parts')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/dropdowns', methods=['GET'])
def get_dropdowns():
    try:
        makes = parts_df['Make'].dropna().unique()
        models = parts_df['Model'].dropna().unique()
        versions = parts_df['Version'].dropna().unique()
        categories = parts_df['Category'].dropna().unique()

        data = {
            'makes': [{'id': idx, 'name': make} for idx, make in enumerate(makes)],
            'models': [{'id': idx, 'name': model} for idx, model in enumerate(models)],
            'versions': [{'id': idx, 'name': version} for idx, version in enumerate(versions)],
            'categories': [{'id': idx, 'name': category} for idx, category in enumerate(categories)]
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/models', methods=['GET'])
def get_models():
    make = request.args.get('make')
    if make:
        models = parts_df[parts_df['Make'] == make]['Model'].dropna().unique()
        data = {'models': [{'id': idx, 'name': model} for idx, model in enumerate(models)]}
        return jsonify(data)
    return jsonify({'models': []})

@app.route('/api/versions', methods=['GET'])
def get_versions():
    model = request.args.get('model')
    if model:
        versions = parts_df[parts_df['Model'] == model]['Version'].dropna().unique()
        data = {'versions': [{'id': idx, 'name': version} for idx, version in enumerate(versions)]}
        return jsonify(data)
    return jsonify({'versions': []})

@app.route('/api/categories', methods=['GET'])
def get_categories():
    version = request.args.get('version')
    if version:
        categories = parts_df[parts_df['Version'] == version]['Category'].dropna().unique()
        data = {'categories': [{'id': idx, 'name': category} for idx, category in enumerate(categories)]}
        return jsonify(data)
    return jsonify({'categories': []})

@app.route('/api/parts', methods=['GET'])
def get_parts():
    make = request.args.get('make')
    model = request.args.get('model')
    version = request.args.get('version')
    category = request.args.get('category')

    query = parts_df
    if make:
        query = query[query['Make'] == make]
    if model:
        query = query[query['Model'] == model]
    if version:
        query = query[query['Version'] == version]
    if category:
        query = query[query['Category'] == category]

    parts = query[['Part', 'Part Number']].drop_duplicates().to_dict(orient='records')
    return jsonify(parts)

if __name__ == '__main__':
    app.run(debug=True)
