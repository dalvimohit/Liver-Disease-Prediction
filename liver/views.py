from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def index(request):
    return render(request,'index.html')
    
def predict(request):
	age=int(request.POST["age"])
	gender=request.POST["gender"]
	Total_Bilirubin=float(request.POST["Total_Bilirubin"])
	Direct_Bilirubin=float(request.POST["Direct_Bilirubin"])
	Alkaline_Phosphotase=float(request.POST["Alkaline_Phosphotase"])
	Alamine_Aminotransferase=float(request.POST["Alamine_Aminotransferase"])
	Aspartate_Aminotransferase=float(request.POST["Aspartate_Aminotransferase"])
	Total_Protiens=float(request.POST["Total_Protiens"])
	Albumin=float(request.POST["Albumin"])
	Albumin_and_Globulin_Ratio=float(request.POST["Albumin_and_Globulin_Ratio"])

	if(gender=="male"):
		Gender_Female = 0
		Gender_Male = 1
	else:
		Gender_Female = 1
		Gender_Male = 0

	input=[[age, Total_Bilirubin, Direct_Bilirubin, Alkaline_Phosphotase, Alamine_Aminotransferase, Aspartate_Aminotransferase, Total_Protiens, Albumin, Albumin_and_Globulin_Ratio, Gender_Female, Gender_Male]]

	#code start here
	import pandas as pd
	import numpy as np
	import warnings
	import matplotlib.pyplot as plt
	warnings.filterwarnings('ignore')

	data = pd.read_csv("indian_liver_patient.csv")
	df = pd.DataFrame(data)

	df['Albumin_and_Globulin_Ratio'].fillna(df['Albumin_and_Globulin_Ratio'].mean(),inplace=True)

	new_df=pd.get_dummies(df, columns=["Gender"])

	new_df=new_df[['Age','Total_Bilirubin','Direct_Bilirubin','Alkaline_Phosphotase','Alamine_Aminotransferase','Aspartate_Aminotransferase','Total_Protiens','Albumin','Albumin_and_Globulin_Ratio','Gender_Female','Gender_Male','Dataset']]

	x=new_df.iloc[:,:-1].values
	y=new_df.iloc[:,11].values

	from sklearn.model_selection import cross_val_score
	from sklearn.neighbors import KNeighborsClassifier

	neigh = KNeighborsClassifier(n_neighbors=1)
	train_model=neigh.fit(x,y)

	y_pred = int(train_model.predict(input))

	if(y_pred==1):
		result="bad"
	else:
		result="good"


	#end here

	if(result=="good"):
		return render(request,'good.html',{'age':age, 'gender':gender,'Total_Bilirubin':Total_Bilirubin, 'Direct_Bilirubin':Direct_Bilirubin,'Alkaline_Phosphotase':Alkaline_Phosphotase, 'Alamine_Aminotransferase':Alamine_Aminotransferase,'Aspartate_Aminotransferase':Aspartate_Aminotransferase, 'Total_Protiens':Total_Protiens,'Albumin':Albumin,'Albumin_and_Globulin_Ratio':Albumin_and_Globulin_Ratio,'result':result})
	else:
		return render(request,'bad.html',{'age':age, 'gender':gender,'Total_Bilirubin':Total_Bilirubin, 'Direct_Bilirubin':Direct_Bilirubin,'Alkaline_Phosphotase':Alkaline_Phosphotase, 'Alamine_Aminotransferase':Alamine_Aminotransferase,'Aspartate_Aminotransferase':Aspartate_Aminotransferase, 'Total_Protiens':Total_Protiens,'Albumin':Albumin,'Albumin_and_Globulin_Ratio':Albumin_and_Globulin_Ratio,'result':result})
	
	
