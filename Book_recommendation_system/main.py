from flask import Flask,render_template,request
import pickle
import pandas as pd
import numpy as np

#with open('pt.pkl','rb') as f:
#    data1=pickle.load(f)
#    data1.to_csv('pt.csv', index=True)

#with open('books.pkl','rb') as f:
#    data2=pickle.load(f)
#data2.to_csv('books.csv', index=True)

#with open('similarity_scores.pkl','rb') as f:
#    data3=pickle.load(f)
#    df = pd.DataFrame(data3)  # Convert NumPy array to pandas DataFrame
#df.to_csv('similarity_scores.csv', index=True)


popular_df = pd.read_csv('popular.csv')
pt = pd.read_csv('pt.csv')
books = pd.read_csv('books.csv')
similarity_scores = pd.read_csv('similarity_scores.csv')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    # Check data types
    print(type(pt.index[0]))  # Print the data type of pt.index
    print(type(user_input))  # Print the data type of user_input

    # Verify formatting
    print(repr(pt.index[0]))  # Print the first element of pt.index with repr() to show any hidden characters
    print(repr(user_input))  # Print user_input with repr() to show any hidden characters

    # Debugging
    print(pt.index)  # Print all elements of pt.index
    print(user_input)  # Print user_input

    if np.any(pt.index==user_input):
        index = np.where(pt.index==user_input)[0]
        index = index[0]
    else:
        print("not found")
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:11]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return str(user_input)

if __name__=='__main__':
    app.run(debug=True)
