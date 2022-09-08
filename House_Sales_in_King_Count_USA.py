#!/usr/bin/env python
# coding: utf-8

# <p style="text-align:center">
#     <a href="https://skills.network/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkDA0101ENSkillsNetwork20235326-2022-01-01" target="_blank">
#     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/assets/logos/SN_web_lightmode.png" width="200" alt="Skills Network Logo"  />
#     </a>
# </p>
# 
# <h1 align=center><font size = 5>Data Analysis with Python</font></h1>
# 

# # House Sales in King County, USA
# 

# This dataset contains house sale prices for King County, which includes Seattle. It includes homes sold between May 2014 and May 2015.
# 

# | Variable      | Description                                                                                                 |
# | ------------- | ----------------------------------------------------------------------------------------------------------- |
# | id            | A notation for a house                                                                                      |
# | date          | Date house was sold                                                                                         |
# | price         | Price is prediction target                                                                                  |
# | bedrooms      | Number of bedrooms                                                                                          |
# | bathrooms     | Number of bathrooms                                                                                         |
# | sqft_living   | Square footage of the home                                                                                  |
# | sqft_lot      | Square footage of the lot                                                                                   |
# | floors        | Total floors (levels) in house                                                                              |
# | waterfront    | House which has a view to a waterfront                                                                      |
# | view          | Has been viewed                                                                                             |
# | condition     | How good the condition is overall                                                                           |
# | grade         | overall grade given to the housing unit, based on King County grading system                                |
# | sqft_above    | Square footage of house apart from basement                                                                 |
# | sqft_basement | Square footage of the basement                                                                              |
# | yr_built      | Built Year                                                                                                  |
# | yr_renovated  | Year when house was renovated                                                                               |
# | zipcode       | Zip code                                                                                                    |
# | lat           | Latitude coordinate                                                                                         |
# | long          | Longitude coordinate                                                                                        |
# | sqft_living15 | Living room area in 2015(implies-- some renovations) This might or might not have affected the lotsize area |
# | sqft_lot15    | LotSize area in 2015(implies-- some renovations)                                                            |
# 

# In[3]:


#After executing the below command restart the kernel and run all cells.
get_ipython().system('pip3 install scikit-learn --upgrade --user')


# You will require the following libraries:
# 

# In[4]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,PolynomialFeatures
from sklearn.linear_model import LinearRegression
get_ipython().run_line_magic('matplotlib', 'inline')


# # Module 1: Importing Data Sets
# 

# Load the csv:
# 

# In[5]:


file_name='https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-SkillsNetwork/labs/FinalModule_Coursera/data/kc_house_data_NaN.csv'
df=pd.read_csv(file_name)


# We use the method <code>head</code> to display the first 5 columns of the dataframe.
# 

# In[6]:


df.head()


# ### Question 1
# 
# Display the data types of each column using the function dtypes, then take a screenshot and submit it, include your code in the image.
# 

# In[8]:


df.dtypes


# We use the method describe to obtain a statistical summary of the dataframe.
# 

# In[9]:


df.describe()


# # Module 2: Data Wrangling
# 

# ### Question 2
# 
# Drop the columns <code>"id"</code>  and <code>"Unnamed: 0"</code> from axis 1 using the method <code>drop()</code>, then use the method <code>describe()</code> to obtain a statistical summary of the data. Take a screenshot and submit it, make sure the <code>inplace</code> parameter is set to <code>True</code>
# 

# In[10]:


df.drop("id", axis = 1, inplace = True)
df.drop("Unnamed: 0", axis = 1, inplace = True)
df.describe()


# We can see we have missing values for the columns <code> bedrooms</code>  and <code> bathrooms </code>
# 

# In[11]:


print("number of NaN values for the column bedrooms :", df['bedrooms'].isnull().sum())
print("number of NaN values for the column bathrooms :", df['bathrooms'].isnull().sum())


# We can replace the missing values of the column <code>'bedrooms'</code> with the mean of the column  <code>'bedrooms' </code> using the method <code>replace()</code>. Don't forget to set the <code>inplace</code> parameter to <code>True</code>
# 

# In[12]:


mean=df['bedrooms'].mean()
df['bedrooms'].replace(np.nan,mean, inplace=True)


# We also replace the missing values of the column <code>'bathrooms'</code> with the mean of the column  <code>'bathrooms' </code> using the method <code>replace()</code>. Don't forget to set the <code> inplace </code>  parameter top <code> True </code>
# 

# In[13]:


mean=df['bathrooms'].mean()
df['bathrooms'].replace(np.nan,mean, inplace=True)


# In[14]:


print("number of NaN values for the column bedrooms :", df['bedrooms'].isnull().sum())
print("number of NaN values for the column bathrooms :", df['bathrooms'].isnull().sum())


