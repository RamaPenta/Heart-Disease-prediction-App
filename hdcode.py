import streamlit as st
import pandas as pd
import pickle
from pathlib import Path
from PIL import Image

image = Image.open('background.jpg')
st.image(image)
# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



def main():
	"""Simple Login App"""

	st.title("Heart Disease Prediction App")

	menu = ["Home","Login","SignUp"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")

	elif choice == "Login":
		#st.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:
				st.sidebar.header('User Input Features')
				def user_input_features():
					
					age = st.sidebar.number_input('Enter your age: ')

					sex  = st.sidebar.selectbox('Sex',(0,1))
					cp = st.sidebar.selectbox('Chest pain type',(0,1,2,3))
					tres = st.sidebar.number_input('Resting blood pressure: ')
					chol = st.sidebar.number_input('Serum cholestoral in mg/dl: ')
					fbs = st.sidebar.selectbox('Fasting blood sugar',(0,1))
					res = st.sidebar.number_input('Resting electrocardiographic results: ')
					tha = st.sidebar.number_input('Maximum heart rate achieved: ')
					exa = st.sidebar.selectbox('Exercise induced angina: ',(0,1))
					old = st.sidebar.number_input('oldpeak ')
					slope = st.sidebar.number_input('he slope of the peak exercise ST segmen: ')
					ca = st.sidebar.selectbox('number of major vessels',(0,1,2,3))
					thal = st.sidebar.selectbox('thal',(0,1,2))

					data = {'age': age,
						'sex': sex, 
						'cp': cp,
						'trestbps':tres,
						'chol': chol,
						'fbs': fbs,
						'restecg': res,
						'thalach':tha,
						'exang':exa,
						'oldpeak':old,
						'slope':slope,
						'ca':ca,
						'thal':thal
						    }
					features = pd.DataFrame(data, index=[0])
					return features
				input_df = user_input_features()
				# Combines user input features with entire dataset
				# This will be useful for the encoding phase
				heart_dataset = pd.read_csv('heart.csv')
				heart_dataset = heart_dataset.drop(columns=['target'])
				df = pd.concat([input_df,heart_dataset],axis=0)

				# Encoding of ordinal features
				# https://www.kaggle.com/pratik1120/penguin-dataset-eda-classification-and-clustering
				df = pd.get_dummies(df, columns = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal'])

				df = df[:1] # Selects only the first row (the user input data)

				st.write(input_df)
				# Reads in saved classification model
				load_clf = pickle.load(open('Random_forest_model.pkl', 'rb'))

				# Apply model to make predictions
				prediction = load_clf.predict(df)
				prediction_proba = load_clf.predict_proba(df)
				#st.subheader(':blue[RANDOM FOREST]')

				st.subheader('Prediction')
				st.write(prediction)

				st.subheader(':blue[RANDOM FOREST Prediction Probability]')
				st.write(prediction_proba)
				# applying logistic regression
				load_lr = pickle.load(open('logistic_regression_model.pkl', 'rb'))
				prediction2 = load_lr.predict(df)
				prediction_proba2 = load_lr.predict_proba(df)
				#st.subheader('LOGISTIC REGRESSION')
				st.subheader('Prediction')
				st.write(prediction2)
				st.subheader(':blue[LOGISTIC REGRESSION Prediction Probability]')
				st.write(prediction_proba2)
				#applying knn
				load_knn = pickle.load(open('knearest_neighbhours_model.pkl', 'rb'))
				prediction3 = load_knn.predict(df)
				prediction_proba3 = load_knn.predict_proba(df)
				st.subheader('Prediction')
				st.write(prediction3)
				st.subheader(':blue[KNN Prediction Probability]')
				st.write(prediction_proba3)
				if(prediction==1):
                                        st.warning("You have Heart disease.Better to consult a doctor")
                
				 
				 
			else:
				st.warning("Incorrect Username/Password")





	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")



if __name__ == '__main__':
	main()
