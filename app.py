from flask import Flask, render_template , request, jsonify
import joblib
from flask_cors import CORS, cross_origin

# Load the saved model and vectorizer
model = joblib.load('./emotion_classifier.joblib')
vectorizer = joblib.load('tfidf_vectorizer.joblib')
# Define the target names
target_names = ["sadness", "joy", "love", "anger", "fear", "surprise"]
# flask app
app = Flask(__name__)
# cors obj
cors = CORS(app, resources={r"/predict": {"origins": "*"}})
 
@app.route("/")
def home():
    return render_template('home.html')

# @cross_origin()
@app.route('/predict', methods=['POST'])
def predict():
    # Get the input JSON data
    data = request.get_json(force=True)
    tweet = data['tweet']
    # Vectorize the tweet using the loaded vectorizer
    tweet_tfidf = vectorizer.transform([tweet])
    # Predict the label using the loaded model
    prediction = model.predict(tweet_tfidf)
    # index 
    index = int(prediction[0])
    # Map the predicted label to the target name
    predicted_label = target_names[index]
    # Return the predicted label as JSON
    return jsonify({'sentiment': predicted_label,'index':index})

if __name__ == '__main__':
    app.run(debug=True)