# # Module 3: Exploratory Data Analysis
# 

# ### Question 3
# 
# Use the method <code>value_counts</code> to count the number of houses with unique floor values, use the method <code>.to_frame()</code> to convert it to a dataframe.
# 

# In[15]:


df['floors'].value_counts().to_frame()


# ### Question 4
# 
# Use the function <code>boxplot</code> in the seaborn library  to  determine whether houses with a waterfront view or without a waterfront view have more price outliers.
# 

# In[16]:


sns.boxplot(x = "waterfront",y = "price", data=df)


# ### Question 5
# 
# Use the function <code>regplot</code>  in the seaborn library  to  determine if the feature <code>sqft_above</code> is negatively or positively correlated with price.
# 

# In[17]:


sns.regplot(x="sqft_above",y="price",data=df, ci=None)


# We can use the Pandas method <code>corr()</code>  to find the feature other than price that is most correlated with price.
# 

# In[18]:


df.corr()['price'].sort_values()


# # Module 4: Model Development
# 

# We can Fit a linear regression model using the  longitude feature <code>'long'</code> and  caculate the R^2.
# 

# In[19]:


X = df[['long']]
Y = df['price']
lm = LinearRegression()
lm.fit(X,Y)
lm.score(X, Y)


# ### Question  6
# 
# Fit a linear regression model to predict the <code>'price'</code> using the feature <code>'sqft_living'</code> then calculate the R^2. Take a screenshot of your code and the value of the R^2.
# 

# In[20]:


X1 = df[['sqft_living']]
Y1 = df[['price']]
lm1 = LinearRegression()
lm1.fit(X1,Y1)
lm1.score(X1,Y1)


# ### Question 7
# 
# Fit a linear regression model to predict the <code>'price'</code> using the list of features:
# 

# In[21]:


features =["floors", "waterfront","lat" ,"bedrooms" ,"sqft_basement" ,"view" ,"bathrooms","sqft_living15","sqft_above","grade","sqft_living"]     


# Then calculate the R^2. Take a screenshot of your code.
# 

# In[22]:


X2 = df[features]
Y2 = df['price']
lm1.fit(X2,Y2)
lm1.score(X2,Y2)


# ### This will help with Question 8
# 
# Create a list of tuples, the first element in the tuple contains the name of the estimator:
# 
# <code>'scale'</code>
# 
# <code>'polynomial'</code>
# 
# <code>'model'</code>
# 
# The second element in the tuple  contains the model constructor
# 
# <code>StandardScaler()</code>
# 
# <code>PolynomialFeatures(include_bias=False)</code>
# 
# <code>LinearRegression()</code>
# 

# In[ ]:


Input=[('scale',StandardScaler()),('polynomial', PolynomialFeatures(include_bias=False)),('model',LinearRegression())]


# ### Question 8
# 
# Use the list to create a pipeline object to predict the 'price', fit the object using the features in the list <code>features</code>, and calculate the R^2.
# 

# In[24]:


input = [('scale',StandardScaler()),('polynomial',PolynomialFeatures(include_bias=False)),('model',LinearRegression())]
pipe = Pipeline(input)
pipe
X3 = df[features]
Y3 = df['price']
pipe.fit(X3,Y3)
pipe.score(X3,Y3)


# # Module 5: Model Evaluation and Refinement
# 

# Import the necessary modules:
# 

# In[25]:


from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
print("done")


# We will split the data into training and testing sets:
# 

# In[26]:


features =["floors", "waterfront","lat" ,"bedrooms" ,"sqft_basement" ,"view" ,"bathrooms","sqft_living15","sqft_above","grade","sqft_living"]    
X = df[features]
Y = df['price']

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.15, random_state=1)


print("number of test samples:", x_test.shape[0])
print("number of training samples:",x_train.shape[0])


# ### Question 9
# 
# Create and fit a Ridge regression object using the training data, set the regularization parameter to 0.1, and calculate the R^2 using the test data.
# 

# In[27]:


from sklearn.linear_model import Ridge


# In[28]:


RidgeModel = Ridge(alpha=0.1)
RidgeModel.fit(x_train,y_train)F
RidgeModel.score(x_test,y_test)


# ### Question 10
# 
# Perform a second order polynomial transform on both the training data and testing data. Create and fit a Ridge regression object using the training data, set the regularisation parameter to 0.1, and calculate the R^2 utilising the test data provided. Take a screenshot of your code and the R^2.
# 

# In[32]:


pf = PolynomialFeatures(degree=2)
x_train_pf = pf.fit_transform(x_train[features])
x_test_pf = pf.fit_transform(x_test[features])

ridgemodel1 = Ridge(alpha=0.1)
ridgemodel1.fit(x_train_pf,y_train)
ridgemodel1.score(x_test_pf,y_test)

