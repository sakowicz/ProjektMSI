from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from Dataset import Dataset
from numpy import swapaxes
from statistics import mean
from sklearn.metrics import accuracy_score
#Import data from files
from sklearn import base

datasets = []
datasets.append(Dataset("datasets\diabetes.csv", "Diabetes set"))
datasets.append(Dataset("datasets\wine.csv", "Wine set"))
datasets.append(Dataset("datasets\german.csv", "German set"))
datasets.append(Dataset("datasets\popfailures.csv","Popfailures set"))
datasets.append(Dataset("datasets\heart.csv","Heart set"))
datasets.append(Dataset("datasets\liver.csv","Liver set"))

#step 1 - full data approach
scores = []
for i in range(len(datasets)):
    classifiers = [
        KNeighborsClassifier(),
        GaussianNB(),
        DecisionTreeClassifier(),
        SVC(gamma='auto')
    ]
    predictions = []
    for j in range(len(classifiers)):
        member_clf = base.clone(classifiers[j])
        member_clf.fit(datasets[i].X_train, datasets[i].y_train)
        predictions.append(member_clf.predict(datasets[i].X_test))
        scores.append(accuracy_score(datasets[i].y_test, predictions[j]))


#step 2 - random subspace approach
subspaceScores = []
numberOfSubspaces = 40
for d in range(len(datasets)):
    subspaceDatasets = []
    classifiers = [
        KNeighborsClassifier(),
        GaussianNB(),
        DecisionTreeClassifier(),
        SVC(gamma='auto')
    ]
    for i in range(numberOfSubspaces):
        subspaceDatasets.append(datasets[d].GetRandomSubspaceDataset())
    for c in range(len(classifiers)):
        predictions = []
        y_pred = []
        for i in range(len(subspaceDatasets)):
            member_clf = base.clone(classifiers[c])
            member_clf.fit(subspaceDatasets[i].X_train, subspaceDatasets[i].y_train)
            predictions.append(member_clf.predict(subspaceDatasets[i].X_test))
        predictions = swapaxes(predictions,0,1)
        for p in range(len(predictions)):
            if mean(predictions[p]) >= 0.5:
                y_pred.append(1)
            else:
                y_pred.append(0)
        subspaceScores.append(accuracy_score(datasets[d].y_test,y_pred))

#step 3 comparasion of results
comparasion = []
for i in range(len(scores)):
    comparasion.append(round(scores[i]/subspaceScores[i],2))
    scores[i] = round(scores[i], 2)
    subspaceScores[i] = round(subspaceScores[i], 2)

for i in range(len(datasets)):
    print("Results: for " + datasets[i].name)
    print("Normal approach ")
    print("KNN, GaussianNB, Decision Tree, SVC")
    print(scores[i*len(classifiers):(i+1)*len(classifiers)])
    print("Subspace approach:")
    print("KNN, GaussianNB, Decision Tree, SVC")
    print(subspaceScores[i*len(classifiers):(i+1)*len(classifiers)])
#    print("Normal approach / Subspace approach")
#    print(comparasion[i*len(classifiers):(i+1)*len(classifiers)])
    print("")
counter = 0
for i in range(len(comparasion)):
    if comparasion[i] <= 1:
        counter = counter +1
print("In " + str(counter) + " of " + str(len(comparasion)) + " tests subspace algorithm achieved higher or equal accuracy")
