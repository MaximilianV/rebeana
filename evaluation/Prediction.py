import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from pm4py.objects.log.importer.parquet import factory as parquet_importer


class Prediction:
    user_id:str = None
    log = None
    output_path = "evaluation/results/ml/"

    def __init__(self, user_id, file:str=None, log=None, export_path:str=None):
        if (file is None and log is None) or (file is not None and log is not None):
            raise Exception("You must either provide a file to load or pass a log object.")
        if file:
            self.log = pd.read_parquet(file, engine='pyarrow')
        else:
            self.log = log

        self.user_id = user_id

        if export_path:
            self.output_path = export_path

    def evaluate(self, features:list, to_predict:str, plot_dataset:bool=True, plot_evaluation:bool=True):

        log = self.log.dropna(subset=features+[to_predict])

        #####################
        ### PLOT DATASET ####
        if plot_dataset:
            log_size = len(log)
            fig, ax = plt.subplots(1,len(features), sharey=True)
            for i, feature in enumerate(features):
                ax[i].plot(log[[feature]], log[[to_predict]], linewidth=0, marker='s', label='Data points (' + str(log_size) + ')')
                ax[i].set_xlabel(feature)
                ax[i].set_ylabel(to_predict)
                ax[i].legend(facecolor='white')

            fig.savefig(self.output_path + self.user_id + "_dataset.png")


        ########################
        ### DATA PREPARATION ###
        if 'daytime' in features:
            log['dt_sin'] = np.sin(log['daytime']*(2.*np.pi/24))
            log['dt_cos'] = np.cos(log['daytime']*(2.*np.pi/24))

            features.remove('daytime')
            features.extend(['dt_sin', 'dt_cos'])


        ##################
        ### SPLIT DATA ###
        X_train, X_test, y_train, y_test = train_test_split(
            log[features], log[to_predict], test_size=0.2, random_state=42)


        #########################
        ### TRAIN AND PREDICT ###

        # regr = linear_model.LinearRegression()
        # regr = linear_model.LogisticRegression(max_iter=200)
        regr = DecisionTreeRegressor(max_depth=5)
        # regr = RandomForestRegressor(max_depth=5, random_state=0)

        regr.fit(X_train, y_train)

        y_pred = regr.predict(X_test)

        ##################
        ### EVALUATION ###

        error = 'MSE: %.2f' % mean_squared_error(y_test, y_pred)
        r2 = 'r2: %.2f' % regr.score(X_test, y_test)
        # r2 = 'r2: %.2f' % r2_score(y_test, y_pred)

        # print(self.user_id)

        # # The coefficients
        # print('Coefficients: \n', regr.coef_)
        # The mean squared error
        # print(error)
        # The coefficient of determination: 1 is perfect prediction
        # print(r2)

        # Plot outputs
        if 'dt_cos' in features:
            features.remove('dt_cos')
            features.remove('dt_sin')

        fig, ax = plt.subplots(1,len(features), sharey=True)
        if len(features) > 1:
            for i, feature in enumerate(features):
                ax[i].plot(X_test[[feature]], y_test, linewidth=0, marker='s', label='Actual')
                ax[i].plot(X_test[[feature]], y_pred, linewidth=0, marker='s', label='Predicted\n'+r2+'\n'+error, color="blue")
                ax[i].set_xlabel(feature)
                ax[i].set_ylabel(to_predict)
                ax[i].legend(facecolor='white')
        else:
            ax.plot(X_test[[features[0]]], y_test, linewidth=0, marker='s', label='Actual')
            ax.plot(X_test[[features[0]]], y_pred, linewidth=0, marker='s', label='Predicted\n'+r2+'\n'+error, color="blue")
            ax.set_xlabel(features[0])
            ax.set_ylabel(to_predict)
            ax.legend(facecolor='white')
        fig.savefig(self.output_path + self.user_id + "_wl_dt_pred.png")


####################################
####### MANUAL PREDICTION ##########

# pred = [[10, 10],
#         [15, 10],
#         [20, 10],
#         [20, 15],
#         [20, 20]]
# print(pred)

# pred = [[10, np.sin(10*(2.*np.pi/24)), np.cos(10*(2.*np.pi/24))],
#         [15, np.sin(10*(2.*np.pi/24)), np.cos(10*(2.*np.pi/24))],
#         [20, np.sin(10*(2.*np.pi/24)), np.cos(10*(2.*np.pi/24))],
#         [20, np.sin(15*(2.*np.pi/24)), np.cos(15*(2.*np.pi/24))],
#         [20, np.sin(20*(2.*np.pi/24)), np.cos(20*(2.*np.pi/24))]]

# print(regr.predict(pred))

####### END MANUAL PREDICTION ######
####################################



