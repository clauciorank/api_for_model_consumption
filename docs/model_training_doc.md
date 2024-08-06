To train the model in the example, we only used Sci-Kit Learn for the machine learning tasks, utilizing the Iris toy dataset.

First, we need to import the functions and libraries.

```
from sklearn.datasets import load_iris  # Import toy dataset Iris
from sklearn.model_selection import train_test_split  # Function to split into training and test
from sklearn.ensemble import RandomForestClassifier  # Random forest machine learning algorithm 
from sklearn import metrics  # Evaluate metrics
import pickle  # Save the trained model in a file
```

Then we get the dataset and split into training and testing

```
# Load dataset
dataset = load_iris(as_frame=True)

# Separate prediction and target variables
X, y = dataset.data, dataset.target

# Split into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

Now choose the model and fit it to the training set.

```
model = RandomForestClassifier(n_estimators=10)
model.fit(X_train, y_train)
```

Finally, print the accuracy of the model on the test set and write the model to a pkl file to be used in other instances.

```
print(metrics.accuracy_score(y_test, model.predict(X_test)))

with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
```


The full code:

```
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import pickle

if __name__ == '__main__':
    dataset = load_iris(as_frame=True)
    X, y = dataset.data, dataset.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=10)
    model.fit(X_train, y_train)
    print(metrics.accuracy_score(y_test, model.predict(X_test)))

    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
```