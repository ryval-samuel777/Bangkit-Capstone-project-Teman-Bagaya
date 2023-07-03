from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            # Process the file and make the API request
            url = 'https://api-gtgktzpmaq-et.a.run.app/fashion/predict'
            files = {'file': (file.filename, file.stream, file.content_type)}
            response = requests.post(url, files=files)

            if response.status_code == 200:
                try:
                    id = ''
                    data = response.json()
                    # Extract the relevant data from the API response
                    for key in data:
                        id = key
                        break  # Stop after finding the first key

                    dataId = data.get(id)

                    name = dataId.get('name')
                    image_url = dataId.get('picture')
                    store = dataId.get('Store')
                    desc = dataId.get('desc')
                    category = dataId.get('category')


                    if name is not None:
                        # Return the data as a JSON response
                        return render_template('detect.html', name=name, image_url=image_url, store=store, desc=desc, category=category)
                    else:
                        # Handle the case where the name is not available
                        return render_template('detect.html', error='Name not found. Please try again.')
                    
                except requests.exceptions.JSONDecodeError:
                    return jsonify({'error': 'Failed to decode response JSON'}), 500
            else:
                return jsonify({'error': 'Failed to upload photo'}), 400

    return render_template('detect.html')


@app.route('/catalog')
def catalog():
    # Make the API request to get the catalog items
    url = 'https://api-gtgktzpmaq-et.a.run.app/fashion/catalog'
    response = requests.get(url)

    if response.status_code == 200:
        try:
            data = response.json()
            items = []
            for key, item_data in data.items():
                item = {
                    'id': key,
                    'name': item_data.get('name'),
                    'image': item_data.get('picture'),
                    'description': item_data.get('desc'),
                    'category': item_data.get('category'),
                    'store': item_data.get('Store')
                }
                items.append(item)

            return render_template('catalog.html', items=items)
        except requests.exceptions.JSONDecodeError:
            return 'Failed to decode response JSON', 500
    else:
        return 'Failed to fetch catalog items', 400


@app.route('/detail/<item_name>')
def item_details(item_name):
    # Make the API request to get the item details based on the item_name
    url = f'https://api-gtgktzpmaq-et.a.run.app/fashion/catalog?name={item_name}'
    response = requests.get(url)

    if response.status_code == 200:
        try:
            items_data = response.json()
            id = ''
            for key in items_data: 
                id = key 
                break

            item_data = items_data.get(id)

            if item_data:
                item = {
                    'name': item_data.get('name'),
                    'image': item_data.get('picture'),
                    'description': item_data.get('desc'),
                    'category': item_data.get('category'),
                    'store': item_data.get('Store')
                }

                return render_template('details.html', item=item)
            else:
                return 'Item not found', 404
        except requests.exceptions.JSONDecodeError:
            return 'Failed to decode response JSON', 500
    else:
        return 'Failed to fetch item details', 400

if __name__ == '__main__':
    app.run(debug=True)
