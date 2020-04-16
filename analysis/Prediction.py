import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from pm4py.objects.log.importer.parquet import factory as parquet_importer
# from sklearn.tree import export_graphviz
# from sklearn.externals.six import StringIO
# import pydotplus

plt.rc('font', size=14)

class Prediction:
    user_id:str = None
    log = None
    output_path = "evaluation/results/"

    def __init__(self, user_id, file:str=None, log=None, export_path:str=None):
        if (file is None and log is None) or (file is not None and log is not None):
            raise Exception("You must either provide a file to load or pass a log object.")
        if file:
            self.log = pd.read_parquet(file, engine='pyarrow')
        else:
            self.log = log


        # self.log = self.log[self.log["org:resource"] != 'User_1'].copy()
        # self.log = self.log[self.log["concept:name"] == 'W_Complete application']

        self.user_id = user_id

        if export_path:
            self.output_path = export_path

    def plot_log(self, features: list, to_predict: str):

        log = self.log.dropna(subset=features+[to_predict])

        colors = {'W_Call after offers': 'red',
                  'W_Call incomplete files': 'blue',
                  'W_Complete application': 'green',
                  'W_Handle leads': 'black',
                  'W_Validate application': 'orange',
                  'W_Assess potential fraud': 'white',
                  'W_Personal Loan collection': 'white',
                  'W_Shortened completion': 'white'}

        log_size = len(log)

        fig, ax = plt.subplots()
        ax.scatter(
            log[['workload']], log[[to_predict]],
            linewidth=0, marker='.', label='Data points (' + str(log_size) + ')')
            # c=log['concept:name'].apply(lambda x: colors[x.strip()]),
        # ax[i].plot(log[[feature]], log[[to_predict]], linewidth=0, marker='s', label='Data points (' + str(log_size) + ')')
        ax.set_xlabel('workload')
        ax.set_ylabel(to_predict)
        ax.legend(facecolor='white')

        fig.savefig(self.output_path + self.user_id +
                    "_dataset.png", dpi=600)



    def evaluate(self, features:list, to_predict:str, plot_evaluation:bool=True):

        log = self.log.copy()

        log.dropna(inplace=True, subset=features+[to_predict])


        ########################
        ### DATA PREPARATION ###

        task_enumeration = {'W_Call after offers': 0,
                  'W_Call incomplete files': 1,
                  'W_Complete application': 2,
                  'W_Handle leads': 3,
                  'W_Validate application': 4,
                  'W_Assess potential fraud': 5,
                  'W_Personal Loan collection': 6,
                  'W_Shortened completion': 7}

        if 'concept:name' in features:
            log.loc[:, 'concept:name'] = log['concept:name'].apply(lambda x: task_enumeration[x.strip()])

        if 'case:RequestedAmount' in features:
            log.loc[:, 'case:RequestedAmount'] = log['case:RequestedAmount'].apply(
                lambda x: int(round(x/5000)))

        if 'org:resource' in features:
            log.loc[:, 'org:resource'] = log['org:resource'].apply(
                lambda x: x[5:] if "User" in x else x)


        # if 'daytime' in features:
        #     log['dt_sin'] = np.sin(log['daytime']*(2.*np.pi/24))
        #     log['dt_cos'] = np.cos(log['daytime']*(2.*np.pi/24))

        #     features.remove('daytime')
        #     features.extend(['dt_sin', 'dt_cos'])


        ##################
        ### SPLIT DATA ###
        X_train, X_test, y_train, y_test = train_test_split(
            log[features], log[to_predict], test_size=0.2, random_state=42)

        #########################
        ### TRAIN AND PREDICT ###

        # regr = linear_model.LinearRegression()
        # regr = linear_model.LogisticRegression(max_iter=200)
        # regr = DecisionTreeRegressor(max_depth=8)
        regr = DecisionTreeRegressor()
        regr2 = RandomForestRegressor(max_depth=8)
        # regr = RandomForestRegressor(max_depth=5, random_state=0)

        regr = regr.fit(X_train, y_train)
        regr2 = regr2.fit(X_train, y_train)

        ####################
        ### GRAPH EXPORT ###
        # dot_data = StringIO()
        # export_graphviz(regr, out_file=dot_data)
        # graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
        # graph.write_pdf(self.output_path + self.user_id +
        #                 "tree.pdf")

        y_pred = regr.predict(X_test)
        y_pred2 = regr2.predict(X_test)

        ##################
        ### EVALUATION ###

        error = 'MSE: %.2f' % mean_squared_error(y_test, y_pred)
        error2 = 'MSE: %.2f' % mean_squared_error(y_test, y_pred2)
        r2 = 'r2: %.2f' % regr.score(X_test, y_test)
        r22 = 'r2: %.2f' % regr2.score(X_test, y_test)
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
        if 'daytime' in features:
            features.remove('daytime')
        if 'org:resource' in features:
            features.remove('org:resource')

        fig, ax = plt.subplots(1,len(features), sharey=True, squeeze=False)
        for i, feature in enumerate(features):
            # ax[0, i].plot(X_test[[feature]], y_test, linewidth=0, marker='.', label='Actual', color="green")
            ax[0, i].plot(X_test[[feature]], y_pred2, linewidth=0, marker='.', label='Random Forest Reg\n'+r22, color="blue")
            ax[0, i].plot(X_test[[feature]], y_pred, linewidth=0, marker='h',  label='Decision Tree Reg\n'+r2, color="red")
            ax[0, i].set_xlabel(feature)
            ax[0, i].set_ylabel(to_predict)
            ax[0, i].set_ylim([-50,None])
        ax[0, len(features)-1].legend(facecolor='white')
        fig.savefig(self.output_path + self.user_id +
                    "_wl_decTree8_predOnly.png", dpi=600)
                    # "_wl_res_decTree.png", dpi=600)
                    # "_wl_dt_linReg.png", dpi=600)


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

pred = Prediction("res20", file="all_wl30min_psInSecMax7200_dt.parquet",
                  export_path='evaluation/results/')

# pred.plot_log(['workload'], 'proc_speed')

# pred.evaluate(['workload','org:resource'], 'proc_speed')

# features = ['concept:name', 'case:RequestedAmount',
#             'workload', 'daytime', 'org:resource']
features = ['workload']

pred.evaluate(features, 'proc_speed')

