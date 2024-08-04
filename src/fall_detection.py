import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import ensemble
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
import streamlit as st

def load_data(filename):
    df = pd.read_csv(filename)
    df = df.astype(float)
    return df.to_numpy()

def train_model(features, labels, depth, num_trees):
    clf = ensemble.RandomForestClassifier(max_depth=depth, n_estimators=num_trees, max_samples=0.5)
    clf.fit(features, labels)
    return clf

def evaluate_model(model, X_test, y_test):
    predicted_labels = model.predict(X_test)
    accuracy = accuracy_score(y_test, predicted_labels)
    return accuracy

def find_best_hyperparameters(X_train, y_train):
    best_accuracy = 0
    best_depth = 1
    best_num_trees = 1
    
    for depth in range(1, 6):
        for num_trees in [2, 3, 4]:
            clf = ensemble.RandomForestClassifier(max_depth=depth, n_estimators=num_trees, max_samples=0.5)
            cv_scores = cross_val_score(clf, X_train, y_train, cv=5)
            average_cv_accuracy = cv_scores.mean()
            print(f"depth: {depth:2d} n_trees: {num_trees:3d} cv accuracy: {average_cv_accuracy:7.4f}")
            
            if average_cv_accuracy > best_accuracy:
                best_accuracy = average_cv_accuracy
                best_depth = depth
                best_num_trees = num_trees
    
    return best_depth, best_num_trees, best_accuracy


def SBD():
    filename = 'cStick.csv'
    data = load_data(filename)
    features = data[:, 0:6]
    labels = data[:, -1]

    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2)

    # Train model
    depth = 1
    num_trees = 4
    model = train_model(X_train, y_train, depth, num_trees)
    # print(f"Built an RF with depth={depth} and number of trees={num_trees}")

    # Evaluate model
    accuracy = evaluate_model(model, X_test, y_test)
    st.header("Model Evaluated")
    st.write(f"The model is {accuracy*100:7.2f}% accurate")

    # # Find best hyperparameters
    # best_depth, best_num_trees, best_accuracy = find_best_hyperparameters(X_train, y_train)
    # print(f"Best depth: {best_depth} and best num_trees: {best_num_trees}. Accuracy: {best_accuracy}")
