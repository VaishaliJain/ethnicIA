from torch.utils.data import SubsetRandomSampler
from model_definition import LogisticRegressionModel
from model_ethnicIA_utilities import get_train_dataset, find_pos_weights
import torch
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt


def computation_train_ethnicIA_model(train_data_label, training_size=500000):
    print("date and time =", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    # race_dict = {0: 'Asian', 1: 'Black', 2: 'Hispanic', 3: 'White'}
    batch_size = 1024
    X_train, y, train_data, y_train = get_train_dataset(train_data_label, num_rows=training_size)
    pos_weights = find_pos_weights(y)
    pos_weights[3] = 1
    train_dataset = torch.utils.data.TensorDataset(torch.tensor(np.array(X_train), dtype=torch.float32),
                                                   torch.tensor(np.array(y_train), dtype=torch.long))
    train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
    print("date and time =", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    epochs = 150
    input_dim = len(X_train.columns)
    output_dim = 4
    lr_rate = 0.001
    model = LogisticRegressionModel(input_dim, output_dim)
    criterion = torch.nn.CrossEntropyLoss(weight=torch.tensor(pos_weights, dtype=torch.float32))
    optimizer = torch.optim.Adam(model.parameters(), lr=lr_rate)

    iteration_list = []
    loss_list = []
    accuracy_list = []
    average_loss = 0
    iteration = 0

    for epoch in range(int(epochs)):
        correct = 0
        total = 0
        for i, (train_features, labels) in enumerate(train_loader):
            iteration = iteration + 1
            optimizer.zero_grad()
            outputs = model(train_features)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total += labels.size(0)
            _, predicted = torch.max(outputs.data, 1)
            correct += (predicted == labels).sum().item()
            average_loss += loss.item()

            if iteration % 100 == 0:
                iteration_list.append(iteration)
                loss_list.append(average_loss / 100)
                accuracy = 100 * correct / total
                print("Iteration: {}. Loss: {}. Accuracy: {}.".format(iteration, average_loss / 100, accuracy))
                accuracy_list.append(accuracy)
                total = 0
                correct = 0
                average_loss = 0

    path = "../../Models/model_" + train_data_label + "_" + str(int(training_size / 1000)) + "k.pt"
    torch.save(model.state_dict(), path)

    plt.plot(iteration_list, loss_list)
    plt.xlabel('Number of Iterations')
    plt.ylabel('Loss on Training Set')
    plt.title('Logistic Regression')
    plt.savefig("../../Visualizations/TrainingCurves/model_" + train_data_label + "_" + str(
        int(training_size / 1000)) + "k_loss.png")
    plt.clf()

    plt.plot(iteration_list, accuracy_list)
    plt.xlabel('Number of Iterations')
    plt.ylabel('Accuracy on Training Set')
    plt.title('Logistic Regression')
    plt.savefig("../../Visualizations/TrainingCurves/model_" + train_data_label + "_" + str(
        int(training_size / 1000)) + "k_accuracy.png")
    plt.clf()
    print("date and time =", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))